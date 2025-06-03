from fhir.resources.observation import Observation
from omop_pydantic import Observation as OMOPObservation

from chidian import DataMapping, Piper
import chidian.partials as p

observation_mapping = DataMapping({
    "resourceType": "Observation",
    "id": p.get("observation_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/observation",
        "value": p.get("observation_id") >> p.str(),
    }],
    "status": "final",
    "code": {
        "coding": [{
            "system": p.case(p.get("observation_type_concept_id"), {
                "32817": "http://loinc.org",
                "32818": "http://snomed.info/sct",
                "default": "http://omop.org/observation"
            }),
            "code": p.get("observation_source_value"),
            "display": p.get("observation_source_value"),
        }]
    },
    "subject": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "encounter": {
        "reference": p.get("visit_occurrence_id") >> p.format("Encounter/{}")
    },
    "effectiveDateTime": p.get("observation_datetime") >> p.str(),
    "issued": p.get("observation_datetime") >> p.str(),
    "performer": [{
        "reference": p.get("provider_id") >> p.format("Practitioner/{}")
    }],
    "valueQuantity": p.case(
        p.get("value_as_number") >> p.exists(),
        {
            "value": p.get("value_as_number"),
            "unit": p.get("unit_source_value"),
            "system": "http://unitsofmeasure.org",
            "code": p.get("unit_source_value"),
        },
        p.default(None)
    ),
    "valueString": p.get("value_as_string"),
    "valueCodeableConcept": p.case(
        p.get("value_as_concept_id") >> p.exists(),
        {
            "coding": [{
                "system": "http://omop.org/concept",
                "code": p.get("value_as_concept_id") >> p.str(),
                "display": p.get("value_source_value"),
            }]
        },
        p.default(None)
    ),
})

to_fhir_observation = Piper(source=OMOPObservation, target=Observation, mapping=observation_mapping)