from fhir.resources.practitioner import Practitioner
from omop_pydantic import Provider

from chidian import DataMapping, Piper
from chidian.seeds import DROP
import chidian.partials as p

from ..lexicons.lib import gender_code_lexicon

practitioner_mapping = DataMapping({
    "resourceType": "Practitioner",
    "id": p.get("provider_id") >> p.str(),
    "identifier": [{
        "system": "http://hl7.org/fhir/sid/us-npi",
        "value": p.get("npi") >> p.str(),
    }],
    "name": [{
        "use": "official",
        "family": p.get("provider_name | split(@, ' ')[-1]"),
        "given": [p.get("provider_name | split(@, ' ')[0]")],
    }],
    "gender": p.get("gender_source_value") >> p.lower() >> p.default("unknown"),
    "birthDate": p.get("year_of_birth") >> p.str(),
    "qualification": [{
        "code": {
            "coding": [{
                "system": "http://nucc.org/provider-taxonomy",
                "code": p.get("specialty_source_value"),
                "display": p.get("specialty_source_value"),
            }]
        }
    }],
})

to_fhir_practitioner = Piper(source=Provider, target=Practitioner, mapping=practitioner_mapping)