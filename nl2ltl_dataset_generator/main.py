import random
from pathlib import Path

import click as click

from nl2ltl_dataset_generator.base import *


def initialize_application(n_samples: int = 10000) -> DatasetDistribution:
    pair_types = [
        PairType(Pattern.ABSENCE, Scope.GLOBAL, 1, absence_global_phrase_template, absence_global_formula_template, PairTypeDistribution(4)),
        PairType(Pattern.UNIVERSAL, Scope.GLOBAL, 1, universal_global_phrase_template, universal_global_formula_template, PairTypeDistribution(14)),
        PairType(Pattern.EXISTENCE, Scope.GLOBAL, 1, existence_global_phrase_template, existence_global_formula_template, PairTypeDistribution(5)),
        PairType(Pattern.RESPONSE, Scope.GLOBAL, 2, response_global_phrase_template, response_global_formula_template, PairTypeDistribution(23)),
        PairType(Pattern.ABSENCE, Scope.AFTER, 2, absence_after_phrase_template, absence_after_formula_template, PairTypeDistribution(1)),
        PairType(Pattern.UNIVERSAL, Scope.AFTER, 2, universal_after_phrase_template, universal_after_formula_template, PairTypeDistribution(1)),
        PairType(Pattern.EXISTENCE, Scope.AFTER, 2, existence_after_phrase_template, existence_after_formula_template, PairTypeDistribution(4)),
        PairType(Pattern.RESPONSE, Scope.AFTER, 3, response_after_phrase_template, response_after_formula_template, PairTypeDistribution(3)),
    ]

    new_dataset_distribution = DatasetDistribution(n_samples, pair_types)

    new_dataset_distribution.update_info()

    return new_dataset_distribution


@log_time
@click.command()
@click.argument("dataset_type", type=str)
@click.option("--number-of-samples", "-s", type=int, default=10000)
@click.option("--dataset-save-path", "-o", type=click.Path(file_okay=True, exists=False), default=Path("./results/dataset.csv"))
@click.option("--identifiers-file-path", "-i", type=click.Path(file_okay=True, exists=False), required=False, default=None)
@click.option("--seed", "-r", type=int, default=None, required=False)
def main(
        dataset_type: str,
        number_of_samples: int = 10000,
        dataset_save_path: Path = Path("./results/dataset.csv"),
        identifiers_file_path: Path = None,
        seed: int = None,
):
    if seed is not None:
        random.seed(seed)

    dataset_save_path: Path = Path(dataset_save_path)
    print(dataset_save_path.resolve())

    identifiers_file_path = Path(identifiers_file_path) if identifiers_file_path is not None else None
    print(identifiers_file_path.resolve())

    if dataset_type.upper() not in DatasetType.names():
        raise InvalidDatasetType(dataset_type)

    dataset_type = DatasetType[dataset_type.upper()]

    dataset_distribution = initialize_application(number_of_samples)

    generation_strategy = generation_strategy_factory(dataset_type, dataset_distribution, identifiers_file_path)

    dataset_generator = DatasetGenerator(dataset_distribution, dataset_type, generation_strategy)

    dataset = dataset_generator.generate_dataset()

    save_csv(dataset, dataset_save_path)

    print(get_means())

    print(f"Dataset generated in {dataset_save_path.resolve()}")


if __name__ == '__main__':
    main()