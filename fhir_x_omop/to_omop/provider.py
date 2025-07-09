from fhir.resources.practitioner import Practitioner
from omop_pydantic import Provider

from chidian import DataMapping, Piper
import chidian.partials as p

def get_provider_name(name_list):
    if not name_list:
        return None
    name = name_list[0]
    given = " ".join(name.given) if name.given else ""
    family = name.family or ""
    return f"{given} {family}".strip()

def get_npi(identifier_list):
    if not identifier_list:
        return None
    for identifier in identifier_list:
        if identifier.system == 'http://hl7.org/fhir/sid/us-npi':
            return identifier.value
    return None

provider_piper = Piper(
    lambda src: {
        "provider_id": (p.get("id") >> p.int())(src),
        "provider_source_value": p.get("id")(src),
        "provider_name": p.get("name", getter=get_provider_name)(src),
        "npi": p.get("identifier", getter=get_npi)(src),
        "gender_source_value": p.get("gender", getter=lambda x: x.upper() if x else None)(src),
        "year_of_birth": p.get("birthDate", getter=lambda x: int(x.split('-')[0]) if x else None)(src),
        "specialty_source_value": p.get("qualification[0].code.coding[0].code")(src),
    }
)

to_omop_provider = DataMapping(
    piper=provider_piper,
    input_schema=Practitioner,
    output_schema=Provider,
)