from fhir.resources.condition import Condition
from omop_pydantic import ConditionOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

condition_piper = Piper(
    lambda src: {
        "resourceType": "Condition",
        "id": (p.get("condition_occurrence_id") >> p.str())(src),
        "identifier": [{
            "system": "http://omop.org/condition",
            "value": (p.get("condition_occurrence_id") >> p.str())(src),
        }],
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": p.case(p.get("condition_status_concept_id")(src), {
                    32893: "active",
                    32897: "resolved",
                    32896: "inactive",
                }, default="active")
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
                "code": p.case(p.get("condition_type_concept_id")(src), {
                    32817: "encounter-diagnosis",
                    32818: "problem-list-item",
                    32819: "health-concern",
                }, default="encounter-diagnosis")
            }]
        }],
        "code": {
            "coding": [{
                "system": p.case(p.get("condition_type_concept_id")(src), {
                    32817: "http://hl7.org/fhir/sid/icd-10-cm",
                    32818: "http://snomed.info/sct",
                }, default="http://hl7.org/fhir/sid/icd-10-cm"),
                "code": p.get("condition_source_value")(src),
                "display": p.get("condition_source_value")(src)
            }]
        },
        "subject": {
            "reference": (p.get("person_id") >> p.format("Patient/{}"))(src)
        },
        "encounter": {
            "reference": (p.get("visit_occurrence_id") >> p.format("Encounter/{}"))(src)
        },
        "onsetDateTime": (p.get("condition_start_datetime") >> p.str())(src),
        "abatementDateTime": (p.get("condition_end_datetime") >> p.str())(src),
        "recordedDate": (p.get("condition_start_datetime") >> p.str())(src),
        "recorder": {
            "reference": (p.get("provider_id") >> p.format("Practitioner/{}"))(src)
        },
        "note": [{
            "text": p.get("stop_reason")(src)
        }]
    }
)

to_fhir_condition = DataMapping(
    piper=condition_piper,
    input_schema=ConditionOccurrence,
    output_schema=Condition,
)