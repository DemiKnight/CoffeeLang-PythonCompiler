from enum import Enum
from typing import List

class Reg(Enum):
    rbp = "%rbp"
    rsp = "%rsp"

class OpCodes(Enum):
    MoveQ = "movq"
    Push = "push"
    MovL = "movl"
    Pop = "pop"
    Popq = "popq"
    Ret = "ret"

def create_method(method_id: str, return_type: str, parameters: List[str]) -> str:
    return (
        f"{method_id}:\n"
    )

def asm(code: OpCodes, *parameters) -> str:
    parameterStr = ""

    # for index in parameters:
    #     parameterStr

    return f"{code.value} "
