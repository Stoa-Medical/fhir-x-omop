from fhir.resources.observation import Observation
from omop_pydantic import Observation as OMOPObservation

from chidian import DataMapping, Mapper
import chidian.partials as p

observation_mapper = Mapper(
    lambda src: {
        "resourceType": "Observation",
        "id": (p.get("observation_id") | p.str())(src),
        "identifier": [{
            "system": "http://omop.org/observation",
            "value": (p.get("observation_id") | p.str())(src),
        }],
        "status": "final",
        "code": {
            "coding": [{
                "system": p.case(p.get("observation_type_concept_id")(src), {
                    32817: "http://loinc.org",
                    32818: "http://snomed.info/sct",
                }, default="http://omop.org/observation"),
                "code": p.get("observation_source_value")(src),
                "display": p.get("observation_source_value")(src),
            }]
        },
        "subject": {
            "reference": (p.get("person_id") | p.format("Patient/{}"))(src)
        },
        "encounter": {
            "reference": (p.get("visit_occurrence_id") | p.format("Encounter/{}"))(src)
        },
        "effectiveDateTime": (p.get("observation_datetime") | p.str())(src),
        "issued": (p.get("observation_datetime") | p.str())(src),
        "performer": [{
            "reference": (p.get("provider_id") | p.format("Practitioner/{}"))(src)
        }],
        "valueQuantity": p.if_else(
            (p.get("value_as_number") | p.exists())(src),
            {
                "value": p.get("value_as_number")(src),
                "unit": p.get("unit_source_value")(src),
                "system": "http://unitsofmeasure.org",
                "code": p.get("unit_source_value")(src),
            },
            p.get(None)(src)
        ),
        "valueString": p.get("value_as_string")(src),
        "valueCodeableConcept": p.if_else(
            (p.get("value_as_concept_id") | p.exists())(src),
            {
                "coding": [{
                    "system": "http://omop.org/concept",
                    "code": (p.get("value_as_concept_id") | p.str())(src),
                    "display": p.get("value_source_value")(src),
                }]
            },
            p.get(None)(src)
        ),
    }
)

to_fhir_observation = DataMapping(
    mapper=observation_mapper,
    input_schema=OMOPObservation,
    output_schema=Observation,
)