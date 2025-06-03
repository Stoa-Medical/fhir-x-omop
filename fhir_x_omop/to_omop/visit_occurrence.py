from fhir.resources.encounter import Encounter
from omop_pydantic import VisitOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

visit_occurrence_mapping = DataMapping({
    "visit_occurrence_id": p.get("id") >> p.int(),
    "person_id": p.get("subject.reference | split(@, '/')[1]") >> p.int(),
    "visit_concept_id": p.case(p.get("class.code"), {
        "IMP": 9201,      # Inpatient Visit
        "AMB": 9202,      # Outpatient Visit  
        "EMER": 9203,     # Emergency Room Visit
        "HH": 581379,     # Home Health
        "VR": 32036,      # Virtual
        "default": 9202   # Default to Outpatient
    }),
    "visit_start_date": p.get("period.start | split(@, 'T')[0]"),
    "visit_start_datetime": p.get("period.start"),
    "visit_end_date": p.get("period.end | split(@, 'T')[0]"),
    "visit_end_datetime": p.get("period.end"),
    "visit_type_concept_id": 44818518,  # Visit derived from EHR
    "provider_id": p.get("participant[?type[0].coding[0].code=='ATND'].individual.reference | [0] | split(@, '/')[1]") >> p.int(),
    "care_site_id": p.get("serviceProvider.reference | split(@, '/')[1]") >> p.int(),
    "visit_source_value": p.get("type[0].coding[0].code"),
    "visit_source_concept_id": 0,
    "admitted_from_concept_id": 0,
    "admitted_from_source_value": p.get("hospitalization.admitSource.coding[0].code"),
    "discharge_to_concept_id": p.case(p.get("hospitalization.dischargeDisposition.coding[0].code"), {
        "home": 8536,
        "snf": 8676,
        "rehab": 8615,
        "exp": 4216643,
        "default": 0
    }),
    "discharge_to_source_value": p.get("hospitalization.dischargeDisposition.coding[0].display"),
    "preceding_visit_occurrence_id": None,
})

to_omop_visit_occurrence = Piper(source=Encounter, target=VisitOccurrence, mapping=visit_occurrence_mapping)