import random
from typing import List

from nl2ltl_dataset_generator.base.data_model import PairTerm, Identifier, LogicalOperator

phrase_templates = {
    "absence_global": [
        "it is never the case that Term1",
        "at no time Term1",
        "it never happens that Term1",
        "never, Term1",
        "it should not happen that Term1",
        "it will not happen that Term1",
        "under no condition Term1",
        "under no circumstances Term1",
        "absolutely never, Term1",
    ],
    "existence_global": [
        "at some point in time Term1",
        "at some point Term1",
        "sooner or later Term1",
        "eventually, Term1",
        "finally, Term1",
        "it will happen that Term1",
        "at a certain moment Term1",
        "in the future Term1",
        "it is going to happen that Term1",
    ],
    "universal_global": [
        "it is always the case that Term1",
        "at any time Term1",
        "in any case Term1",
        "always, Term1",
        "it is always true that Term1",
        "all the time Term1",
        "every time Term1",
        "forever, Term1",
        "eternally, Term1",
    ],
    "response_global": [
        "whenever Term1 then Term2",
        "if Term1 then Term2",
        "after Term1, Term2",
        "every time Term1 then Term2",
        "Term2 after Term1",
        "as Term1, Term2",
        "always when Term1 then Term2",
    ],
    "absence_after": [
        "whenever Term1 then Term2",
        "if Term1 then Term2",
        "after Term1, Term2",
        "every time Term1 then Term2",
        "Term2 after Term1",
        "always Term1 implies that Term2",
    ],
    "existence_after": [
        "Term1 and, Term2 afterwards",
        "first, Term1, and then, Term2",
    ],
    "universal_after": [
        "whenever Term1 then Term2",
        "if Term1 then Term2",
        "after Term1, Term2",
        "every time Term1 then Term2",
        "Term2 after Term1",
    ],
    "response_after": [
        "Term1 and, as a consequence, Term2",
        "each time Term1 then Term2",
        "when Term1 then Term2 afterwards",
        "Term1 implies that Term2",
        "Term1 involves that Term2",
    ],
}


def or_logical_operator_phrase_template(identifier1: Identifier, identifier2: Identifier,
                                        identifier3: Identifier = None) -> str:
    two_terms = [
        f"either {identifier1.get_phrase_string()} or {identifier2.get_phrase_string()}",
        f"{identifier1.get_phrase_string()} or {identifier2.get_phrase_string()}",
    ]
    three_terms = [
        f"either {identifier1.get_phrase_string()}, {identifier2.get_phrase_string()} or {identifier3.get_phrase_string()}",
        f"{identifier1.get_phrase_string()} or {identifier2.get_phrase_string()} or {identifier3.get_phrase_string()}",
    ] if identifier3 is not None else []

    return random.choice(two_terms) if identifier3 is None else random.choice(three_terms)


def and_logical_operator_phrase_template(identifier1: Identifier, identifier2: Identifier,
                                         identifier3: Identifier = None) -> str:
    two_terms = [
        f"both {identifier1.get_phrase_string()} and {identifier2.get_phrase_string()}",
        f"{identifier1.get_phrase_string()} and {identifier2.get_phrase_string()}",
    ]
    three_terms = [
        f"{identifier1.get_phrase_string()}, {identifier2.get_phrase_string()} and {identifier3.get_phrase_string()}",
        f"{identifier1.get_phrase_string()} and together {identifier2.get_phrase_string()} and {identifier3.get_phrase_string()}",
        f"{identifier1.get_phrase_string()} and, at the same time, {identifier2.get_phrase_string()} and {identifier3.get_phrase_string()}",
    ] if identifier3 is not None else []

    return random.choice(two_terms) if identifier3 is None else random.choice(three_terms)


def term_phrase_template(term: PairTerm) -> str:
    if term.logical_operator is None:
        return term.identifiers[0].get_phrase_string()

    if term.logical_operator == LogicalOperator.OR:
        return or_logical_operator_phrase_template(*term.identifiers)
    elif term.logical_operator == LogicalOperator.AND:
        return and_logical_operator_phrase_template(*term.identifiers)


def absence_global_phrase_template(terms: List[PairTerm]):
    accepted_terms = 1
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["absence_global"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0]))


def existence_global_phrase_template(terms: List[PairTerm]):
    accepted_terms = 1
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["existence_global"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0]))


def universal_global_phrase_template(terms: List[PairTerm]):
    accepted_terms = 1
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["universal_global"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0]))


def response_global_phrase_template(terms: List[PairTerm]):
    accepted_terms = 2
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["response_global"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0])).replace("Term2", existence_global_phrase_template([terms[1]]))


def absence_after_phrase_template(terms: List[PairTerm]):
    accepted_terms = 2
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["absence_after"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0])).replace("Term2", absence_global_phrase_template([terms[1]]))


def existence_after_phrase_template(terms: List[PairTerm]):
    accepted_terms = 2
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["existence_after"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", existence_global_phrase_template([terms[0]])).replace("Term2", existence_global_phrase_template([terms[1]]))


def response_after_phrase_template(terms: List[PairTerm]):
    accepted_terms = 3
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["response_after"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0])).replace("Term2",
                                                                             response_global_phrase_template([terms[1], terms[2]]))


def universal_after_phrase_template(terms: List[PairTerm]):
    accepted_terms = 2
    if len(terms) != accepted_terms:
        raise Exception(f"Too many terms for 'absence_global' formula, got {len(terms)} expected {accepted_terms}")

    templates = phrase_templates["universal_after"]

    template = random.sample(templates, 1)[0]

    return template.replace("Term1", term_phrase_template(terms[0])).replace("Term2", universal_global_phrase_template([terms[1]]))
