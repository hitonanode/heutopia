import json
import os
import subprocess
from typing import Optional, Union


def run(
    solver_abs_path: str,
    input_dir_abs_path: str,
    input_filename: str,
    solver_args: Optional[list[Union[str, float, int]]],
    show_detail: bool,
) -> dict[str, Union[str, float, int]]:
    comm = "cat {} | {} {}".format(
        os.path.join(input_dir_abs_path, input_filename),
        solver_abs_path,
        " ".join([str(arg) for arg in solver_args]) if solver_args else "",
    )
    process = subprocess.run(
        comm, shell=True, check=False, capture_output=True, text=True
    )
    if process.returncode:
        print("Error: {}".format(input_filename))

    ret: dict[str, Union[str, float, int]] = {"input_filename": input_filename}
    ret |= json.loads(process.stdout)

    if show_detail:
        print("Run {}: {}".format(input_filename, ret))

    return ret
