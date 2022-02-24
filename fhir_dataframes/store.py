from __future__ import annotations
from itertools import tee
from typing import Iterable, Optional, Sequence, Union
import pandas as pd
from tiro_fhir import Resource
from fhir_dataframes import valueset


class LocalFHIRStore:
    def __init__(self, resources: Iterable[Resource] = []):
        self._resources: Iterable[Resource] = resources

    @property
    def resources(self):
        self._resources, result = tee(self._resources)
        return result

    def to_pandas(self, keys: Optional[Sequence[str]] = None):
        records = [resource.record(keys) for resource in self.resources]
        return pd.DataFrame(records)

    def __getitem__(self, key: Union[str, Sequence[str]]):
        if isinstance(key, str):
            return self.to_pandas([key])
        else:
            return self.to_pandas(key)

    def get_by_resource_type(self, resource_type: str) -> LocalFHIRStore:
        return LocalFHIRStore(
            resources=filter(lambda r: r.resourceType == resource_type, self.resources)
        )

    def _repr_html_(self) -> str:
        return pd.Series(self.resources).to_frame(name="resource")._repr_html_()

    @property
    def Observation(self):
        return self.get_by_resource_type("Observation")

    @property
    def Procedure(self):
        return self.get_by_resource_type("Procedure")

    @property
    def Condition(self):
        return self.get_by_resource_type("Condition")
