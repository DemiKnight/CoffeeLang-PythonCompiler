from dataclasses import dataclass
from enum import Enum

# All possible errors
from typing import List


class ErrorType(Enum):
    VAR_NOT_FOUND = "Variable {identifier} not found"
    VAR_ALREADY_DEFINED = "Variable {identifier} already defined"
    VAR_PARAM_ALREADY_DEFINED = "Parameter {identifier} already defined"
    METHOD_ALREADY_DEFINED = "Method {identifier} already defined!"


@dataclass(order=True)
class SemanticsError:
    lineNumber: int
    identifier: str
    ErrorT: ErrorType


def printSemanticErrors(errors: List[SemanticsError]) -> None:
    for error in errors:
        formattedString = error.ErrorT.value.format(identifier=error.identifier)
        print(f"\n{formattedString}! See {error.lineNumber}")
