from __future__ import annotations
from itertools import tee
from typing import Any, Dict, Iterable, Optional, Sequence, Union
import pandas as pd
from fhirkit import Resource


class LocalFHIRStore:
    def __init__(self, resources: Iterable[Resource] = []):
        self._resources: Iterable[Resource] = resources

    @property
    def resources(self):
        self._resources, result = tee(self._resources)
        return result

    def to_pandas(self, keys: Optional[Sequence[str]] = None):
        records = [resource.to_record(keys) for resource in self.resources]
        df = pd.DataFrame.from_dict(records)
        df.columns = [".".join(map(str, c)) for c in df.columns.tolist()]
        return df

    def __call__(self, *args, **kwds: Dict[str, Any]) -> LocalFHIRStore:
        if "resourceType" in kwds:
            return self.get_by_resource_type(kwds["resourceType"])
        return self

    def __getitem__(self, key: Optional[Union[str, Sequence[str]]]):
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
