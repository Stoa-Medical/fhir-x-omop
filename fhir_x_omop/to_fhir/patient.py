from fhir.resources.patient import Patient
from omop_pydantic import Person

from chidian import DataMapping, Piper
from chidian.seeds import DROP
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon, race_code_lexicon, ethnicity_code_lexicon

patient_mapping = DataMapping({
    "resourceType": "Patient",
    "id": p.get("person_id") >> p.str(),
    "identifier": [{
        "use": "usual",
        "system": "http://omop.org/person",
        "value": p.get("person_id") >> p.str(),
    }],
    "gender": p.get("gender_concept_id") >> p.str() >> p.lookup(gender_code_lexicon) >> p.default("unknown"),
    "birthDate": p.get("[year_of_birth, month_of_birth?, day_of_birth?]") >> p.remove_empty() >> p.format_date("-"),
    "deceasedDateTime": p.get("death_datetime") >> p.when_exists() >> p.str() >> p.default(DROP.THIS_KEY),
    "extension": [
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race",
            "extension": [{
                "url": "ombCategory",
                "valueCoding": {
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": p.get("race_concept_id") >> p.str() >> p.lookup(race_code_lexicon) >> p.default("UNK"),
                    "display": p.case(p.get("race_concept_id") >> p.str() >> p.lookup(race_code_lexicon), {
                        "1002-5": "American Indian or Alaska Native",
                        "2028-9": "Asian",
                        "2054-5": "Black or African American",
                        "2076-8": "Native Hawaiian or Other Pacific Islander",
                        "2106-3": "White",
                        "UNK": "Unknown",
                    })
                }
            }]
        },
        {
            "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity",
            "extension": [{
                "url": "ombCategory",
                "valueCoding": {
                    "system": "urn:oid:2.16.840.1.113883.6.238",
                    "code": p.get("ethnicity_concept_id") >> p.str() >> p.lookup(ethnicity_code_lexicon) >> p.default("UNK"),
                    "display": p.case(p.get("ethnicity_concept_id") >> p.str() >> p.lookup(ethnicity_code_lexicon), {
                        "2135-2": "Hispanic or Latino",
                        "2186-5": "Not Hispanic or Latino",
                        "UNK": "Unknown",
                    })
                }
            }]
        }
    ]
})

to_fhir_patient = Piper(source=Person, target=Patient, mapping=patient_mapping)
