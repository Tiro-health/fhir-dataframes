# FHIR DataFrames (coming soon)
DataFrames are the bread and butter of every datascientist. This packages makes analysing FHIR resources as easy as manipulating Pandas DataFrames.

## ⭐ Highlights ⭐

- Convenient way to map FHIR resources with deeply nested structures to a flat Pandas DataFrame.
```python
df = FHIRStore["Observation"]["code", "value", "subject.reference"]
```
- Easy pythonic way to handle CodeableConcepts, Codings and ValueSets (FHIR Terminology)

```python
```
**Stay tuned and [watch this repo](https://github.com/Tiro-health/fhir-dataframes/subscription).**
