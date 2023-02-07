import itertools
import math
import random
import string
from abc import ABC
from enum import Enum
from pathlib import Path
from typing import List, Generator, Tuple, Any

import numpy as np

from nl2ltl_dataset_generator.base.data_model import DatasetDistribution, DatasetType, Identifier, Pair, PairTerm, LogicalOperator, PairType, \
    RestrictedIdentifier, Dataset
from nl2ltl_dataset_generator.base.loader import load_unrestricted_identifiers
from nl2ltl_dataset_generator.base.log import log_time


class TermBuildingMode(Enum):
    LEQ = '<='
    EQUALS = '='
    GEQ = '>='


class TermBuilder:
    """Generate sets of terms of dynamic dimensions, where the dimension is the number of internal identifiers."""
    MAX_DIMENSION = 3
    LOGICAL_OPERATORS = [LogicalOperator.AND, LogicalOperator.OR]

    def __init__(self, dimension: int = 2, mode: TermBuildingMode = TermBuildingMode.LEQ):
        if dimension > self.MAX_DIMENSION:
            raise Exception(
                f"A {self.__class__.__name__} can generate dispositions of at most {self.MAX_DIMENSION} identifiers."
            )

        self.terms_dimension = dimension
        self.building_mode = mode

    @log_time
    def _term_generator(self, identifiers: List[Identifier], dimension: int) -> Generator[PairTerm, Any, None]:
        """Generate terms of a given dimension, where the dimension is the number of identifiers."""
        if dimension > 1:
            for symbol in self.LOGICAL_OPERATORS:
                for permutation in itertools.permutations(identifiers, dimension):
                    yield PairTerm([*permutation], symbol)
        else:
            for permutation in itertools.permutations(identifiers, dimension):
                yield PairTerm([*permutation])

    @log_time
    def get_terms(self, identifiers: List[Identifier]) -> Generator[PairTerm, Any, None]:
        """Generate all the requested terms"""
        if self.building_mode == TermBuildingMode.EQUALS:
            return self._term_generator(identifiers, self.terms_dimension)

        dimensions = (
            range(1, self.terms_dimension + 1)
            if self.building_mode == TermBuildingMode.LEQ
            else range(self.terms_dimension, self.MAX_DIMENSION + 1)
        )

        return (
            pair_term
            for dimension in dimensions
            for pair_term in self._term_generator(identifiers, dimension)
        )


# total_dispositions = n!/(n-k)!, i want to know n.
@log_time
def calculate_sample_number_dispositions(total_dispositions: int, k: int, maximum_n: int):
    # print(f"DATI1: {total_dispositions}, {k}, {maximum_n}")
    for n in range(20, maximum_n, 5):
        if (disp := math.factorial(n)/(math.factorial(n-k))) > total_dispositions:
            # print(f"DATI2: {disp}")
            return n

    # print(maximum_n)
    return maximum_n


class Sampler:

    @staticmethod
    @log_time
    def get_pairs(terms: List[PairTerm], pair_type: PairType) -> List[Pair]:
        n = int(np.around(calculate_sample_number_dispositions(pair_type.distribution.new_value, pair_type.n_terms, len(terms))))

        random.shuffle(terms)

        samples = random.sample(terms, n)

        if pair_type.n_terms != 1:
            samples = list(itertools.permutations(samples, pair_type.n_terms))
        else:
            samples = [[sample] for sample in samples]

        samples = random.sample(samples, pair_type.distribution.new_value)

        for sample in samples:
            yield Pair([*sample], pair_type)


def get_terms_dimension(n_terms: int) -> Tuple[int, TermBuildingMode]:
    """Get the number of allowed identifiers per term, given the number of terms."""
    identifiers_terms_mapping = {
        1: (3, TermBuildingMode.LEQ),
        2: (2, TermBuildingMode.LEQ),
        3: (1, TermBuildingMode.EQUALS),
    }

    return identifiers_terms_mapping.get(n_terms)


class RestrictedIdentifierGenerator:
    """Generate a Restricted identifier."""
    def __init__(self):
        self.min_length = 5
        self.max_length = 15
        self.letters = string.ascii_letters + '_'

    def generate_identifier(self) -> RestrictedIdentifier:
        length = random.randint(self.min_length, self.max_length)
        identifier_string = ''.join([random.choice(self.letters) for _ in range(length)])
        return RestrictedIdentifier(["the", "a", "an", ""], identifier_string)


