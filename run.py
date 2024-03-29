import datetime
import json
import multiprocessing
import os
import pathlib
import random
import shutil
import string
import subprocess
import tempfile
import time
from multiprocessing.pool import AsyncResult

import pandas as pd  # type: ignore
import yaml

import external_solver
from heutopia.cpphelper import expandcpp
from heutopia.exporter import (
    AbstractExporter,
    BatchResult,
    GSheetsExporter,
    LocalFileExporter,
    StdoutExporter,
)

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    print("Config:")
    print(json.dumps(config, indent=4))
    print("")

    start_time = time.perf_counter()
    pool = multiprocessing.get_context("fork").Pool(processes=config["num_process"])
    num_case_limit = config["num_case_limit"]

    run_id = "{}{}".format(
        datetime.datetime.now().strftime("%y%m%d%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(2)),
    )

    exporters: list[AbstractExporter] = [
        StdoutExporter(config["print_columns"]),
        LocalFileExporter(output_dirpath=os.path.join("result", run_id)),
    ]

    if "google_sheets_exporter" in config:
        exporters.append(
            GSheetsExporter(
                run_id=run_id,
                gcp_sa_path=config["google_sheets_exporter"]["gcp_sa_path"],
                sheet_key=config["google_sheets_exporter"]["sheet_key"],
            )
        )

    print("\nEnabled exporters:")
    for exporter in exporters:
        print("  - {}".format(exporter.summary()))
    print("")

    cpp_src = expandcpp(os.path.abspath("./main.cpp"))
    for exporter in exporters:
        exporter.dump_src(cpp_src)

    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_output("make", shell=True)
        solver_path = (pathlib.Path(tmpdir) / "solver.out").resolve()
        shutil.copy2("./solver.out", solver_path)

        input_filesinfo: list[tuple[str, str]] = list()

        for root, _, files in os.walk(config["dataset_dir"]):
            input_filesinfo.extend([(root, f) for f in files])

        input_filesinfo = sorted(input_filesinfo)[: config["num_case_limit"]]

        print("Input: {} ({} cases)".format(input_filesinfo, len(input_filesinfo)))

        process_list: list[AsyncResult] = [
            pool.apply_async(
                external_solver.run,
                args=(solver_path, input_filedir, input_filename, None, True),
            )
            for input_filedir, input_filename in input_filesinfo
        ]
        pool.close()
        pool.join()

    end_time = time.perf_counter()

    result = BatchResult(
        df=pd.DataFrame([x.get() for x in process_list if x.successful()])
        .sort_values("input_filename", ascending=True)
        .reset_index(drop=True)
    )

    for exporter in exporters:
        exporter.dump(result)

    print("Elapsed time: {} sec.".format(end_time - start_time))
