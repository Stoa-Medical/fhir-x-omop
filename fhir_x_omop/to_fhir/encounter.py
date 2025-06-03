from fhir.resources.encounter import Encounter
from omop_pydantic import VisitOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

encounter_mapping = DataMapping({
    "resourceType": "Encounter",
    "id": p.get("visit_occurrence_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/visit",
        "value": p.get("visit_occurrence_id") >> p.str(),
    }],
    "status": "finished",
    "class": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
        "code": p.case(p.get("visit_concept_id"), {
            "9201": "IMP",      # Inpatient Visit
            "9202": "AMB",      # Outpatient Visit
            "9203": "EMER",     # Emergency Room Visit
            "581379": "HH",     # Home Health
            "32036": "VR",      # Virtual
            "default": "AMB"
        }),
        "display": p.case(p.get("visit_concept_id"), {
            "9201": "inpatient encounter",
            "9202": "ambulatory",
            "9203": "emergency",
            "581379": "home health",
            "32036": "virtual",
            "default": "ambulatory"
        })
    },
    "type": [{
        "coding": [{
            "system": "http://omop.org/visit-type",
            "code": p.get("visit_source_value"),
            "display": p.get("visit_source_value")
        }]
    }],
    "subject": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "participant": [{
        "type": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                "code": "ATND",
                "display": "attender"
            }]
        }],
        "individual": {
            "reference": p.get("provider_id") >> p.format("Practitioner/{}")
        }
    }],
    "period": {
        "start": p.get("visit_start_datetime") >> p.str(),
        "end": p.get("visit_end_datetime") >> p.str()
    },
    "hospitalization": {
        "dischargeDisposition": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/discharge-disposition",
                "code": p.case(p.get("discharge_to_concept_id"), {
                    "8536": "home",
                    "8676": "snf",
                    "8615": "rehab",
                    "4216643": "exp",   # Expired
                    "default": "other"
                }),
                "display": p.get("discharge_to_source_value")
            }]
        },
        "admitSource": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/admit-source",
                "code": p.get("admitted_from_source_value"),
                "display": p.get("admitted_from_source_value")
            }]
        }
    },
    "serviceProvider": {
        "reference": p.get("care_site_id") >> p.format("Organization/{}")
    }
})

to_fhir_encounter = Piper(source=VisitOccurrence, target=Encounter, mapping=encounter_mapping)