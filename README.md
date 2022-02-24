# FHIR DataFrames (coming soon)
DataFrames are the bread and butter of every datascientist. This packages makes analysing FHIR resources as easy as manipulating Pandas DataFrames.

## ⭐ Highlights ⭐

- Convenient way to map FHIR resources with deeply nested structures to a flat Pandas DataFrame.
```python
df = FHIRStore["Observation"]["code", "value", "subject.reference"]
```
- Easy pythonic way to handle CodeableConcepts, Codings and ValueSets (FHIR Terminology)

```python
code = SCTCoding("90470006 |Prostatectomy (procedure)|") # create a coding based on the inline SNOMED-CT format
vs = code.descendants()
df = df[df["code"].code.isin(vs)] # filter procedures on code that subsume prostatectomy
```
**Stay tuned and [watch this repo](https://github.com/Tiro-health/fhir-dataframes/subscription).**
