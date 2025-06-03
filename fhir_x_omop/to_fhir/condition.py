from fhir.resources.condition import Condition
from omop_pydantic import ConditionOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

condition_mapping = DataMapping({
    "resourceType": "Condition",
    "id": p.get("condition_occurrence_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/condition",
        "value": p.get("condition_occurrence_id") >> p.str(),
    }],
    "clinicalStatus": {
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
            "code": p.case(p.get("condition_status_concept_id"), {
                "32893": "active",
                "32897": "resolved",
                "32896": "inactive",
                "default": "active"
            })
        }]
    },
    "verificationStatus": {
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
            "code": "confirmed"
        }]
    },
    "category": [{
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/condition-category",
            "code": p.case(p.get("condition_type_concept_id"), {
                "32817": "encounter-diagnosis",
                "32818": "problem-list-item",
                "32819": "health-concern",
                "default": "encounter-diagnosis"
            })
        }]
    }],
    "code": {
        "coding": [{
            "system": p.case(p.get("condition_type_concept_id"), {
                "32817": "http://hl7.org/fhir/sid/icd-10-cm",
                "32818": "http://snomed.info/sct",
                "default": "http://hl7.org/fhir/sid/icd-10-cm"
            }),
            "code": p.get("condition_source_value"),
            "display": p.get("condition_source_value")
        }]
    },
    "subject": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "encounter": {
        "reference": p.get("visit_occurrence_id") >> p.format("Encounter/{}")
    },
    "onsetDateTime": p.get("condition_start_datetime") >> p.str(),
    "abatementDateTime": p.get("condition_end_datetime") >> p.str(),
    "recordedDate": p.get("condition_start_datetime") >> p.str(),
    "recorder": {
        "reference": p.get("provider_id") >> p.format("Practitioner/{}")
    },
    "note": [{
        "text": p.get("stop_reason")
    }]
})

to_fhir_condition = Piper(source=ConditionOccurrence, target=Condition, mapping=condition_mapping)