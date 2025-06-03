from fhir.resources.immunization import Immunization
from omop_pydantic import DrugExposure

from chidian import DataMapping, Piper
import chidian.partials as p

drug_exposure_mapping = DataMapping({
    "drug_exposure_id": p.get("id") >> p.int(),
    "person_id": p.get("patient.reference | split(@, '/')[1]") >> p.int(),
    "drug_concept_id": 0,  # Would need concept mapping in production
    "drug_exposure_start_date": p.get("occurrenceDateTime | split(@, 'T')[0]"),
    "drug_exposure_start_datetime": p.get("occurrenceDateTime"),
    "drug_exposure_end_date": p.get("occurrenceDateTime | split(@, 'T')[0]"),
    "drug_exposure_end_datetime": p.get("occurrenceDateTime"),
    "verbatim_end_date": p.get("occurrenceDateTime | split(@, 'T')[0]"),
    "drug_type_concept_id": p.case(p.get("vaccineCode.coding[0].system"), {
        "http://hl7.org/fhir/sid/cvx": 38000179,
        "http://www.nlm.nih.gov/research/umls/rxnorm": 38000180,
        "default": 38000175  # Prescription
    }),
    "stop_reason": None,
    "refills": 0,
    "quantity": p.get("doseQuantity.value") >> p.float() >> p.default(1.0),
    "days_supply": 1,  # Immunizations are single dose
    "sig": p.get("vaccineCode.coding[0].display | vaccineCode.text") >> p.format("Immunization: {}"),
    "route_concept_id": 0,
    "lot_number": p.get("lotNumber"),
    "provider_id": p.get("performer[0].actor.reference | split(@, '/')[1]") >> p.int(),
    "visit_occurrence_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "visit_detail_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "drug_source_value": p.get("vaccineCode.coding[0].code"),
    "drug_source_concept_id": 0,
    "route_source_value": p.case(p.get("route.coding[0].code"), {
        "IM": "intramuscular",
        "SC": "subcutaneous", 
        "PO": "oral",
        "NASINHL": "intranasal",
        "default": "intramuscular"
    }),
    "dose_unit_source_value": p.get("doseQuantity.unit | 'dose'"),
})

to_omop_drug_exposure = Piper(source=Immunization, target=DrugExposure, mapping=drug_exposure_mapping)