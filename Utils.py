from dataclasses import dataclass
from enum import Enum

# All possible errors
from typing import List

# All possible errors and associated error message. Error message should include
# placeholder for replacement. All possible placeholders:
# - `{identifier}` - REQUIRED - name/identifier for entity
# - `{type_mismatched}` - SPECIFIC - The incorrect type evaluated
# - `{type_required}` - SPECIFIC - The required type.
class ErrorType(Enum):
    # Variable assignment/use errors
    VAR_NOT_FOUND = "Variable {identifier} not defined in scope"
    VAR_ALREADY_DEFINED = "Variable {identifier} already defined"
    VAR_PARAM_ALREADY_DEFINED = "Parameter {identifier} already defined"
    VAR_ASSIGN_TYPE_MISMATCH = "Variable {identifier} requires {type_required} but was assigned {type_mismatched}"

    # Method errors
    METHOD_ALREADY_DEFINED = "Method {identifier} already defined"
    METHOD_NOT_FOUND = "Method {identifier} used before declaration"
    METHOD_SIGNATURE_TYPE_MISMATCH_PARAMETERS = "Call to method {identifier} has incorrect argument type(s)"
    METHOD_SIGNATURE_TYPE_MISMATCH_RETURN_VALUE = "Method {identifier} called but return type {type_required}"
    METHOD_SIGNATURE_ARGUMENT_COUNT = "Call to method {identifier} has incorrect number of parameters"
    METHOD_VOID_RETURNING_VALUE = "Method {identifier} declared void but is returning a value"
    METHOD_MISSING_RETURN = "Method {identifier} missing return"
    METHOD_MISSING_RETURN_NON_EXHAUSTIVE = "Method {identifier} missing return on all branches/paths"
    METHOD_RETURN_TYPE_MISMATCH = "Method {identifier} expecting {type_required} return type but got instead {" \
                                  "type_mismatched} "

    # Arithmetic/Logic/Expression errors
    EXPRESSION_USING_VOID_METHOD = "Method {identifier} returns void but was used within an expression"
    EXPRESSION_CONDITION_TYPE_MISMATCH = "If condition should be bool not {type_mismatched}"
    EXPRESSION_CONDITION_TYPE_MISMATCH_NOT = "{type_mismatched} used with a logical NOT"

    # MISC.
    MAIN_METHOD_RETURN_TYPE_MISMATCH = "Main method must return int but instead got {type_mismatched}"
    IMPORT_DUPLICATE = "Method {identifier} imported multiple times"

    # Arrays
    ARRAY_SIZE_ZERO_OR_LESS = "Array {identifier} declared with 0 or less capacity"

    # Weird/impossible state errors
    UNKNOWN_LITERAL_TYPE = "Unknown literal type {identifier}"


@dataclass(order=True)
class SemanticsError:
    lineNumber: int
    identifier: str
    ErrorT: ErrorType
    type_mismatched: str = None
    type_required: str = None


def print_semantic_errors(errors: List[SemanticsError]) -> None:
    for error in errors:
        type_mismatch_str = error.type_mismatched if error.type_mismatched is not None else ""
        type_required_str = error.type_required if error.type_required is not None else ""

        formatted_str: str = error.ErrorT.value.format(
            identifier=error.identifier, type_mismatched=type_mismatch_str, type_required=type_required_str)


        print(f"\nERROR: {formatted_str}! See line {error.lineNumber}")
