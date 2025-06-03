from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Piper
import chidian.partials as p

from ..lexicons import gender_code_lexicon, race_code_lexicon, ethnicity_code_lexicon

person_mapping = DataMapping({
    "person_id": p.get("id"),
    "gender_concept_id": p.get("gender") >> p.lookup(gender_code_lexicon),
    "year_of_birth": p.get("birthDate") >> p.split("-")[0],
    "month_of_birth": p.get("birthDate") >> p.split("-")[1],
    "day_of_birth": p.get("birthDate") >> p.split("-")[2],
    "telecom": p.get("telecom[0].value"),
    "race_concept_id": p.get("extension[?url='http://hl7.org/fhir/StructureDefinition/us-core-race'].extension[0].valueString") >> p.lookup(race_code_lexicon),
    "ethnicity_concept_id": p.get("extension[?url='http://hl7.org/fhir/StructureDefinition/us-core-ethnicity'].extension[0].valueString") >> p.lookup(ethnicity_code_lexicon),
})

to_omop_person = Piper(source=Patient, target=Person, mapping=person_mapping)
