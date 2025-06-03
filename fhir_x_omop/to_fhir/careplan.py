from fhir.resources.careplan import CarePlan
from omop_pydantic import Observation as OMOPObservation

from chidian import DataMapping, Piper
import chidian.partials as p

careplan_mapping = DataMapping({
    "resourceType": "CarePlan",
    "id": p.get("observation_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/observation",
        "value": p.get("observation_id") >> p.str(),
    }],
    "status": p.case(p.get("observation_type_concept_id"), {
        "32817": "active",
        "32818": "completed",
        "32819": "on-hold",
        "default": "active"
    }),
    "intent": "plan",
    "category": [{
        "coding": [{
            "system": "http://hl7.org/fhir/us/core/CodeSystem/careplan-category",
            "code": "assess-plan",
            "display": "Assessment and Plan of Treatment"
        }]
    }],
    "title": p.get("observation_source_value"),
    "description": p.get("value_as_string"),
    "subject": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "encounter": {
        "reference": p.get("visit_occurrence_id") >> p.format("Encounter/{}")
    },
    "period": {
        "start": p.get("observation_datetime") >> p.str(),
        "end": p.get("observation_datetime") >> p.str()
    },
    "created": p.get("observation_datetime") >> p.str(),
    "author": {
        "reference": p.get("provider_id") >> p.format("Practitioner/{}")
    },
    "activity": [{
        "detail": {
            "kind": "Task",
            "code": {
                "coding": [{
                    "system": "http://snomed.info/sct",
                    "code": p.get("observation_source_value"),
                    "display": p.get("observation_source_value")
                }]
            },
            "status": "in-progress",
            "description": p.get("value_as_string")
        }
    }],
    "note": [{
        "text": p.get("qualifier_source_value")
    }]
})

to_fhir_careplan = Piper(source=OMOPObservation, target=CarePlan, mapping=careplan_mapping)