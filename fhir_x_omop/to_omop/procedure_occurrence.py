from fhir.resources.procedure import Procedure
from omop_pydantic import ProcedureOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

procedure_occurrence_mapping = DataMapping({
    "procedure_occurrence_id": p.get("id") >> p.int(),
    "person_id": p.get("subject.reference | split(@, '/')[1]") >> p.int(),
    "procedure_concept_id": 0,  # Would need concept mapping in production
    "procedure_date": p.get("performedDateTime | split(@, 'T')[0]"),
    "procedure_datetime": p.get("performedDateTime"),
    "procedure_type_concept_id": p.case(p.get("code.coding[0].system"), {
        "http://www.ama-assn.org/go/cpt": 32817,
        "http://hl7.org/fhir/sid/icd-10-pcs": 32818,
        "http://hl7.org/fhir/sid/icd-9-cm": 32819,
        "default": 32820
    }),
    "modifier_concept_id": 0,
    "quantity": 1,
    "provider_id": p.get("performer[0].actor.reference | split(@, '/')[1]") >> p.int(),
    "visit_occurrence_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "visit_detail_id": p.get("encounter.reference | split(@, '/')[1]") >> p.int(),
    "procedure_source_value": p.get("code.coding[0].code"),
    "procedure_source_concept_id": 0,
    "modifier_source_value": p.get("code.coding[0].display"),
})

to_omop_procedure_occurrence = Piper(source=Procedure, target=ProcedureOccurrence, mapping=procedure_occurrence_mapping)