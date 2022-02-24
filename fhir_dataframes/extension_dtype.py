from __future__ import annotations
from typing import Any, Dict, Type, cast
import numpy as np
from tiro_fhir import CodeableConcept
import pandas as pd
from pandas._typing import DtypeObj
from pandas.core.dtypes.dtypes import PandasExtensionDtype, Ordered, Dtype


class CodeableConceptDtypeDtype(type):
    pass


@pd.api.extensions.register_extension_dtype
class CodeableConceptDtype(pd.api.extensions.ExtensionDtype):
    type = CodeableConcept
    name = "CodeableConcept"
    na_value = None

    @classmethod
    def construct_array_type(cls) -> Type[CodeableConcept]:
        return CodeableConceptArray

    @classmethod
    def construct_from_string(cls, string: str) -> CodeableConceptDtype:
        if not isinstance(string, str):
            raise TypeError(
                f"'construct_from_string' expects a string, got {type(string)}"
            )
        if string != cls.name:
            raise TypeError(f"Cannot construct a '{cls.name}' from '{string}'")

        return cls()

    @property
    def _is_boolean(self) -> bool:
        return False

    @property
    def _is_numeric(self) -> bool:
        return False

    def _get_common_dtype(self, dtypes: list[DtypeObj]) -> DtypeObj | None:

        # check if we have all codeableconcept dtype
        if all(isinstance(x, CodeableConceptDtype) for x in dtypes):
            return CodeableConcept

        return None


class CodeableConceptArray(pd.api.extensions.ExtensionDtype):
    """Abstract base class for custom 1-D array types."""

    def __init__(self, values, dtype=None, copy=False):
        """Instantiate the array.
        If you're doing any type coercion in here, you will also need
        that in an overwritten __settiem__ method.
        But, here we coerce the input values into Decimals.
        """
        validated = []
        for value in values:
            if not isinstance(value, CodeableConcept):
                raise TypeError(
                    f"Expected value of type CodeableConcept but received {value}"
                )
            validated.append(value)
        self._data = np.asarray(values, dtype=object)
        self._dtype = CodeableConceptDtype()

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        """Construct a new ExtensionArray from a sequence of scalars."""
        return cls(scalars, dtype=dtype)

    @property
    def ndim(self):
        return 1

    @classmethod
    def _from_factorized(cls, values, original):
        """Reconstruct an ExtensionArray after factorization."""
        return cls(values)

    def __getitem__(self, item):
        """Select a subset of self."""
        return self._data[item]

    def __len__(self) -> int:
        """Length of this array."""
        return len(self._data)

    def _formatter(self, boxed: bool = False):
        return str

    @property
    def nbytes(self):
        """The byte size of the data."""
        return self._itemsize * len(self)

    @property
    def dtype(self):
        """An instance of 'ExtensionDtype'."""
        return self._dtype

    def isna(self):
        """A 1-D array indicating if each value is missing."""
        return np.array([x is None for x in self._data], dtype=bool)

    def __arrow_array__(self, type=None):
        # convert the underlying array values to a pyarrow Array
        import pyarrow

        return pyarrow.array([x.text for x in self._data], type="string")

    def isin(self, values):
        return np.array([x in values for x in self])

    def astype(self, *args, **kwargs):
        return self._data

    def take(self, indexer, allow_fill=False, fill_value=None):
        """Take elements from an array.
        Relies on the take method defined in pandas:
        https://github.com/pandas-dev/pandas/blob/e246c3b05924ac1fe083565a765ce847fcad3d91/pandas/core/algorithms.py#L1483
        """
        from pandas.api.extensions import take

        data = self._data
        if allow_fill and fill_value is None:
            fill_value = self.dtype.na_value

        result = take(data, indexer, fill_value=fill_value, allow_fill=allow_fill)
        return self._from_sequence(result)

    def copy(self):
        """Return a copy of the array."""
        return type(self)(self._data.copy())

    @classmethod
    def _concat_same_type(cls, to_concat):
        """Concatenate multiple arrays."""
        return cls(np.concatenate([x._data for x in to_concat]))
