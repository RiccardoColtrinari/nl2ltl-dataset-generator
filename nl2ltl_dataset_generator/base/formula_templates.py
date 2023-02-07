from nl2ltl_dataset_generator.base.data_model import PairTerm


def term_formula_template(term: PairTerm) -> str:
    if term.logical_operator is None:
        return term.identifiers[0].get_formula_string()

    return f" {term.logical_operator.value} ".join([identifier.get_formula_string() for identifier in term.identifiers])


def existence_global_formula_template(term1: PairTerm):
    return f"F( {term_formula_template(term1)} )"


def universal_global_formula_template(term1: PairTerm):
    return f"G( {term_formula_template(term1)} )"


def absence_global_formula_template(term1: PairTerm):
    return f"G(!( {term_formula_template(term1)} ))"


def response_global_formula_template(term1: PairTerm, term2: PairTerm):
    return f"G(( {term_formula_template(term1)} ) -> {existence_global_formula_template(term2)})"


def existence_after_formula_template(term1: PairTerm, term2: PairTerm):
    return f"{absence_global_formula_template(term1)} | F(( {term_formula_template(term1)} ) & {existence_global_formula_template(term2)})"


def universal_after_formula_template(term1: PairTerm, term2: PairTerm):
    return f"G(( {term_formula_template(term1)} ) -> {universal_global_formula_template(term2)})"


def absence_after_formula_template(term1: PairTerm, term2: PairTerm):
    return f"G(( {term_formula_template(term1)} ) -> {absence_global_formula_template(term2)})"


def response_after_formula_template(term1: PairTerm, term2: PairTerm, term3: PairTerm):
    return f"G(( {term_formula_template(term1)} ) -> {response_global_formula_template(term2, term3)})"
