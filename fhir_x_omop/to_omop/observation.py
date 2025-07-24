from fhir.resources.observation import Observation as FHIRObservation
from omop_pydantic import Observation

from chidian import DataMapping, Mapper
import chidian.partials as p

def get_first_existing(src, paths):
    for path in paths:
        value = p.get(path)(src)
        if value:
            return value
    return None

observation_mapper = Mapper(
    lambda src: {
        "observation_id": (p.get("id") | p.int())(src),
        "person_id": p.get("subject.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "observation_concept_id": 0,  # Would need concept mapping in production
        "observation_date": p.get("effectiveDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "observation_datetime": p.get("effectiveDateTime")(src),
        "observation_type_concept_id": p.case(p.get("code.coding[0].system")(src), {
            "http://loinc.org": 32817,
            "http://snomed.info/sct": 32818,
        }, default=32819),
        "value_as_number": (p.get("valueQuantity.value") | p.float())(src),
        "value_as_string": p.get("valueString")(src),
        "value_as_concept_id": (p.get("valueCodeableConcept.coding[0].code") | p.int())(src),
        "qualifier_concept_id": 0,
        "unit_concept_id": 0,
        "provider_id": p.get("performer[0].reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_occurrence_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_detail_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "observation_source_value": p.get("code.coding[0].code")(src),
        "observation_source_concept_id": 0,
        "unit_source_value": p.get("valueQuantity.unit")(src),
        "qualifier_source_value": p.get("code.coding[0].display")(src),
        "value_source_value": (p.get(getter=lambda s: str(get_first_existing(s, ["valueCodeableConcept.coding[0].display", "valueString", "valueQuantity.value"]) or '')))(src),
    }
)

to_omop_observation = DataMapping(
    mapper=observation_mapper,
    input_schema=FHIRObservation,
    output_schema=Observation,
)