from dataclasses import dataclass



@dataclass(order=True)
class SemanticsError:
    lineNumber: int
    message: str

    def errorStr(self) -> str:
        return f"Line {self.lineNumber}: {self.message}"


@dataclass
class Instr:
    opcode: str
    modR: str
    SIB: str
    displacement: str
    immediate: str
