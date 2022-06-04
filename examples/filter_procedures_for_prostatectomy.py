# "resourceType": "Observation", "meta": {"source": "traject.csv#R0", "security": [], "tag": []}, "date": "2020-09-10T00:00:00", "code": "Gleason Score", "encounter": {"resourceType": "Encounter", "meta": {"source": "traject.csv#R0", "security": [], "tag": []}, "date": "2020-09-22T12:45:00", "subject": {"resourceType": "Patient", "meta": {"source": "traject.csv#R0", "security": [], "tag": []}, "eadnr": "542658ca418958e1a818961535bca9ce", "birthDate": "1948-01-01T00:00:00", "gender": "M"}, "status": "finished", "type": "Patient condition assessed", "class": "AMB"}, "performer": {"resourceType": "Practitioner", "meta": {"source": "traject.csv#R0", "security": [], "tag": []}, "arts": "wevera0", "afdeling": "URO", "supervisor": "wevera0"}, "subject": {"resourceType": "Patient", "meta": {"source": "traject.csv#R0", "security": [], "tag": []}, "eadnr": "542658ca418958e1a818961535bca9ce", "birthDate": "1948-01-01T00:00:00", "gender": "M"}, "status": "final", "valueString": "4+5", "method": "277590007 |Imaging guided biopsy (procedure)|"}
#%%
import os

os.chdir("..")
# %%
from datetime import datetime
from fhirkit import (
    Observation,
    Procedure,
    SCTConcept,
    SCTCoding,
    Reference,
    SCTFHIRTerminologyServer,
    SimpleValueSet,
)
from fhir_dataframes.store import LocalFHIRStore
from fhir_dataframes.extension_dtype import CodeableConceptDtype

gs_observable = SCTConcept("372278000 |Gleason score|")
gp_observable = (
    SCTConcept("384994009 |Primary Gleason pattern|"),
    SCTConcept("384995005 |Secondary Gleason pattern|"),
)
gs_findings = [
    SCTConcept("18430005 |Gleason grade score 4|"),
    SCTConcept("46677009 |Gleason grade score 3|"),
    SCTConcept("84556003 |Gleason grade score 6|"),
]
gp_findings = [
    (
        SCTConcept("369771005 |Gleason Pattern 2|"),
        SCTConcept("369771005 |Gleason Pattern 2|"),
    ),
    (
        SCTConcept("369770006 |Gleason Pattern 1|"),
        SCTConcept("369771005 |Gleason Pattern 2|"),
    ),
    (
        SCTConcept("369772003 |Gleason Pattern 3|"),
        SCTConcept("369772003 |Gleason Pattern 3|"),
    ),
]
dates = [datetime(2020, 1, 4), datetime(2018, 4, 28), datetime(2019, 3, 10)]
observations = [
    Observation(
        code=gs_observable,
        value=finding,
        effective=d,
        component=[
            {"code": obs, "value": find}
            for (obs, find) in zip(gp_observable, comp_findings)
        ],
    )
    for finding, comp_findings, d in zip(gs_findings, gp_findings, dates)
]

# %%
subject = Reference(reference="test-patient")
procedures = [
    Procedure(
        code=SCTConcept(
            "26294005+58347006 |Radical prostatectomy with lymphadenectomy|"
        ),
        performed=datetime(2012, 11, 4),
        subject=subject,
    ),
    Procedure(
        code=SCTConcept("708919000 |RARP|"),
        performed=datetime(2015, 8, 10),
        subject=subject,
    ),
    Procedure(
        code=SCTConcept("90470006 |Prostatectomy|"),
        performed=datetime(2020, 4, 25),
        subject=subject,
    ),
    Procedure(
        code=SCTConcept("176258007 |Open prostatectomy|"),
        performed=datetime(2021, 7, 18),
        subject=subject,
    ),
]
# %%
store = LocalFHIRStore(procedures + observations)
snowstorm = SCTFHIRTerminologyServer("https://snowstorm-aovarw23xa-uc.a.run.app/fhir")
prostatectomy = SCTCoding("90470006 |Prostatectomy (procedure)|")
valueset_is_a_prostatectomy = prostatectomy.descendants(fhir_server=snowstorm)

# %%

df_procedures = store(resourceType="Procedure")["code", "performed"]
df_observations = store(resourceType="Observation").to_pandas()


#%%
df["code"].astype("CodeableConcept")
# %%
df["code"].code.isin(SimpleValueSet([SCTCoding("708919000 |RARP|")]))


# %%
