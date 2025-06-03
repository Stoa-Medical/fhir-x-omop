from fhir.resources.observation import Observation as FHIRObservation
from omop_pydantic import Observation

from chidian import DataMapping, Piper
import chidian.partials as p

observation_mapping = DataMapping({
    "observation_id": p.get("id") >> p.int(),
    "person_id": p.get("subject.reference | split(@, '/')[1]") >> p.int(),
    "observation_concept_id": 0,  # Would need concept mapping in production
    "observation_date": p.get("effectiveDateTime | split(@, 'T')[0]"),
    "observation_datetime": p.get("effectiveDateTime"),
    "observation_type_concept_id": p.case(p.get("code.coding[0].system"), {
        "http://loinc.org": 32817,
        "http://snomed.info/sct": 32818,
        "default": 32819
    }),
    "value_as_number": p.get("valueQuantity.value") >> p.float(),
    "value_as_string": p.get("valueString"),
    "value_as_concept_id": p.get("valueCodeableConcept.coding[0].code") >> p.int(),
    "qualifier_concept_id": 0,
    "unit_concept_id": 0,
    "provider_id": p.get("performer[0].reference | split(@, '/')[1]") >> p.int(),
    "visit_occurrence_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "visit_detail_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "observation_source_value": p.get("code.coding[0].code"),
    "observation_source_concept_id": 0,
    "unit_source_value": p.get("valueQuantity.unit"),
    "qualifier_source_value": p.get("code.coding[0].display"),
    "value_source_value": p.get("valueCodeableConcept.coding[0].display | valueString | valueQuantity.value | str(@)"),
})

to_omop_observation = Piper(source=FHIRObservation, target=Observation, mapping=observation_mapping)