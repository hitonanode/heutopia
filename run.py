#!/usr/bin/env python3
import datetime
import shutil
import os
import random
import string
import time
import multiprocessing
import subprocess

manager = multiprocessing.Manager()
return_dict = manager.dict()


def RunCase(output_dir: str, fn: str):
    ret_file_path = os.path.join(output_dir, fn)
    with open(os.devnull, 'w') as devnull:
        subprocess.check_output('cat tools/in/{} | {}/solver.out > "{}"'.format(fn, output_dir, ret_file_path), shell=True, stderr=devnull)
        res = subprocess.check_output('cat "{}"'.format(ret_file_path), shell=True, stderr=devnull)
    st = res.decode('utf-8')
    score = int(st.split()[0])
    return_dict[fn] = score
    print("Run {}: {}".format(fn, st.split('\n')[:2]))


if __name__ == "__main__":
    num_proc = 16
    num_case = 9999

    start_time = time.perf_counter()
    pool = multiprocessing.Pool(processes=num_proc)

    output_dirname = "{}_{}".format(
        datetime.datetime.now().strftime("%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(4))
    )

    os.makedirs(output_dirname)
    shutil.copy2("./main.cpp", os.path.join(output_dirname, "main.cpp.old"))
    subprocess.check_output("make", shell=True)
    shutil.copy2("./solver.out", os.path.join(output_dirname, "solver.out"))

    input_fns = sorted(os.listdir('./tools/in'))[:num_case]
    print("Input: {}".format(input_fns))
    for infile in input_fns:
        pool.apply_async(RunCase, args=(output_dirname, infile,))

    pool.close()
    pool.join()

    L = sorted(list(return_dict.items()))
    end_time = time.perf_counter()
    print(L)
    print("Score average: {}".format(sum(return_dict.values()) / len(return_dict.values())))
    print("Elapsed time: {} sec.".format(end_time - start_time))
