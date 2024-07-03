import argparse
import json
import random
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--variables", "-v", type=Path, default="examples/jazz-guitar/variables.json")
    parser.add_argument("--exercises", "-e", type=Path, default="examples/jazz-guitar/exercises.tsv")

    return parser.parse_args()


def load_variables(path):
    with open(path) as f:
        return json.load(f)


def load_exercise(path):
    exercises = []
    with open(path) as fp:
        for line in fp:
            exercises.append(line.strip())

    exercise = random.sample(exercises, 1)[0]
    return exercise


def fill_template(exercise, variables):
    sampled_variables = {key: random.choice(value) for key, value in variables.items()}
    exercise = exercise.format(**sampled_variables)

    print(f"{exercise} - Position: {sampled_variables['position']}, Key: {sampled_variables['key']}")


def main():
    args = parse_args()

    variables = load_variables(args.variables)
    exercise = load_exercise(args.exercises)

    fill_template(exercise, variables)


if __name__ == "__main__":
    main()
