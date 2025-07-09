from fhir.resources.procedure import Procedure
from omop_pydantic import ProcedureOccurrence

from chidian import DataMapping, Piper
import chidian.partials as p

procedure_piper = Piper(
    lambda src: {
        "resourceType": "Procedure",
        "id": (p.get("procedure_occurrence_id") >> p.str())(src),
        "identifier": [{
            "system": "http://omop.org/procedure",
            "value": (p.get("procedure_occurrence_id") >> p.str())(src),
        }],
        "status": "completed",
        "code": {
            "coding": [{
                "system": p.case(p.get("procedure_type_concept_id")(src), {
                    32817: "http://www.ama-assn.org/go/cpt",
                    32818: "http://hl7.org/fhir/sid/icd-10-pcs",
                    32819: "http://hl7.org/fhir/sid/icd-9-cm",
                }, default="http://omop.org/procedure"),
                "code": p.get("procedure_source_value")(src),
                "display": p.get("procedure_source_value")(src),
            }]
        },
        "subject": {
            "reference": (p.get("person_id") >> p.format("Patient/{}"))(src)
        },
        "encounter": {
            "reference": (p.get("visit_occurrence_id") >> p.format("Encounter/{}"))(src)
        },
        "performedDateTime": (p.get("procedure_datetime") >> p.str())(src),
        "performer": [{
            "actor": {
                "reference": (p.get("provider_id") >> p.format("Practitioner/{}"))(src)
            }
        }],
    }
)

to_fhir_procedure = DataMapping(
    piper=procedure_piper,
    input_schema=ProcedureOccurrence,
    output_schema=Procedure,
)