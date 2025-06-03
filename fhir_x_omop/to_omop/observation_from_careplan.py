from fhir.resources.careplan import CarePlan
from omop_pydantic import Observation

from chidian import DataMapping, Piper
import chidian.partials as p

observation_from_careplan_mapping = DataMapping({
    "observation_id": p.get("id") >> p.int(),
    "person_id": p.get("subject.reference | split(@, '/')[1]") >> p.int(),
    "observation_concept_id": 0,  # Would need concept mapping for care plan in production
    "observation_date": p.get("created | split(@, 'T')[0]"),
    "observation_datetime": p.get("created"),
    "observation_type_concept_id": p.case(p.get("status"), {
        "active": 32817,
        "completed": 32818,
        "on-hold": 32819,
        "default": 32817
    }),
    "value_as_number": None,
    "value_as_string": p.get("description | activity[0].detail.description"),
    "value_as_concept_id": 0,
    "qualifier_concept_id": 0,
    "unit_concept_id": 0,
    "provider_id": p.get("author.reference | split(@, '/')[1]") >> p.int(),
    "visit_occurrence_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "visit_detail_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "observation_source_value": p.get("title | activity[0].detail.code.coding[0].code"),
    "observation_source_concept_id": 0,
    "unit_source_value": None,
    "qualifier_source_value": p.get("note[0].text"),
    "value_source_value": p.get("description | activity[0].detail.description"),
})

to_omop_observation_from_careplan = Piper(source=CarePlan, target=Observation, mapping=observation_from_careplan_mapping)