import os
import subprocess

import constants


def evaluate(ret: str) -> float:
    return float(ret.split()[0])


def run(output_dir: str, fn: str, params=tuple()) -> str:
    ret_file_path = os.path.join(output_dir, fn)
    with open(os.devnull, "w") as devnull:
        subprocess.check_output(
            'cat {}/{} | {}/solver.out {} > "{}"'.format(
                constants.DATASET_DIR,
                fn,
                output_dir,
                " ".join(map(str, params)),
                ret_file_path,
            ),
            shell=True,
            stderr=devnull,
        )

    ret = load_result(output_dir, fn)
    return ret


def load_result(output_dir: str, fn: str) -> str:
    """Parse dumped text file"""
    ret_file_path = os.path.join(output_dir, fn)
    with open(os.devnull, "w") as devnull:
        res = subprocess.check_output(
            'cat "{}"'.format(ret_file_path), shell=True, stderr=devnull
        )
    ret = res.decode("utf-8")
    return ret
