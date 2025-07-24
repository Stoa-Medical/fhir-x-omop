from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Mapper
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon, race_code_lexicon, ethnicity_code_lexicon

def get_extension_value(extensions, url):
    if not extensions:
        return None
    for ext in extensions:
        if ext.url == url and ext.extension:
            return ext.extension[0].valueCoding.code
    return None

gender_code_lexicon_inv = {v: k for k, v in gender_code_lexicon.items()}
race_code_lexicon_inv = {v: k for k, v in race_code_lexicon.items()}
ethnicity_code_lexicon_inv = {v: k for k, v in ethnicity_code_lexicon.items()}

person_mapper = Mapper(
    lambda src: {
        "person_id": (p.get("id") | p.int())(src),
        "gender_concept_id": (p.get("gender") | p.lookup(gender_code_lexicon_inv, default=0) | p.int())(src),
        "year_of_birth": p.get("birthDate", getter=lambda x: int(x.split('-')[0]) if x else None)(src),
        "month_of_birth": p.get("birthDate", getter=lambda x: int(x.split('-')[1]) if x and len(x.split('-')) > 1 else None)(src),
        "day_of_birth": p.get("birthDate", getter=lambda x: int(x.split('-')[2]) if x and len(x.split('-')) > 2 else None)(src),
        "death_datetime": p.get("deceasedDateTime")(src),
        "race_concept_id": (
            p.get("extension", getter=lambda x: get_extension_value(x, 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-race'))
            | p.lookup(race_code_lexicon_inv, default=0) 
            | p.int()
        )(src),
        "ethnicity_concept_id": (
            p.get("extension", getter=lambda x: get_extension_value(x, 'http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity'))
            | p.lookup(ethnicity_code_lexicon_inv, default=0)
            | p.int()
        )(src),
    }
)

to_omop_person = DataMapping(
    mapper=person_mapper,
    input_schema=Patient,
    output_schema=Person,
)

