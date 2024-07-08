import argparse
import json
import random
import re
from pathlib import Path

import numpy as np
from scipy.special import softmax

from spaced_repetition import update_easiness

DEFAULT_TEMP = 40
SCORES_FILE = Path("./scores.json")
SCORE_QUERY = "Rate the easiness from 0 (very difficult) to 5 (very easy): "


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--variables", "-v", type=Path, default="examples/jazz-guitar.json"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--softmax-temp",
        type=float,
        help="""Softmax temperature used when sampling an exercise based on the
             easiness scores. Values close to zero correspond to sampling from a
             uniform distribution, ignoring the scores. High values correspond
             to always picking the most difficult exercise.""",
        default=DEFAULT_TEMP,
    )
    group.add_argument(
        "--sampling-strategy", choices=["random", "default", "pick-hardest"]
    )
    return parser.parse_args()


def get_softmax_temp(args):
    if args.softmax_temp:
        return args.softmax_temp

    else:
        if args.sampling_strategy == "random":
            return 1e-6

        elif args.sampling_strategy == "default":
            return DEFAULT_TEMP

        elif args.sampling_strategy == "pick-hardest":
            return 1e6

        else:
            raise ValueError(
                f"Sampling strategy {args.sampling_strategy} not supported."
            )


def load_skill_data(path):
    """Load exercise and variables from a JSON file."""
    with open(path) as f:
        return json.load(f)


def load_scores():
    """Load cores from a JSON file."""
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            return json.load(f)
    else:
        return {"exercises": {}, "variables": {"local": {}, "global": {},}}


def write_score(scores, updated_score, exercise):
    """Write scores to a JSON file."""
    scores["exercises"].update({exercise: updated_score})

    with open(SCORES_FILE, "w") as f:
        return json.dump(scores, f, indent=2)


def fill_template(exercise, data, sample_inds):
    """Fill the exercise template with sampled variables."""
    sampled_local = {
        var: instances[sample_inds[var]]
        for var, instances in data["variables"]["local"].items()
    }
    exercise = exercise.format(**sampled_local)

    sampled_global = ", ".join(
        [
            f"{var}: {instances[sample_inds[var]]}"
            for var, instances in data["variables"]["global"].items()
        ]
    )

    print(f"{exercise} - {sampled_global}")


def sample_weighted(scores, softmax_temp):
    """Sample an exercise based on scores and softmax temperature."""
    probs = softmax(1 / (scores / softmax_temp))
    i_sampled = np.random.choice(len(probs), p=probs)
    return i_sampled


def get_user_score():
    """Get the score from the user input."""
    while True:
        try:
            score = int(input(SCORE_QUERY))
            if score in range(0, 6):
                return score
            else:
                print("Please enter a score between 0 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 5.")


def add_default_scores(scores, data):
    scores["exercises"] = {
        exercise: scores["exercises"].get(exercise, 2.5)
        for exercise in data["exercises"]
    }
    for var_type in ["local", "global"]:
        for var, instances in data["variables"][var_type].items():
            if var not in scores["variables"][var_type]:
                scores["variables"][var_type][var] = {}
            for inst in instances:
                if inst not in scores["variables"][var_type][var]:
                    scores["variables"][var_type][var][inst] = 2.5

    return scores


def sample_variables(scores, softmax_temp):
    sample_inds = {}
    for var_type in ["local", "global"]:
        for var, instances in scores["variables"][var_type].items():
            i_sampled = sample_weighted(
                np.array(list(instances.values())), softmax_temp
            )
            sample_inds[var] = i_sampled
    return sample_inds


def main():
    args = parse_args()

    softmax_temp = get_softmax_temp(args)

    skill_data = load_skill_data(args.variables)
    scores_data = load_scores()
    scores = add_default_scores(scores_data, skill_data)
    i_sampled = sample_weighted(
        np.array(list(scores["exercises"].values())), softmax_temp
    )
    sample_inds = sample_variables(scores, softmax_temp)

    exercise = skill_data["exercises"][i_sampled]
    score = scores["exercises"][exercise]

    fill_template(exercise, skill_data, sample_inds)
    q = get_user_score()
    updated_score = update_easiness(q, score)

    used_vars = {
        'local': re.findall(r"\{(.*?)\}", exercise),
        'global': skill_data["variables"]["global"],
    }

    for var_type, vars in used_vars.items():
        for var in vars:
            i = sample_inds[var]
            sampled_inst = skill_data["variables"][var_type][var][i]
            score = scores["variables"][var_type][var][sampled_inst]

            print(f"How easy was {sampled_inst}?")
            q = get_user_score()
            updated_score = update_easiness(q, score)

            scores["variables"][var_type][var][sampled_inst] = updated_score

    write_score(scores_data, updated_score, exercise)


if __name__ == "__main__":
    main()
