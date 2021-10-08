from __future__ import annotations

from dataclasses import dataclass

from typing import List


@dataclass(order=True)
class SemanticsError:
    lineNumber: int
    message: str

    def errorStr(self) -> str:
        return f"Line {self.lineNumber}: {self.message}"


class Assembler:
    header: List[AssemblyOutput]
    body: List[AssemblyOutput]

    stringCache: List[str]
    dataCache: List[str]

    def __init__(self) -> None:
        self.header = list()
        self.body = list()
        self.stringCache = list()

    def generate(self) -> str:
        output = ""

        headerStr: List[str] = [x.output() for x in self.header]
        bodyStr: List[str] = [x.output() for x in self.body]

        output += "".join(headerStr)
        output += "".join(bodyStr)

        return output


class AssemblyOutput:
    def output(self) -> str:
        return f"{self._outputImpl()}\n"

    def _outputImpl(self) -> str:
        raise NotImplemented

@dataclass
class Segment(AssemblyOutput):
    segment_name: str

    def _outputImpl(self) -> str:
        return f".{self.segment_name}"


@dataclass
class FunctionOutput(AssemblyOutput):
    function_name: str

    def _outputImpl(self) -> str:
        return f'{self.function_name}:'


@dataclass
class Instr(AssemblyOutput):
    opcode: str
    # TODO replace following with better typing
    SIB: str = ""
    modR: str = ""
    displacement: str = ""
    immediate: str = ""

    def _outputImpl(self) -> str:
        immediate_output = "" if self.immediate == "" else f", {self.immediate}"

        return f"{self.opcode} ".join([self.displacement, immediate_output])