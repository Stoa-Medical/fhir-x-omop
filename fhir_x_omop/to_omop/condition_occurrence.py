from fhir.resources.condition import Condition
from omop_pydantic import ConditionOccurrence

from chidian import DataMapping, Mapper
import chidian.partials as p

def get_first_existing(src, paths):
    for path in paths:
        value = p.get(path)(src)
        if value:
            return value
    return None

condition_occurrence_mapper = Mapper(
    lambda src: {
        "condition_occurrence_id": (p.get("id") | p.int())(src),
        "person_id": p.get("subject.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "condition_concept_id": 0,  # Would need concept mapping in production
        "condition_start_date": p.get(getter=lambda s: (get_first_existing(s, ['onsetDateTime', 'recordedDate']) or '').split('T')[0] or None)(src),
        "condition_start_datetime": get_first_existing(src, ['onsetDateTime', 'recordedDate']),
        "condition_end_date": p.get("abatementDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "condition_end_datetime": p.get("abatementDateTime")(src),
        "condition_type_concept_id": p.case(p.get("category[0].coding[0].code")(src), {
            "encounter-diagnosis": 32817,
            "problem-list-item": 32818,
            "health-concern": 32819,
        }, default=32817),
        "condition_status_concept_id": p.case(p.get("clinicalStatus.coding[0].code")(src), {
            "active": 32893,
            "resolved": 32897,
            "inactive": 32896,
        }, default=32893),
        "stop_reason": p.get("note[0].text")(src),
        "provider_id": p.get("recorder.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_occurrence_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_detail_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "condition_source_value": p.get("code.coding[0].code")(src),
        "condition_source_concept_id": 0,
        "condition_status_source_value": p.get("clinicalStatus.coding[0].code")(src),
    }
)

to_omop_condition_occurrence = DataMapping(
    mapper=condition_occurrence_mapper,
    input_schema=Condition,
    output_schema=ConditionOccurrence,
)