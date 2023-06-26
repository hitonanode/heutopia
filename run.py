import datetime
import multiprocessing
import os
import pathlib
import random
import shutil
import string
import subprocess
import time
from multiprocessing.pool import AsyncResult

import pandas as pd  # type: ignore
import yaml

import external_solver

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    print(config)

    start_time = time.perf_counter()
    pool = multiprocessing.get_context("fork").Pool(processes=config["num_process"])
    num_case_limit = config["num_case_limit"]

    output_dirname = "result{}_{}".format(
        datetime.datetime.now().strftime("%y%m%d%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(4)),
    )

    os.makedirs(output_dirname)
    subprocess.check_output(
        "poetry run python3 expander.py main.cpp -c > {}".format(
            os.path.join(output_dirname, "main.cpp.old")
        ),
        shell=True,
    )
    subprocess.check_output("make", shell=True)
    solver_path = str(
        pathlib.Path(os.path.join(output_dirname, "solver.out")).resolve()
    )
    shutil.copy2("./solver.out", solver_path)
    print(config["dataset_dir"])
    input_filesinfo: list[tuple[str, str]] = list()

    def choose_file(s: str) -> bool:
        # if s[-3:] != ".in":
        #     return False

        # if Parameter.parse_str(s[:-3]).idx != 1:
        #     return False

        return True

    for root, _, files in os.walk(config["dataset_dir"]):
        input_filesinfo.extend([(root, f) for f in files if choose_file(f)])

    input_filesinfo = sorted(input_filesinfo)[: config["num_case_limit"]]

    print("Input: {} ({} cases)".format(input_filesinfo, len(input_filesinfo)))

    process_list: list[tuple[str, AsyncResult]] = [
        (
            input_filename,
            pool.apply_async(
                external_solver.run,
                args=(solver_path, input_filedir, input_filename, None, True),
            ),
        )
        for input_filedir, input_filename in input_filesinfo
    ]
    pool.close()
    pool.join()

    end_time = time.perf_counter()

    return_list = [(name, x.get()) for (name, x) in process_list if x.successful()]
    return_list.sort()
    df = pd.DataFrame([x for _, x in return_list])

    mean_df = df.mean(numeric_only=True).round(4)
    min_df = df.min()
    max_df = df.max()
    mean_df["input_filename"] = "mean"
    min_df["input_filename"] = "min"
    max_df["input_filename"] = "max"

    df_to_save = pd.concat([df, pd.DataFrame([mean_df, min_df, max_df])])
    # df_to_save.to_csv(os.path.join(output_dirname, "summary.csv"), index=False)
    df_to_save.to_excel(os.path.join(output_dirname, "summary.xlsx"), index=False)

    print(mean_df.to_json(indent=4))

    print("Length: {} / {}".format(len(return_list), len(process_list)))
    print("Elapsed time: {} sec.".format(end_time - start_time))

    for column in config["print_columns"]:
        lst = sorted([(x[column], name) for name, x in return_list])
        print("Worst cases by {}: {}".format(column, lst[:10]))
