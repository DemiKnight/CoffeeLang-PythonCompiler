

from dataclasses import dataclass
from enum import Enum

# All possible errors
class ErrorType(Enum):
    VAR_NOT_FOUND = ""


@dataclass(order=True)
class SemanticsError:
    lineNumber: int
    ErrorT: ErrorType


