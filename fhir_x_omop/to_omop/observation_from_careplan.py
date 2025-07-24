from fhir.resources.careplan import CarePlan
from omop_pydantic import Observation

from chidian import DataMapping, Mapper
import chidian.partials as p

def get_first_existing(src, paths):
    for path in paths:
        value = p.get(path)(src)
        if value:
            return value
    return None

observation_from_careplan_mapper = Mapper(
    lambda src: {
        "observation_id": (p.get("id") | p.int())(src),
        "person_id": p.get("subject.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "observation_concept_id": 0,  # Would need concept mapping for care plan in production
        "observation_date": p.get("created", getter=lambda x: x.split('T')[0] if x else None)(src),
        "observation_datetime": p.get("created")(src),
        "observation_type_concept_id": p.case(p.get("status")(src), {
            "active": 32817,
            "completed": 32818,
            "on-hold": 32819,
        }, default=32817),
        "value_as_number": None,
        "value_as_string": get_first_existing(src, ["description", "activity[0].detail.description"]),
        "value_as_concept_id": 0,
        "qualifier_concept_id": 0,
        "unit_concept_id": 0,
        "provider_id": p.get("author.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_occurrence_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_detail_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "observation_source_value": get_first_existing(src, ["title", "activity[0].detail.code.coding[0].code"]),
        "observation_source_concept_id": 0,
        "unit_source_value": None,
        "qualifier_source_value": p.get("note[0].text")(src),
        "value_source_value": get_first_existing(src, ["description", "activity[0].detail.description"]),
    }
)

to_omop_observation_from_careplan = DataMapping(
    mapper=observation_from_careplan_mapper,
    input_schema=CarePlan,
    output_schema=Observation,
)