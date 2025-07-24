from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Mapper
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon, race_code_lexicon, ethnicity_code_lexicon

def format_birth_date(src):
    parts = [
        p.get("year_of_birth")(src),
        p.get("month_of_birth")(src),
        p.get("day_of_birth")(src),
    ]
    return "-".join(str(part) for part in parts if part is not None)

patient_mapper = Mapper(
    lambda src: {
        "resourceType": "Patient",
        "id": (p.get("person_id") | p.str())(src),
        "identifier": [{
            "use": "usual",
            "system": "http://omop.org/person",
            "value": (p.get("person_id") | p.str())(src),
        }],
        "gender": p.lookup(
            (p.get("gender_concept_id") | p.str())(src),
            gender_code_lexicon,
            default="unknown"
        ),
        "birthDate": format_birth_date(src),
        "deceasedDateTime": (p.get("death_datetime") | p.str())(src),
        "extension": [
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
                "extension": [{
                    "url": "ombCategory",
                    "valueCoding": {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": p.lookup(
                            (p.get("race_concept_id") | p.str())(src),
                            race_code_lexicon,
                            default="UNK"
                        ),
                        "display": p.case(p.lookup(
                            (p.get("race_concept_id") | p.str())(src),
                            race_code_lexicon,
                            default="UNK"
                        ), {
                            "1002-5": "American Indian or Alaska Native",
                            "2028-9": "Asian",
                            "2054-5": "Black or African American",
                            "2076-8": "Native Hawaiian or Other Pacific Islander",
                            "2106-3": "White",
                        }, default="Unknown")
                    }
                }]
            },
            {
                "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
                "extension": [{
                    "url": "ombCategory",
                    "valueCoding": {
                        "system": "urn:oid:2.16.840.1.113883.6.238",
                        "code": p.lookup(
                            (p.get("ethnicity_concept_id") | p.str())(src),
                            ethnicity_code_lexicon,
                            default="UNK"
                        ),
                        "display": p.case(p.lookup(
                            (p.get("ethnicity_concept_id") | p.str())(src),
                            ethnicity_code_lexicon,
                            default="UNK"
                        ), {
                            "2135-2": "Hispanic or Latino",
                            "2186-5": "Not Hispanic or Latino",
                        }, default="Unknown")
                    }
                }]
            }
        ]
    }
)

to_fhir_patient = DataMapping(
    mapper=patient_mapper,
    input_schema=Person,
    output_schema=Patient,
)
