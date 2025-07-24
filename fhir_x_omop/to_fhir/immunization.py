from fhir.resources.immunization import Immunization
from omop_pydantic import DrugExposure

from chidian import DataMapping, Mapper
import chidian.partials as p

immunization_mapper = Mapper(
    lambda src: {
        "resourceType": "Immunization",
        "id": (p.get("drug_exposure_id") | p.str())(src),
        "identifier": [{
            "system": "http://omop.org/drug_exposure",
            "value": (p.get("drug_exposure_id") | p.str())(src),
        }],
        "status": "completed",
        "vaccineCode": {
            "coding": [{
                "system": p.case(p.get("drug_type_concept_id")(src), {
                    38000179: "http://hl7.org/fhir/sid/cvx",
                    38000180: "http://www.nlm.nih.gov/research/umls/rxnorm",
                }, default="http://omop.org/drug"),
                "code": p.get("drug_source_value")(src),
                "display": p.get("drug_source_value")(src),
            }]
        },
        "patient": {
            "reference": (p.get("person_id") | p.format("Patient/{}"))(src)
        },
        "encounter": {
            "reference": (p.get("visit_occurrence_id") | p.format("Encounter/{}"))(src)
        },
        "occurrenceDateTime": (p.get("drug_exposure_start_datetime") | p.str())(src),
        "recorded": (p.get("drug_exposure_start_datetime") | p.str())(src),
        "primarySource": True,
        "lotNumber": p.get("lot_number")(src),
        "route": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration",
                "code": p.case(p.get("route_source_value")(src), {
                    "intramuscular": "IM",
                    "subcutaneous": "SC",
                    "oral": "PO",
                    "intranasal": "NASINHL",
                }, default="IM"),
                "display": p.get("route_source_value")(src)
            }]
        },
        "doseQuantity": {
            "value": (p.get("quantity") | p.float())(src),
            "unit": p.get("dose_unit_source_value", default='dose')(src),
            "system": "http://unitsofmeasure.org",
            "code": p.get("dose_unit_source_value", default='dose')(src)
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
                "reference": (p.get("provider_id") | p.format("Practitioner/{}"))(src)
            }
        }],
    }
)

to_fhir_immunization = DataMapping(
    mapper=immunization_mapper,
    input_schema=DrugExposure,
    output_schema=Immunization,
)