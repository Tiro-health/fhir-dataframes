from __future__ import annotations
from typing import Generic, Sequence, Type, TypeVar


class FHIRPath:
    def __init__(self, path: Sequence[FHIRPath], field: str) -> None:
        self._field = field
        self._next_field = None
        self._path = path

    @property
    def current_path(self):
        return (*self._path, self)

    def __str__(self) -> str:
        if len(self._path):
            return str(self._path[-1]) + self._field
        else:
            return self._field


class String(FHIRPath):
    pass


class Integer(FHIRPath):
    pass


class Coding(FHIRPath):
    @property
    def display(self):
        self._next_field = String(self.current_path, ".display")
        return self._next_field


T = TypeVar("T", FHIRPath)


class Array(FHIRPath, Generic[T]):
    def __init__(
        self, element_type: Type[T], path: Sequence[FHIRPath], field: str
    ) -> None:
        self._element_type: T = element_type
        self._index = None
        self._agg = None
        super().__init__(path, field)

    def __getitem__(self, index) -> T:
        self._index = index
        index_str = f"[{index}]"
        self._next_field = self._element_type(self.current_path, index_str)
        assert isinstance(
            index, int
        ), f"Index value must be an integer number but received {index}"
        index_str = f"[{index}]"
        return self._next_field

    def first(self) -> T:
        self._index = 0
        self._next_field = self._element_type(self.current_path, ".first()")
        return self._next_field

    def last(self) -> T:
        self._index = -1
        self._next_field = self._element_type(self.current_path, ".last()")
        return self._next_field

    def count(self) -> Integer:
        self._agg = "count"
        self._next_field = self._element_type(self.current_path, ".count()")
        return self._next_field

    def __str__(self) -> str:
        if len(self._path):
            return str(self._path[-1]) + self._field

        raise RuntimeError("An array should be a root path")


class CodeableConcept(FHIRPath):
    @property
    def text(self):
        return String(self.current_path, ".text")

    @property
    def coding(self) -> Array[Coding]:
        return Array(Coding, self.current_path, ".coding")


class Procedure(FHIRPath):
    @property
    def code(self) -> CodeableConcept:
        return CodeableConcept(self.current_path, ".code")


if __name__ == "__main__":

    Procedure = Procedure([], "Procedure")
