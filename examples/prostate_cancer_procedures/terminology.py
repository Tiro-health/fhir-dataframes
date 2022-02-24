from tiro_fhir import SCTCoding, Coding, CodeableConcept, SimpleValueSet

TIRO_CS = "https://tiro.health/fhir/sid"
PROSTATECTOMIE = SCTCoding("90470006 |Prostatectomy (procedure)|")
EXCISIE_OP_ABDOMEN = SCTCoding("108189003 |Abdomen excision (procedure)|")

LINKS_ZENUWSPAREND = Coding(
    code="links-zenuwsparend", display="links zenuwsparend", system=TIRO_CS
)
RECHTS_ZENUWSPAREND = Coding(
    code="rechts-zenuwsparend", display="rechts zenuwsparend", system=TIRO_CS
)
NIET_ZENUWSPAREND = Coding(
    code="niet-zenuwsparend", display="rechts zenuwsparend", system=TIRO_CS
)

RALP = SCTCoding(
    "708919000 |Laparoscopic radical prostatectomy using robotic assistance (procedure)|"
)

LYMFADENECTOMIE = SCTCoding("58347006 |Excision of lymph node (procedure)|")

CT_ABDOMEN = SCTCoding("169070004 |Computed tomography of abdomen (procedure)|")
CT_PELVIS = SCTCoding("169071000 |Computed tomography of pelvis (procedure)|")

CT_ABDOMEN_PELVIS = SCTCoding(
    "419394006 |Computed tomography of abdomen and pelvis (procedure)|"
)
EBRT = SCTCoding("33195004 |External beam radiation therapy procedure (procedure)|")

APPENDECTOMIE = SCTCoding("80146002 |Excision of appendix (procedure)|")

ADJUVANTE_RADIOTHERAPIE = SCTCoding(
    "148221000146101 |adjuvante radiotherapie (verrichting)|"
)

PROCEDURE_OP_PROSTAAT = SCTCoding("118877007 |verrichting op prostaat (verrichting)|")

ALL_PROCEDURES = [
    # 0
    CodeableConcept(
        text="ralp met lymfadenectomy, niet zenuwsparend",
        coding=[RALP, LYMFADENECTOMIE, NIET_ZENUWSPAREND],
    ),
    # 1
    CodeableConcept(
        text="prostatectomie links zenuwsparend",
        coding=[PROSTATECTOMIE, LINKS_ZENUWSPAREND],
    ),
    # 2
    CodeableConcept(
        text="apendectomie",
        coding=[
            APPENDECTOMIE,
        ],
    ),
    # 3
    CodeableConcept(text="rarp", coding=[RALP]),
    # 4
    CodeableConcept(text="ebrt van prostaat", coding=[EBRT, PROCEDURE_OP_PROSTAAT]),
    # 5
    CodeableConcept(
        text="adjuvante radiotherapie",
        coding=[ADJUVANTE_RADIOTHERAPIE, PROCEDURE_OP_PROSTAAT],
    ),
    # 6
    CodeableConcept(text="ct van abdomen", coding=[CT_ABDOMEN]),
    # 7
    CodeableConcept(text="ct van abdomen en pelvis", coding=[CT_ABDOMEN, CT_PELVIS]),
]

FILTERS = {
    "Procedure op abdomen": SimpleValueSet(
        RALP,
        LYMFADENECTOMIE,
        PROSTATECTOMIE,
        APPENDECTOMIE,
        CT_ABDOMEN,
        PROCEDURE_OP_PROSTAAT,
    ),
    "Procedure op prostaat": SimpleValueSet(
        RALP, LYMFADENECTOMIE, PROSTATECTOMIE, PROCEDURE_OP_PROSTAAT
    ),
    "Excisie van abdomen": SimpleValueSet(
        RALP, LYMFADENECTOMIE, PROSTATECTOMIE, APPENDECTOMIE
    ),
    "Radiotherapie van prostaat": SimpleValueSet(EBRT, ADJUVANTE_RADIOTHERAPIE),
    "EBRT prostaat": SimpleValueSet(EBRT),
    "Adjuvante radiotherapie": SimpleValueSet(ADJUVANTE_RADIOTHERAPIE),
    "computertomografie": SimpleValueSet(CT_ABDOMEN, CT_PELVIS),
}
