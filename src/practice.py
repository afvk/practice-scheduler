import argparse
import json
import random
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--variables", "-v", type=Path, default="data/variables.json")
    parser.add_argument("--exercises", "-e", type=Path, default="data/exercises.tsv")
    parser.add_argument("--solos", "-s", type=Path, default="data/solos.txt")
    parser.add_argument("--repertoire", "-r", type=Path, default="data/repertoire.txt")

    return parser.parse_args()


def load_variables(path):
    with open(path) as f:
        return json.load(f)


def load_exercises(path):
    exercises = []
    with open(path) as fp:
        for line in fp:
            exercises.append(
                {"exercise": line.strip(), "type": "improvisation",}  # TODO: remove
            )
    exercises = pd.DataFrame(exercises)
    exercises = exercises.groupby("type").sample().sample(1)
    return exercises


def load_solos(path):

    with open(path) as f:
        solos = []
        for solo in f.readlines():
            standard, link = solo.strip().split("\t")
            solos.append(f"{standard} ({link})")
    return solos


def load_repertoire(path):
    with open(path) as f:
        return [standard.strip() for standard in f.readlines()]


def sample_exercises(exercises, standards, solos, variables):

    exercises["exercise"] = exercises["exercise"].apply(
        lambda x: x.format(
            bars_improv=random.choice(variables["bars_improv"]),
            chord_tone=random.choice(variables["chord_tone"]),
            up_down=random.choice(variables["up_down"]),
            direction=random.choice(variables["direction"]),
            string_set=random.choice(variables["string_set"]),
            drop2_string_set=random.choice(variables["drop2_string_set"]),
            drop3_string_set=random.choice(variables["drop3_string_set"]),
            standard=random.choice(standards),
            scale=random.choice(variables["scale"]),
            solo=random.choice(solos),
            connection_type=random.choice(variables["connection_type"]),
            another_standard=random.choice(standards),
        )
    )
    exercises["position"] = [
        random.choice(variables["position"]) for _ in range(len(exercises))
    ]
    exercises["key"] = [random.choice(variables["key"]) for _ in range(len(exercises))]
    return exercises


def display_table(exercises):
    print(exercises[["type", "exercise", "position", "key"]].to_markdown(index=False))


def main():
    args = parse_args()

    variables = load_variables(args.variables)
    exercises = load_exercises(args.exercises)
    solos = load_solos(args.solos)
    standards = load_repertoire(args.repertoire)

    practice = sample_exercises(exercises, standards, solos, variables)

    display_table(practice)


if __name__ == "__main__":
    main()
