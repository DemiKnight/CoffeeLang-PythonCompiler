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
    VAR_NOT_FOUND = "Variable {identifier} not defined in scope"
    VAR_ALREADY_DEFINED = "Variable {identifier} already defined"
    VAR_PARAM_ALREADY_DEFINED = "Parameter {identifier} already defined"
    VAR_ASSIGN_TYPE_MISMATCH = "Variable {identifier} requires {type_required} but was assigned {type_mismatched}"
    METHOD_ALREADY_DEFINED = "Method {identifier} already defined!"

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


        print(f"\n{formatted_str}! See line {error.lineNumber}")
