from fhir.resources.practitioner import Practitioner
from omop_pydantic import Provider

from chidian import DataMapping, Piper
import chidian.partials as p


provider_mapping = DataMapping({
    "provider_id": p.get("id") >> p.int(),
    "provider_source_value": p.get("id"),
    "provider_name": p.get("name[0] | join(' ', [given[0], family])"),
    "npi": p.get("identifier[?system=='http://hl7.org/fhir/sid/us-npi'].value | [0]"),
    "gender_source_value": p.get("gender") >> p.upper(),
    "year_of_birth": p.get("birthDate | split(@, '-')[0]") >> p.int(),
    "specialty_source_value": p.get("qualification[0].code.coding[0].code"),
})

to_omop_provider = Piper(source=Practitioner, target=Provider, mapping=provider_mapping)