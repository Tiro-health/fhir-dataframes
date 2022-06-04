import numpy as np
import pandas as pd
from fhirkit import ValueSet


@pd.api.extensions.register_series_accessor("code")
class CodeOperations:
    def __init__(self, pandas_obj):
        self._obj: pd.Series = pandas_obj

    def isin(self, vs: ValueSet):
        return self._obj.apply(lambda c: c in vs).astype("bool")

    def unique(self):
        flattened = []
        for i, x in self._obj.iteritems():
            flattened.extend(x.coding)
        return np.array(flattened)
