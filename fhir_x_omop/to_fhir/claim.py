from fhir.resources.claim import Claim
from omop_pydantic import Cost

from chidian import DataMapping, Piper
import chidian.partials as p

claim_mapping = DataMapping({
    "resourceType": "Claim",
    "id": p.get("cost_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/cost",
        "value": p.get("cost_id") >> p.str(),
    }],
    "status": "active",
    "type": {
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/claim-type",
            "code": p.case(p.get("cost_domain_id"), {
                "Visit": "institutional",
                "Procedure": "professional", 
                "Drug": "pharmacy",
                "default": "professional"
            }),
            "display": p.case(p.get("cost_domain_id"), {
                "Visit": "Institutional",
                "Procedure": "Professional", 
                "Drug": "Pharmacy",
                "default": "Professional"
            })
        }]
    },
    "use": "claim",
    "patient": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "created": p.get("cost_date") >> p.str(),
    "insurance": [{
        "sequence": 1,
        "focal": True,
        "coverage": {
            "reference": p.get("payer_plan_period_id") >> p.format("Coverage/{}")
        }
    }],
    "item": [{
        "sequence": 1,
        "revenue": {
            "coding": [{
                "system": "http://hl7.org/fhir/ex-revenue-center",
                "code": p.get("revenue_code_source_value"),
            }]
        },
        "net": {
            "value": p.get("total_charge"),
            "currency": "USD"
        },
        "adjudication": [
            {
                "category": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "eligible"
                    }]
                },
                "amount": {
                    "value": p.get("amount_allowed"),
                    "currency": "USD"
                }
            },
            {
                "category": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "benefit"
                    }]
                },
                "amount": {
                    "value": p.get("paid_by_payer"),
                    "currency": "USD"
                }
            },
            {
                "category": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "copay"
                    }]
                },
                "amount": {
                    "value": p.get("paid_patient_copay"),
                    "currency": "USD"
                }
            },
            {
                "category": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "coins"
                    }]
                },
                "amount": {
                    "value": p.get("paid_patient_coinsurance"),
                    "currency": "USD"
                }
            },
            {
                "category": {
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/adjudication",
                        "code": "deductible"
                    }]
                },
                "amount": {
                    "value": p.get("paid_patient_deductible"),
                    "currency": "USD"
                }
            }
        ]
    }],
    "total": {
        "value": p.get("total_charge"),
        "currency": "USD"
    },
    "payment": {
        "amount": {
            "value": p.get("total_paid"),
            "currency": "USD"
        }
    }
})

to_fhir_claim = Piper(source=Cost, target=Claim, mapping=claim_mapping)