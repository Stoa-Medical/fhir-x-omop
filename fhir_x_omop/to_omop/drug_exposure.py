from fhir.resources.immunization import Immunization
from omop_pydantic import DrugExposure

from chidian import DataMapping, Piper
import chidian.partials as p

def get_first_existing(src, paths):
    for path in paths:
        value = p.get(path)(src)
        if value:
            return value
    return None

drug_exposure_piper = Piper(
    lambda src: {
        "drug_exposure_id": (p.get("id") >> p.int())(src),
        "person_id": p.get("patient.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "drug_concept_id": 0,  # Would need concept mapping in production
        "drug_exposure_start_date": p.get("occurrenceDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "drug_exposure_start_datetime": p.get("occurrenceDateTime")(src),
        "drug_exposure_end_date": p.get("occurrenceDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "drug_exposure_end_datetime": p.get("occurrenceDateTime")(src),
        "verbatim_end_date": p.get("occurrenceDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "drug_type_concept_id": p.case(p.get("vaccineCode.coding[0].system")(src), {
            "http://hl7.org/fhir/sid/cvx": 38000179,
            "http://www.nlm.nih.gov/research/umls/rxnorm": 38000180,
        }, default=38000175),  # Prescription
        "stop_reason": None,
        "refills": 0,
        "quantity": (p.get("doseQuantity.value", default=1.0) >> p.float())(src),
        "days_supply": 1,  # Immunizations are single dose
        "sig": (p.get(getter=lambda s: get_first_existing(s, ["vaccineCode.coding[0].display", "vaccineCode.text"])) >> p.format("Immunization: {}"))(src),
        "route_concept_id": 0,
        "lot_number": p.get("lotNumber")(src),
        "provider_id": p.get("performer[0].actor.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_occurrence_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_detail_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "drug_source_value": p.get("vaccineCode.coding[0].code")(src),
        "drug_source_concept_id": 0,
        "route_source_value": p.case(p.get("route.coding[0].code")(src), {
            "IM": "intramuscular",
            "SC": "subcutaneous", 
            "PO": "oral",
            "NASINHL": "intranasal",
        }, default="intramuscular"),
        "dose_unit_source_value": p.get("doseQuantity.unit", default='dose')(src),
    }
)

to_omop_drug_exposure = DataMapping(
    piper=drug_exposure_piper,
    input_schema=Immunization,
    output_schema=DrugExposure,
)