# fhir-x-omop

> [!NOTE]
> This repo is for demonstration purposes only and is still a work-in-progress, though it'll remain open-source, and this will continue to be updated!

A bi-directional, composable mapping between FHIR R4 and OMOP CDM 5.3 ... in code! (WIP)

Usage:
```python
from fhir.resources.patient import Patient
from omop_pydantic import Person
from fhir_x_omop.to_omop import to_omop_person
from fhir_x_omop.to_fhir import to_fhir_patient

fhir_patient = Patient(**{"resourceType": "Patient", ...})

# Convert to OMOP
omop_person: Person = to_omop_person(fhir_patient)

# Re-convert to FHIR
fhir_patient_recovered: Patient = to_fhir_patient(omop_person)
```

To view/modify mappings:
```python
from fhir_x_omop.to_omop import to_omop_person
from copy import deepcopy

print(to_omop_person.mapping) # { "Id": "id", ... }

to_omop_person_custom = deepcopy(to_omop_person)
to_omop_person_custom.mapping["Id"] = "identifier[0].value"  # Override the default path mapping
```

To do a lossless mapping, we can keep the orignal data when converting:
```python
...

# Convert to OMOP
omop_person, extra: tuple[Person, dict] = to_omop_person(fhir_patient, output_extra=True)

# Re-convert to FHIR
fhir_patient_recovered_lossless: Patient = to_fhir_patient(omop_person, input_extra=extra)

assert fhir_patient == fhir_patient_recovered_lossless
```

