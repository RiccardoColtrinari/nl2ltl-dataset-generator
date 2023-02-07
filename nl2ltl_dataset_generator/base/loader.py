import string
from typing import List
import random
import itertools

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from nl2ltl_dataset_generator.base.data_model import UnrestrictedIdentifier, Dataset
from nl2ltl_dataset_generator.base.log import log_time


def load_unrestricted_identifiers(file_path: Path) -> List[UnrestrictedIdentifier]:
    if not file_path.exists():
        raise Exception(f"{file_path} does not exists!")

    with file_path.open('r') as fp:
        lines = fp.readlines()

    identifiers = []

    for line in lines:
        parts = line.split(';')

        determiners = parts[0].split('-')

        noun = parts[1].strip()

        verbs = [verb.strip().split('-') for verb in parts[2].strip().split(',')]

        verbs = [(verb[0], verb[1]) if len(verb) > 1 else ('', verb[0]) for verb in verbs]

        identifiers.extend([
            UnrestrictedIdentifier(determiners, noun, verb.split(' '), aux.split(' ') if aux != '' else None)
            for noun, (aux, verb) in itertools.product([noun], verbs)
        ])

    return identifiers


@log_time
def save_csv(dataset: Dataset, file_path: Path) -> None:
    df = pd.DataFrame(
        [[f"{pair.pair_type.pattern}_{pair.pair_type.scope}", pair.formula, pair.phrase] for pair in dataset.pairs],
        columns=["pair_type", "ltl", "en"]
    )

    df.to_csv(file_path, index=False)


def save_opennmt_format(dataset: Dataset,
                        directory_path: Path,
                        test_size: float = .33,
                        val_size: float = None,
                        shuffle: bool = True) -> None:
    SRC_TRAIN = directory_path / "src-train.txt"
    SRC_VAL = directory_path / "src-val.txt"
    SRC_TEST = directory_path / "src-test.txt"

    TGT_TRAIN = directory_path / "tgt-train.txt"
    TGT_VAL = directory_path / "tgt-val.txt"
    TGT_TEST = directory_path / "tgt-test.txt"

    if shuffle:
        random.shuffle(dataset.pairs)

    df = pd.DataFrame(
        [[pair.formula, pair.phrase] for pair in dataset.pairs],
        columns=["ltl_formula", "phrase"]
    )

    X_train, X_test, Y_train, Y_test = train_test_split(df["phrase"], df["ltl_formula"], test_size=test_size,
                                                        shuffle=False)

    X_train, X_val, Y_train, Y_val = (
        train_test_split(X_train, Y_train, test_size=val_size, shuffle=False)
        if val_size is not None
        else (X_train, None, Y_train, None)
    )

    pd.DataFrame(X_train).to_csv(SRC_TRAIN, sep='\n', index=False, header=False)
    pd.DataFrame(X_val).to_csv(SRC_VAL, sep='\n', index=False, header=False) if X_val is not None else None
    pd.DataFrame(X_test).to_csv(SRC_TEST, sep='\n', index=False, header=False)

    pd.DataFrame(Y_train).to_csv(TGT_TRAIN, sep='\n', index=False, header=False)
    pd.DataFrame(Y_val).to_csv(TGT_VAL, sep='\n', index=False, header=False) if Y_val is not None else None
    pd.DataFrame(Y_test).to_csv(TGT_TEST, sep='\n', index=False, header=False)
