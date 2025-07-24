from fhir.resources.practitioner import Practitioner
from omop_pydantic import Provider

from chidian import DataMapping, Mapper
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon

practitioner_mapper = Mapper(
    lambda src: {
        "resourceType": "Practitioner",
        "id": (p.get("provider_id") | p.str())(src),
        "identifier": [{
            "system": "http://hl7.org/fhir/sid/us-npi",
            "value": p.get("npi")(src),
        }],
        "name": [{
            "use": "official",
            "family": p.get("provider_name", getter=lambda x: x.split(' ')[-1] if x else None)(src),
            "given": [p.get("provider_name", getter=lambda x: x.split(' ')[0] if x else None)(src)],
        }],
        "gender": p.get("gender_source_value", getter=lambda x: x.lower() if x else "unknown")(src),
        "birthDate": (p.get("year_of_birth") | p.str())(src),
        "qualification": [{
            "code": {
                "coding": [{
                    "system": "http://nucc.org/provider-taxonomy",
                    "code": p.get("specialty_source_value")(src),
                    "display": p.get("specialty_source_value")(src),
                }]
            }
        }],
    }
)

to_fhir_practitioner = DataMapping(
    mapper=practitioner_mapper,
    input_schema=Provider,
    output_schema=Practitioner,
)