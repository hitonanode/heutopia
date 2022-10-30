#!/usr/bin/env python3
import datetime
import shutil
import os
import random
import string
import time
import multiprocessing
import subprocess

import constants
import external_solver

NUM_CASE_LIMIT = 512


def wrapper(output_dirname: str, infile: str, params):
    ret = external_solver.run(output_dirname, infile, params)
    print("Run {} as params={}: {}".format(infile, params, ret.split()[:1]))  # Modify
    return_dict[infile] = external_solver.evaluate(ret)


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    start_time = time.perf_counter()
    pool = multiprocessing.get_context("fork").Pool(processes=constants.NUM_PROCESS)

    output_dirname = "result{}_{}".format(
        datetime.datetime.now().strftime("%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(4)),
    )

    os.makedirs(output_dirname)
    shutil.copy2("./main.cpp", os.path.join(output_dirname, "main.cpp.old"))
    subprocess.check_output("make", shell=True)
    shutil.copy2("./solver.out", os.path.join(output_dirname, "solver.out"))

    input_fns = sorted(os.listdir(constants.DATASET_DIR))[:NUM_CASE_LIMIT]
    print("Input: {}".format(input_fns))

    for infile in input_fns:
        pool.apply_async(wrapper, args=(output_dirname, infile, tuple()))

    pool.close()
    pool.join()

    end_time = time.perf_counter()
    avg_score: float = sum(return_dict.values()) / len(return_dict.values())  # type: ignore

    print("Length: {}".format(len(return_dict)))
    print("Score average: {}".format(avg_score))
    print("Expected score: {}".format(avg_score * constants.SCOREBOARD_TESTCASES))
    print("Elapsed time: {} sec.".format(end_time - start_time))

    lst = sorted([(score, name) for name, score in return_dict.items()])
    print("Worst cases: {}".format(lst[:10]))
