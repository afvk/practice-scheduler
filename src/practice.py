import argparse
import json
import random
from pathlib import Path

import numpy as np
from scipy.special import softmax

from spaced_repetition import update_easiness

SOFTMAX_TEMP = 20
SCORES_FILE = Path("./scores.json")
SCORE_QUERY = "Rank how well the exercise went from 0 to 5 (inclusive): "


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--variables", "-v", type=Path, default="examples/jazz-guitar/variables.json"
    )
    parser.add_argument(
        "--exercises", "-e", type=Path, default="examples/jazz-guitar/exercises.tsv"
    )

    return parser.parse_args()


def load_variables(path):
    with open(path) as f:
        return json.load(f)


def load_scores():
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            return json.load(f)
    else:
        return {}


def write_score(scores, updated_score, exercise):
    scores.update({exercise: updated_score})

    with open(SCORES_FILE, "w") as f:
        return json.dump(scores, f, indent=2)


def load_exercises(path):
    exercises = []
    with open(path) as fp:
        for line in fp:
            exercises.append(line.strip())

    return exercises


def fill_template(exercise, variables):
    sampled_variables = {key: random.choice(value) for key, value in variables.items()}
    exercise = exercise.format(**sampled_variables)

    print(
        f"{exercise} - Position: {sampled_variables['position']}, Key: {sampled_variables['key']}"
    )


def sample_exercise(exercises, scores):
    """Sample an exercise based on scores and softmax probabilities."""
    probs = softmax([1 / (scores.get(exercise, 2.5) / SOFTMAX_TEMP) for exercise in exercises])
    i_sampled = np.random.choice(len(probs), p=probs)
    return exercises[i_sampled]


def get_user_score():
    """Get the score from the user input."""
    while True:
        try:
            score = int(input(SCORE_QUERY))
            if score in range(1, 6):
                return score
            else:
                print("Please enter a score between 0 and 5.")
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 5.")


def main():
    args = parse_args()

    variables = load_variables(args.variables)
    exercises = load_exercises(args.exercises)
    scores = load_scores()

    exercise = sample_exercise(exercises, scores)
    score = scores.get(exercise, 2.5)

    fill_template(exercise, variables)
    q = get_user_score()

    updated_score = update_easiness(q, score)

    write_score(scores, updated_score, exercise)


if __name__ == "__main__":
    main()
