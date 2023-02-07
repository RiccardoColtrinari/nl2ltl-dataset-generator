import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Callable

import numpy as np

from nl2ltl_dataset_generator.base.log import log_time


class DatasetType(Enum):
    RESTRICTED = 0
    UNRESTRICTED = 1

    @staticmethod
    def names():
        return [e.name for e in DatasetType]


class LogicalOperator(Enum):
    AND = '&'
    OR = '|'


class Pattern(Enum):
    ABSENCE = 0
    UNIVERSAL = 1
    RESPONSE = 2
    EXISTENCE = 3

    def __str__(self):
        return self.name.lower()


class Scope(Enum):
    GLOBAL = 0
    AFTER = 1

    def __str__(self):
        return self.name.lower()

@dataclass
class PhraseTemplate:
    phrase_template: str


@dataclass
class FormulaTemplate:
    def __init__(self):
        self._fn_list = []
        self._is_empty = True

    def append_string(self, string: str):
        def string_function():
            return string

        self._fn_list.append(string_function)

    def append_term_by_index(self, term_index):
        def term_function(terms):
            return terms[term_index]

    def get_string(self, terms):
        final_string = ""
        for fn in self._fn_list:
            final_string = final_string + " " + fn(terms)


@dataclass
class PairTypeDistribution:
    old_value: int
    percentage: float = None
    new_value: int = None


@dataclass
class PairType:
    pattern: Pattern
    scope: Scope
    n_terms: int
    phrase_templates: Callable = None  # todo: remove None
    formula_template: Callable = None  # todo: remove None
    distribution: PairTypeDistribution = None


@dataclass
class Identifier(ABC):
    pass

    @abstractmethod
    def get_phrase_string(self):
        pass

    @abstractmethod
    def get_formula_string(self):
        pass


@dataclass
class UnrestrictedIdentifier(Identifier):
    determiners: List[str]
    noun: str
    verb: List[str]
    aux: List[str] = None

    @log_time
    def get_phrase_string(self):
        determiner = random.choice(self.determiners)
        formula_action = ' '.join(self.aux + self.verb) if self.aux is not None else ' '.join(self.verb)
        formula_action = formula_action.strip()
        return f"{determiner} {self.noun} {formula_action}"

    @log_time
    def get_formula_string(self):
        formula_action = '_'.join(self.aux + self.verb) if self.aux is not None else '_'.join(self.verb)
        return f"{self.noun}_{formula_action}"


@dataclass
class RestrictedIdentifier(Identifier):
    determiners: List[str]
    random_identifier: str

    @log_time
    def get_phrase_string(self):
        return self.random_identifier

    @log_time
    def get_formula_string(self):
        return self.random_identifier


@dataclass
class TypesDistribution:
    pair_types_distribution: List[PairTypeDistribution]


@dataclass
class PairTerm:
    identifiers: List[Identifier]
    logical_operator: LogicalOperator = None

    def __len__(self):
        return len(self.identifiers)


@dataclass
class Pair:
    terms: List[PairTerm]
    pair_type: PairType
    phrase: str = None
    formula: str = None

    @log_time
    def update_phrase(self):
        self.phrase = self.pair_type.phrase_templates(self.terms)

    @log_time
    def update_formula(self):
        self.formula = self.pair_type.formula_template(*self.terms)


class DatasetDistribution:

    @log_time
    def __init__(self, n_samples: int, pair_types: List[PairType]):
        self.n_samples = n_samples
        self.pair_types = pair_types
        self.old_values_total = sum(pair_type.distribution.old_value for pair_type in self.pair_types)

    def _calculate_new_info(self, pair_type_distribution: PairTypeDistribution):
        pair_type_distribution.percentage = pair_type_distribution.old_value / self.old_values_total
        pair_type_distribution.new_value = int(np.around(self.n_samples * pair_type_distribution.percentage))

    def update_info(self) -> None:
        remaining_samples = self.n_samples

        for pair_type in self.pair_types[:-1]:
            self._calculate_new_info(pair_type.distribution)
            remaining_samples -= pair_type.distribution.new_value

        self.pair_types[-1].distribution.percentage = self.pair_types[-1].distribution.old_value / self.old_values_total
        self.pair_types[-1].distribution.new_value = remaining_samples


@dataclass
class Dataset:
    pairs: List[Pair]
    dataset_type: DatasetType
    types_distribution: TypesDistribution = None
