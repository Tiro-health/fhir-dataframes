import numpy as np
import pandas as pd
from fhirkit import ValueSet


@pd.api.extensions.register_series_accessor("code")
class ResourceOperations:
    def __init__(self) -> None:
        pass

    def sequence(self) -> None:
        pass
