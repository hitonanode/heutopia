#!/usr/bin/env python3
import datetime
import json
import shutil
import optuna
import os
import random
import string
import multiprocessing
import subprocess

import constants
import external_solver


NUM_CASES_LIMIT = 512
NUM_TRIALS = 20


def objective(trial: optuna.trial.Trial):
    # Modify here
    # https://optuna.readthedocs.io/en/stable/reference/multi_objective/generated/optuna.multi_objective.trial.MultiObjectiveTrial.html
    x = trial.suggest_int("x", 4, 12, log=False)
    params = (str(x),)

    input_fns = sorted(os.listdir(constants.DATASET_DIR))[:NUM_CASES_LIMIT]
    pool = multiprocessing.Pool(processes=constants.NUM_PROCESS)

    for infile in input_fns:
        pool.apply_async(external_solver.run, args=(output_dirname, infile, params))
    pool.close()
    pool.join()

    return sum(
        [
            external_solver.evaluate(external_solver.load_result(output_dirname, fn))
            for fn in input_fns
        ]
    )


if __name__ == "__main__":

    output_dirname = "train{}_{}".format(
        datetime.datetime.now().strftime("%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(4)),
    )

    os.makedirs(output_dirname)
    shutil.copy2("./main.cpp", os.path.join(output_dirname, "main.cpp.old"))
    subprocess.check_output("make", shell=True)
    shutil.copy2("./solver.out", os.path.join(output_dirname, "solver.out"))

    study = optuna.create_study(study_name=output_dirname, direction="maximize")
    study.optimize(objective, n_trials=NUM_TRIALS, n_jobs=1)
    print(study.best_params)

    with open(os.path.join(output_dirname, "best_parameters.json"), "w") as f:
        json.dump(study.best_params, f)
