from fhir.resources.immunization import Immunization
from omop_pydantic import DrugExposure

from chidian import DataMapping, Piper
import chidian.partials as p

immunization_mapping = DataMapping({
    "resourceType": "Immunization",
    "id": p.get("drug_exposure_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/drug_exposure",
        "value": p.get("drug_exposure_id") >> p.str(),
    }],
    "status": "completed",
    "vaccineCode": {
        "coding": [{
            "system": p.case(p.get("drug_type_concept_id"), {
                "38000179": "http://hl7.org/fhir/sid/cvx",
                "38000180": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "default": "http://omop.org/drug"
            }),
            "code": p.get("drug_source_value"),
            "display": p.get("drug_source_value"),
        }]
    },
    "patient": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "encounter": {
        "reference": p.get("visit_occurrence_id") >> p.format("Encounter/{}")
    },
    "occurrenceDateTime": p.get("drug_exposure_start_datetime") >> p.str(),
    "recorded": p.get("drug_exposure_start_datetime") >> p.str(),
    "primarySource": True,
    "lotNumber": p.get("lot_number"),
    "route": {
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration",
            "code": p.case(p.get("route_source_value"), {
                "intramuscular": "IM",
                "subcutaneous": "SC",
                "oral": "PO",
                "intranasal": "NASINHL",
                "default": "IM"
            }),
            "display": p.get("route_source_value")
        }]
    },
    "doseQuantity": {
        "value": p.get("quantity") >> p.float(),
        "unit": p.get("dose_unit_source_value | 'dose'"),
        "system": "http://unitsofmeasure.org",
        "code": p.get("dose_unit_source_value | 'dose'")
    },
    "performer": [{
        "function": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v2-0443",
                "code": "AP",
                "display": "Administering Provider"
            }]
        },
        "actor": {
            "reference": p.get("provider_id") >> p.format("Practitioner/{}")
        }
    }],
})

to_fhir_immunization = Piper(source=DrugExposure, target=Immunization, mapping=immunization_mapping)