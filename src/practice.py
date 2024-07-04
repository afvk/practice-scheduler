import argparse
import json
import random
from pathlib import Path

import numpy as np
from scipy.special import softmax

from spaced_repetition import update_easiness

DEFAULT_TEMP = 20
SCORES_FILE = Path("./scores.json")
SCORE_QUERY = "Rank how well the exercise went from 0 to 5 (inclusive): "


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
        return {}


def write_score(scores, updated_score, exercise):
    """Write scores to a JSON file."""
    scores.update({exercise: updated_score})

    with open(SCORES_FILE, "w") as f:
        return json.dump(scores, f, indent=2)


def fill_template(exercise, variables):
    """Fill the exercise template with sampled variables."""
    sampled_local = {
        key: random.choice(value) for key, value in variables["local"].items()
    }
    exercise = exercise.format(**sampled_local)

    sampled_global = ", ".join(
        [f"{key}: {random.choice(value)}" for key, value in variables["global"].items()]
    )

    print(f"{exercise} - {sampled_global}")


def sample_exercise(exercises, scores, softmax_temp):
    """Sample an exercise based on scores and softmax probabilities."""
    probs = softmax(1 / (scores / softmax_temp))
    i_sampled = np.random.choice(len(probs), p=probs)
    return exercises[i_sampled], scores[i_sampled]


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


def add_default_scores(scores, skill_data):
    return np.array([scores.get(exercise, 2.5) for exercise in skill_data["exercises"]])


def main():
    args = parse_args()

    softmax_temp = get_softmax_temp(args)

    skill_data = load_skill_data(args.variables)
    scores_data = load_scores()
    scores = add_default_scores(scores_data, skill_data)

    exercise, score = sample_exercise(skill_data["exercises"], scores, softmax_temp)

    fill_template(exercise, skill_data["variables"])
    q = get_user_score()

    updated_score = update_easiness(q, score)

    write_score(scores_data, updated_score, exercise)


if __name__ == "__main__":
    main()
