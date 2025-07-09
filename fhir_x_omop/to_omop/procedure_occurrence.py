from fhir.resources.procedure import Procedure
from omop_pydantic import ProcedureOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

procedure_occurrence_piper = Piper(
    lambda src: {
        "procedure_occurrence_id": (p.get("id") >> p.int())(src),
        "person_id": p.get("subject.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "procedure_concept_id": 0,  # Would need concept mapping in production
        "procedure_date": p.get("performedDateTime", getter=lambda x: x.split('T')[0] if x else None)(src),
        "procedure_datetime": p.get("performedDateTime")(src),
        "procedure_type_concept_id": p.case(p.get("code.coding[0].system")(src), {
            "http://www.ama-assn.org/go/cpt": 32817,
            "http://hl7.org/fhir/sid/icd-10-pcs": 32818,
            "http://hl7.org/fhir/sid/icd-9-cm": 32819,
        }, default=32820),
        "modifier_concept_id": 0,
        "quantity": 1,
        "provider_id": p.get("performer[0].actor.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_occurrence_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "visit_detail_id": p.get("encounter.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "procedure_source_value": p.get("code.coding[0].code")(src),
        "procedure_source_concept_id": 0,
        "modifier_source_value": p.get("code.coding[0].display")(src),
    }
)

to_omop_procedure_occurrence = DataMapping(
    piper=procedure_occurrence_piper,
    input_schema=Procedure,
    output_schema=ProcedureOccurrence,
)