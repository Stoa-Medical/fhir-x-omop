from fhir.resources.procedure import Procedure
from omop_pydantic import ProcedureOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

procedure_mapping = DataMapping({
    "resourceType": "Procedure",
    "id": p.get("procedure_occurrence_id") >> p.str(),
    "identifier": [{
        "system": "http://omop.org/procedure",
        "value": p.get("procedure_occurrence_id") >> p.str(),
    }],
    "status": "completed",
    "code": {
        "coding": [{
            "system": p.case(p.get("procedure_type_concept_id"), {
                "32817": "http://www.ama-assn.org/go/cpt",
                "32818": "http://hl7.org/fhir/sid/icd-10-pcs",
                "32819": "http://hl7.org/fhir/sid/icd-9-cm",
                "default": "http://omop.org/procedure"
            }),
            "code": p.get("procedure_source_value"),
            "display": p.get("procedure_source_value"),
        }]
    },
    "subject": {
        "reference": p.get("person_id") >> p.format("Patient/{}")
    },
    "encounter": {
        "reference": p.get("visit_occurrence_id") >> p.format("Encounter/{}")
    },
    "performedDateTime": p.get("procedure_datetime") >> p.str(),
    "performer": [{
        "actor": {
            "reference": p.get("provider_id") >> p.format("Practitioner/{}")
        }
    }],
})

to_fhir_procedure = Piper(source=ProcedureOccurrence, target=Procedure, mapping=procedure_mapping)