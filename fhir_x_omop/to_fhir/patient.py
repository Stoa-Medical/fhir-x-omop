from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Piper
from chidian.seeds import DROP
import chidian.partials as p

from ..lexicons import gender_code_lexicon

patient_mapping = DataMapping({
    "resourceType": "Patient",
    "id": p.get("person_id"),
    "identifier": [{
        "use": "usual",
        "system": "OMOP",
        "value": p.get("person_id") >> p.default(DROP.THIS_OBJECT),
    }],
    "gender": p.get("gender_concept_id") >> p.lookup(gender_code_lexicon),
    "birthDate": p.case(
        p.get("birthDate") >> p.default(DROP.THIS_OBJECT),
        p.get("year_of_birth,month_of_birth,day_of_birth") >> p.join("-")
    ),
    "telecom": p.get("telecom[0].value"),
})

to_fhir_patient = Piper(source=Person, target=Patient, mapping=patient_mapping)
