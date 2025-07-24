from fhir.resources.encounter import Encounter
from omop_pydantic import VisitOccurrence

from chidian import DataMapping, Mapper
import chidian.partials as p

def get_attending_provider_id(participants):
    if not participants:
        return None
    for participant in participants:
        if (participant.type and 
            participant.type[0].coding and 
            participant.type[0].coding[0].code == 'ATND' and
            participant.individual and
            participant.individual.reference):
            return int(participant.individual.reference.split('/')[1])
    return None

visit_occurrence_mapper = Mapper(
    lambda src: {
        "visit_occurrence_id": (p.get("id") | p.int())(src),
        "person_id": p.get("subject.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_concept_id": p.case(p.get("class.code")(src), {
            "IMP": 9201,      # Inpatient Visit
            "AMB": 9202,      # Outpatient Visit  
            "EMER": 9203,     # Emergency Room Visit
            "HH": 581379,     # Home Health
            "VR": 32036,      # Virtual
        }, default=9202),   # Default to Outpatient
        "visit_start_date": p.get("period.start", getter=lambda x: x.split('T')[0] if x else None)(src),
        "visit_start_datetime": p.get("period.start")(src),
        "visit_end_date": p.get("period.end", getter=lambda x: x.split('T')[0] if x else None)(src),
        "visit_end_datetime": p.get("period.end")(src),
        "visit_type_concept_id": 44818518,  # Visit derived from EHR
        "provider_id": p.get("participant", getter=get_attending_provider_id)(src),
        "care_site_id": p.get("serviceProvider.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_source_value": p.get("type[0].coding[0].code")(src),
        "visit_source_concept_id": 0,
        "admitted_from_concept_id": 0,
        "admitted_from_source_value": p.get("hospitalization.admitSource.coding[0].code")(src),
        "discharge_to_concept_id": p.case(p.get("hospitalization.dischargeDisposition.coding[0].code")(src), {
            "home": 8536,
            "snf": 8676,
            "rehab": 8615,
            "exp": 4216643,
        }, default=0),
        "discharge_to_source_value": p.get("hospitalization.dischargeDisposition.coding[0].display")(src),
        "preceding_visit_occurrence_id": None,
    }
)

to_omop_visit_occurrence = DataMapping(
    mapper=visit_occurrence_mapper,
    input_schema=Encounter,
    output_schema=VisitOccurrence,
)