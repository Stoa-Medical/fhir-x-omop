from fhir.resources.claim import Claim
from omop_pydantic import Cost

from chidian import DataMapping, Mapper
import chidian.partials as p

claim_mapper = Mapper(
    lambda src: {
        "resourceType": "Claim",
        "id": (p.get("cost_id") | p.str())(src),
        "identifier": [{
            "system": "http://omop.org/cost",
            "value": (p.get("cost_id") | p.str())(src),
        }],
        "status": "active",
        "type": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/claim-type",
                "code": p.case(p.get("cost_domain_id")(src), {
                    "Visit": "institutional",
                    "Procedure": "professional", 
                    "Drug": "pharmacy",
                }, default="professional"),
                "display": p.case(p.get("cost_domain_id")(src), {
                    "Visit": "Institutional",
                    "Procedure": "Professional", 
                    "Drug": "Pharmacy",
                }, default="Professional")
            }]
        },
        "use": "claim",
        "patient": {
            "reference": (p.get("person_id") | p.format("Patient/{}"))(src)
        },
        "created": (p.get("cost_date") | p.str())(src),
        "insurance": [{
            "sequence": 1,
            "focal": True,
            "coverage": {
                "reference": (p.get("payer_plan_period_id") | p.format("Coverage/{}"))(src)
            }
        }],
        "item": [{
            "sequence": 1,
            "revenue": {
                "coding": [{
                    "system": "http://hl7.org/fhir/ex-revenue-center",
                    "code": p.get("revenue_code_source_value")(src),
                }]
            },
            "net": {
                "value": p.get("total_charge")(src),
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
                        "value": p.get("amount_allowed")(src),
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
                        "value": p.get("paid_by_payer")(src),
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
                        "value": p.get("paid_patient_copay")(src),
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
                        "value": p.get("paid_patient_coinsurance")(src),
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
                        "value": p.get("paid_patient_deductible")(src),
                        "currency": "USD"
                    }
                }
            ]
        }],
        "total": {
            "value": p.get("total_charge")(src),
            "currency": "USD"
        },
        "payment": {
            "amount": {
                "value": p.get("total_paid")(src),
                "currency": "USD"
            }
        }
    }
)

to_fhir_claim = DataMapping(
    mapper=claim_mapper,
    input_schema=Cost,
    output_schema=Claim,
)