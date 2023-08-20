#!/usr/bin/env python3
import datetime
import json
import multiprocessing
import os
import pathlib
import random
import shutil
import string
import subprocess
from multiprocessing.pool import AsyncResult

import optuna
import yaml

from external_solver import run


def objective(trial: optuna.trial.Trial):
    # Modify here
    # https://optuna.readthedocs.io/en/stable/reference/multi_objective/generated/optuna.multi_objective.trial.MultiObjectiveTrial.html
    x = trial.suggest_int("x", 4, 12, log=False)
    params = (x,)

    dataset_dir = str(pathlib.Path(config["dataset_dir"]).resolve())

    pool = multiprocessing.get_context("fork").Pool(processes=config["num_process"])
    results: list[AsyncResult] = [
        pool.apply_async(
            run, args=(str(solver_path), dataset_dir, infile, params, False)
        )
        for infile in sorted(os.listdir(dataset_dir))[: config["num_case_limit"]]
    ]

    pool.close()
    pool.join()

    return sum([r.get()["score"] for r in results])


if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    print(config)

    train_id = "train{}_{}".format(
        datetime.datetime.now().strftime("%H%M%S"),
        "".join(random.choice(string.ascii_lowercase) for _ in range(4)),
    )

    output_dirname = pathlib.Path(train_id).resolve()

    os.makedirs(output_dirname)
    shutil.copy2("./main.cpp", output_dirname / "main.cpp.old")
    subprocess.check_output("make", shell=True)
    solver_path = output_dirname / "solver.out"
    shutil.copy2("./solver.out", solver_path)

    study = optuna.create_study(
        study_name=train_id,
        direction="maximize",
        storage="sqlite:///train.db",
        load_if_exists=True,
    )

    # study.enqueue_trial({"x": 5,})

    study.optimize(objective, n_trials=config["optuna_num_trials"], n_jobs=1)
    print(study.best_params)

    with open(output_dirname / "best_parameters.json", "w") as f:
        json.dump(study.best_params, f)

    study.trials_dataframe().to_csv(output_dirname / "trials.csv")
