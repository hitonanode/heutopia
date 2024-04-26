import json
import os
import subprocess
import time
from typing import Optional, Union

from heutopia.config import RunnerConfig


def standalone_run(
    solver_abs_path: str,
    input_dir_abs_path: str,
    input_filename: str,
    solver_args: Optional[list[Union[str, float, int]]],
    runner_config: RunnerConfig,
    show_detail: bool,
) -> dict[str, Union[str, float, int]]:
    args_str = " ".join([str(arg) for arg in solver_args]) if solver_args else ""

    comm = runner_config.run_comand.format(
        INPUT_FILE=os.path.join(input_dir_abs_path, input_filename),
        SOLVER_CMD=solver_abs_path + " " + args_str,
        SOLVER_OUTPUT="/dev/null",
    )

    begin_ns = time.perf_counter_ns()
    process = subprocess.run(
        comm, shell=True, check=False, capture_output=True, text=True
    )
    end_ns = time.perf_counter_ns()
    spent_ms = (end_ns - begin_ns) // 1000000

    if process.returncode:
        print("Error: {}".format(input_filename))

    ret: dict[str, Union[str, float, int]] = {"input_filename": input_filename}
    ret |= json.loads(process.stdout)
    ret["msec"] = spent_ms

    if show_detail:
        print("Run {}: {}".format(input_filename, ret))

    return ret