class TermGenerator:
    """Generate a PairTerm."""
    def __init__(self, n_identifiers: int = 2):
        self.LOGICAL_OPERATORS_CHOICES = [LogicalOperator.AND, LogicalOperator.OR]
        self.identifier_generator = RestrictedIdentifierGenerator()
        self.n_identifiers = n_identifiers

    def generate_term(self):
        n_identifiers = random.randint(1, self.n_identifiers) if self.n_identifiers > 1 else 1

        chosen_symbol = random.choice(self.LOGICAL_OPERATORS_CHOICES) if n_identifiers > 1 else None

        identifiers = [self.identifier_generator.generate_identifier() for _ in range(0, n_identifiers)]

        return PairTerm(identifiers, chosen_symbol)


class PairsGenerator:
    """Generates a list of Pair of a given PairType."""

    @staticmethod
    @log_time
    def get_pairs(pair_type: PairType) -> List[Pair]:
        terms_dimension, _ = get_terms_dimension(pair_type.n_terms)
        term_generator = TermGenerator(terms_dimension)
        pairs = []
        for _ in range(pair_type.distribution.new_value):
            pair_terms = []
            for _ in range(pair_type.n_terms):
                pair_terms.append(term_generator.generate_term())

            pairs.append(Pair(pair_terms, pair_type))

        return pairs


class PairGenerationStrategy(ABC):
    """Generates a set of Pair."""
    def __init__(self, dataset_distribution: DatasetDistribution, identifiers: List[Identifier] = None):
        self.dataset_distribution = dataset_distribution
        self.identifiers = identifiers

    def get_pairs(self) -> List[Pair]:
        pass


class RestrictedPairGenerationStrategy(PairGenerationStrategy):
    """Generates a set of Restricted Pair."""
    def __init__(self, dataset_distribution: DatasetDistribution):
        super(RestrictedPairGenerationStrategy, self).__init__(dataset_distribution)

    @log_time
    def get_pairs(self) -> List[Pair]:
        pair_types = self.dataset_distribution.pair_types
        pairs = []

        for pair_type in pair_types:
            pairs.extend(PairsGenerator.get_pairs(pair_type))

        return pairs


@log_time
def unrestricted_from_type(pair_type: PairType, identifiers: List[Identifier]) -> List[Pair]:
    terms_dimension, term_building_mode = get_terms_dimension(pair_type.n_terms)

    term_builder = TermBuilder(terms_dimension, term_building_mode)
    terms = list(term_builder.get_terms(identifiers))

    return Sampler.get_pairs(terms, pair_type)


class UnrestrictedPairGenerationStrategy(PairGenerationStrategy):
    """Generates a set of Unrestricted Pair."""
    def __init__(self, dataset_distribution: DatasetDistribution, identifiers: List[Identifier]):
        super(UnrestrictedPairGenerationStrategy, self).__init__(dataset_distribution, identifiers)

    @log_time
    def get_pairs(self) -> List[Pair]:
        pair_types = self.dataset_distribution.pair_types
        pairs = []

        for pair_type in pair_types:
            pairs.extend(unrestricted_from_type(pair_type, self.identifiers))

        return pairs


@log_time
def generation_strategy_factory(dataset_type: DatasetType, dataset_distribution: DatasetDistribution, file_path: Path = None) -> PairGenerationStrategy:
    if dataset_type is DatasetType.RESTRICTED:
        return RestrictedPairGenerationStrategy(dataset_distribution)

    if file_path is None:
        exit(-1) # todo: gestire eccezione

    identifiers = load_unrestricted_identifiers(file_path)
    return UnrestrictedPairGenerationStrategy(dataset_distribution, identifiers)


@log_time
def generate_strings(pairs: List[Pair]) -> List[Pair]:
    for pair in pairs:
        pair.update_phrase()
        pair.update_formula()

    return pairs


class DatasetGenerator:
    """Generates a Dataset of any kind: Restricted or Unrestricted."""
    def __init__(self, dataset_distribution: DatasetDistribution, dataset_type: DatasetType, generation_strategy: PairGenerationStrategy):
        self.dataset_distribution = dataset_distribution
        self.dataset_type = dataset_type
        self.generation_strategy = generation_strategy

    @log_time
    def generate_dataset(self):
        pairs = self.generation_strategy.get_pairs()

        pairs = generate_strings(pairs)

        # crea dataset
        return Dataset(pairs, self.dataset_type)
