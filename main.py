import pandas as pd
import argparse
from glob import glob
import os


def warning_obj_not_found(optimizer):
    print(f"[Warning]Objective not found for {optimizer}")
    return


def parse_obj_con(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Locally optimal; objective" in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_fmc(logpath, verbose=False):
    objs = {}
    with open(logpath, "r") as f:

        for line in f:
            if ".nl" in line:
                instance = line.split("\\")[-1].split(".")[0]

                # Find associated fval
                for line in f:
                    if "fval" in line:
                        next(f)  # skip the empty line
                        objs[instance] = float(next(f))
                        break

    return objs


def parse_obj_ipo(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Objective..............." in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_kni(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Final objective value               =" in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_loq(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "primal objective " in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_pen(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Objective                        " in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_snp(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Objective            " in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


def parse_obj_wor(logpath, verbose=False):
    with open(logpath, "r") as f:
        for line in f:
            if "Final objective value ............." in line:
                return float(line.strip().split()[-1])
    if verbose:
        warning_obj_not_found(logpath)
    return None


class BenchViewer:
    def __init__(self):
        # Hard-coded paths
        _logs_folder = "ampl-nlp_logs"
        _optimizers = ["con", "fmc", "ipo", "kni", "loq", "pen", "snp", "wor"]
        _parsers = [
            parse_obj_con,
            parse_obj_fmc,
            parse_obj_ipo,
            parse_obj_kni,
            parse_obj_loq,
            parse_obj_pen,
            parse_obj_snp,
            parse_obj_wor,
        ]

        metadata = {
            "optimizers": _optimizers,
            "results_paths": [
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    _logs_folder,
                    opt + "_results",
                )
                for opt in _optimizers
            ],
            "suffix": ["con", "txt", "ipo", "kni", "loq", "pen", "snp", "wor"],
            "is_single_log": [False, True, False, False, False, False, False, False],
        }

        # Use CONPT logs to create a list of instances
        USED_OPT_INDEX = 0
        results_path = metadata["results_paths"][USED_OPT_INDEX]
        suffix = metadata["suffix"][USED_OPT_INDEX]
        instances = []
        for log in glob(os.path.join(results_path, f"*.{suffix}")):
            instances.append(os.path.basename(log).split(".")[0])

        # Create empty data frame for objective values
        obj_df = pd.DataFrame(
            {"optimizer": _optimizers}, columns=["optimizer", *instances]
        )

        # Populate objectives
        for optidx, (optname, results_path, suffix, parser) in enumerate(
            zip(
                metadata["optimizers"],
                metadata["results_paths"],
                metadata["suffix"],
                _parsers,
            )
        ):
            # For fmc, there is 1 single log file
            if optname == "fmc":
                log = os.path.join(results_path, "fmincon.txt")
                objs = parser(log)
                for instance, obj in objs.items():
                    obj_df.iloc[optidx][instance] = obj

            else:
                for log in glob(os.path.join(results_path, f"*.{suffix}")):
                    instance = os.path.splitext(os.path.basename(log))[0]
                    obj_df.iloc[optidx][instance] = parser(log)

        obj_df.to_csv("raw.csv")

        return


def main():
    p = argparse.ArgumentParser()
    args = p.parse_args()

    viewer = BenchViewer()

    return


if __name__ == "__main__":
    main()
