from fhir.resources.careplan import CarePlan
from omop_pydantic import Observation as OMOPObservation

from chidian import DataMapping, Piper
import chidian.partials as p

careplan_piper = Piper(
    lambda src: {
        "resourceType": "CarePlan",
        "id": (p.get("observation_id") >> p.str())(src),
        "identifier": [{
            "system": "http://omop.org/observation",
            "value": (p.get("observation_id") >> p.str())(src),
        }],
        "status": p.case(p.get("observation_type_concept_id")(src), {
            32817: "active",
            32818: "completed",
            32819: "on-hold",
        }, default="active"),
        "intent": "plan",
        "category": [{
            "coding": [{
                "system": "http://hl7.org/fhir/us/core/CodeSystem/careplan-category",
                "code": "assess-plan",
                "display": "Assessment and Plan of Treatment"
            }]
        }],
        "title": p.get("observation_source_value")(src),
        "description": p.get("value_as_string")(src),
        "subject": {
            "reference": (p.get("person_id") >> p.format("Patient/{}"))(src)
        },
        "encounter": {
            "reference": (p.get("visit_occurrence_id") >> p.format("Encounter/{}"))(src)
        },
        "period": {
            "start": (p.get("observation_datetime") >> p.str())(src),
            "end": (p.get("observation_datetime") >> p.str())(src)
        },
        "created": (p.get("observation_datetime") >> p.str())(src),
        "author": {
            "reference": (p.get("provider_id") >> p.format("Practitioner/{}"))(src)
        },
        "activity": [{
            "detail": {
                "kind": "Task",
                "code": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": p.get("observation_source_value")(src),
                        "display": p.get("observation_source_value")(src)
                    }]
                },
                "status": "in-progress",
                "description": p.get("value_as_string")(src)
            }
        }],
        "note": [{
            "text": p.get("qualifier_source_value")(src)
        }]
    }
)

to_fhir_careplan = DataMapping(
    piper=careplan_piper,
    input_schema=OMOPObservation,
    output_schema=CarePlan,
)