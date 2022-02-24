from tiro_fhir import Procedure, Reference, SimpleValueSet
from datetime import datetime
import streamlit as st
import pandas as pd

from fhir_dataframes.store import LocalFHIRStore
from fhir_dataframes import extension_dtype
from examples.prostate_cancer_procedures.terminology import ALL_PROCEDURES, FILTERS

procedure_list = [
    Procedure(
        performedDateTime=datetime(2018, 2, 10),
        code=ALL_PROCEDURES[0],
        subject=Reference(id="patient-1"),
    ),
    Procedure(
        performedDateTime=datetime(2013, 8, 18),
        code=ALL_PROCEDURES[1],
        subject=Reference(id="patient-2"),
    ),
    Procedure(
        performedDateTime=datetime(2011, 11, 28),
        code=ALL_PROCEDURES[2],
        subject=Reference(id="patient-1"),
    ),
    Procedure(
        performedDateTime=datetime(2011, 10, 2),
        code=ALL_PROCEDURES[3],
        subject=Reference(id="patient-3"),
    ),
    Procedure(
        performedDateTime=datetime(2013, 9, 8),
        code=ALL_PROCEDURES[4],
        subject=Reference(id="patient-4"),
    ),
    Procedure(
        performedDateTime=datetime(2014, 3, 30),
        code=ALL_PROCEDURES[5],
        subject=Reference(id="patient-5"),
    ),
    Procedure(
        performedDateTime=datetime(2012, 9, 7),
        code=ALL_PROCEDURES[6],
        subject=Reference(id="patient-4"),
    ),
    Procedure(
        performedDateTime=datetime(2011, 7, 12),
        code=ALL_PROCEDURES[7],
        subject=Reference(id="patient-5"),
    ),
]

store = LocalFHIRStore(procedure_list)

df = store.Procedure.to_pandas()
df["code"] = df["code"].astype("CodeableConcept")
df["subject"] = df["subject"].apply(lambda x: x.id)
st.set_page_config(layout="wide")
st.title("Demo analyse klinsiche data")


st.header("Vergelijking data collectie klassiek versus Tiro-alternatief")

col1, col2 = st.columns(2)
col1.text("Data collected with classical forms:")
col1.dataframe(
    pd.DataFrame.from_dict(
        [
            {
                "subject": "patient-1",
                "prostatectomie": True,
                "robot-geassisteerd": True,
                "zenuwsparend": "niet",
                "lymfadenectomie": True,
                "rp_datum": "2018-02-10T00:00:00",
                "voorgeschiedenis_ingreep_1": "appendectomie",
                "voorgeschiedenis_ingreep_1_datum": "2011-11-28T00:00:00",
            },
            {
                "subject": "patient-2",
                "prostatectomie": True,
                "robot-geassisteerd": False,
                "zenuwsparend": "links",
                "operatie_datum": "2013-08-18T00:00:00",
            },
            {
                "subject": "patient-3",
                "prostatectomie": True,
                "robot-geassisteerd": True,
                "lymfadenectomie": False,
                "operatie_datum": "2011-10-02T00:00:00",
            },
            {
                "subject": "patient-4",
                "radiotherapie": True,
                "ebrt": True,
                "radiotherapie_datum": "2013-09-08T00:00:00",
                "ct": True,
                "ct_datum": "2012-09-07T00:00:00",
            },
            {
                "subject": "patient-5",
                "radiotherapie": True,
                "adjuvante radiotherapie": True,
                "radiotherapie_datum": "2014-03-30T00:00:00",
                "ct": True,
                "ct_datum": "2011-07-12T00:00:00",
            },
        ]
    )
)

col2.text("All data in tiro format:")
col2.dataframe(df)

st.markdown("------")

st.header("Filter patienten")
vs_keys = st.multiselect("Filter procedure", FILTERS.keys())
for vs_key in vs_keys:
    df = df[df["code"].code.isin(FILTERS[vs_key])]
st.text("Filter result")

all_codes = []

# todo: df["code"].code.unique()

all_codes.extend(df["code"].code.unique())
clicked = st.button(
    "Add new filter",
)
if clicked:
    st.session_state["number_of_filters"] += 1

if "number_of_filters" not in st.session_state:
    st.session_state["number_of_filters"] = 1

resulting_codes = []
for i in range(st.session_state["number_of_filters"]):
    resulting_codes = st.multiselect(
        f"Filter on codes: ", all_codes, format_func=str, key="filter_" + str(i)
    )


vs = SimpleValueSet(*resulting_codes)
st.dataframe(df[df["code"].code.isin(vs)])

st.dataframe(df, width=1000)
st.write("Unieke patienten na filteren: ", df["subject"].unique().tolist())
