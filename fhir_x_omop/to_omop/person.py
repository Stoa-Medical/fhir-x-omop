from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Piper
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon, race_code_lexicon, ethnicity_code_lexicon

person_mapping = DataMapping({
    "person_id": p.get("id") >> p.int(),
    "gender_concept_id": p.get("gender") >> p.lookup(gender_code_lexicon.inverse()) >> p.int() >> p.default(0),
    "year_of_birth": p.get("birthDate | split(@, '-')[0]") >> p.int(),
    "month_of_birth": p.get("birthDate | split(@, '-')[1]") >> p.int(),
    "day_of_birth": p.get("birthDate | split(@, '-')[2]") >> p.int(),
    "death_datetime": p.get("deceasedDateTime"),
    "race_concept_id": p.get("extension[?url=='http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'].extension[0].valueCoding.code") >> p.lookup(race_code_lexicon.inverse()) >> p.int() >> p.default(0),
    "ethnicity_concept_id": p.get("extension[?url=='http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'].extension[0].valueCoding.code") >> p.lookup(ethnicity_code_lexicon.inverse()) >> p.int() >> p.default(0),
})

to_omop_person = Piper(source=Patient, target=Person, mapping=person_mapping)
