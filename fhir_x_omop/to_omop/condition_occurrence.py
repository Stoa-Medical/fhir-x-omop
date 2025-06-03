from fhir.resources.condition import Condition
from omop_pydantic import ConditionOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

condition_occurrence_mapping = DataMapping({
    "condition_occurrence_id": p.get("id") >> p.int(),
    "person_id": p.get("subject.reference | split(@, '/')[1]") >> p.int(),
    "condition_concept_id": 0,  # Would need concept mapping in production
    "condition_start_date": p.get("onsetDateTime | recordedDate | split(@, 'T')[0]"),
    "condition_start_datetime": p.get("onsetDateTime | recordedDate"),
    "condition_end_date": p.get("abatementDateTime | split(@, 'T')[0]"),
    "condition_end_datetime": p.get("abatementDateTime"),
    "condition_type_concept_id": p.case(p.get("category[0].coding[0].code"), {
        "encounter-diagnosis": 32817,
        "problem-list-item": 32818,
        "health-concern": 32819,
        "default": 32817
    }),
    "condition_status_concept_id": p.case(p.get("clinicalStatus.coding[0].code"), {
        "active": 32893,
        "resolved": 32897,
        "inactive": 32896,
        "default": 32893
    }),
    "stop_reason": p.get("note[0].text"),
    "provider_id": p.get("recorder.reference | split(@, '/')[1]") >> p.int(),
    "visit_occurrence_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "visit_detail_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "condition_source_value": p.get("code.coding[0].code"),
    "condition_source_concept_id": 0,
    "condition_status_source_value": p.get("clinicalStatus.coding[0].code"),
})

to_omop_condition_occurrence = Piper(source=Condition, target=ConditionOccurrence, mapping=condition_occurrence_mapping)