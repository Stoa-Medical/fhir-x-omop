from fhir.resources.claim import Claim
from omop_pydantic import Cost

from chidian import DataMapping, Piper
import chidian.partials as p

cost_mapping = DataMapping({
    "cost_id": p.get("id") >> p.int(),
    "cost_event_id": p.get("id") >> p.int(),
    "cost_domain_id": p.case(p.get("type.coding[0].code"), {
        "institutional": "Visit",
        "professional": "Procedure",
        "pharmacy": "Drug",
        "default": "Procedure"
    }),
    "cost_type_concept_id": p.case(p.get("type.coding[0].code"), {
        "institutional": 32810,
        "professional": 32812,
        "pharmacy": 32813,
        "default": 32814
    }),
    "currency_concept_id": 44818668,  # USD
    "total_charge": p.get("total.value") >> p.float(),
    "total_cost": p.get("total.value") >> p.float(),
    "total_paid": p.get("payment.amount.value | item[*].adjudication[?category.coding[0].code=='benefit'].amount.value | sum(@)") >> p.float(),
    "paid_by_payer": p.get("payment.amount.value | item[*].adjudication[?category.coding[0].code=='benefit'].amount.value | sum(@)") >> p.float(),
    "paid_by_patient": p.get("item[*].adjudication[?category.coding[0].code=='copay'].amount.value | sum(@)") >> p.float(),
    "paid_patient_copay": p.get("item[*].adjudication[?category.coding[0].code=='copay'].amount.value | sum(@)") >> p.float(),
    "paid_patient_coinsurance": p.get("item[*].adjudication[?category.coding[0].code=='coins'].amount.value | sum(@)") >> p.float(),
    "paid_patient_deductible": p.get("item[*].adjudication[?category.coding[0].code=='deductible'].amount.value | sum(@)") >> p.float(),
    "paid_by_primary": p.get("insurance[?focal==`true`].coverage.display | [0]"),
    "paid_ingredient_cost": p.get("item[*].net.value | sum(@)") >> p.float(),
    "paid_dispensing_fee": p.get("item[*].adjudication[?category.coding[0].code=='dispensefee'].amount.value | sum(@)") >> p.float(),
    "payer_plan_period_id": p.get("insurance[0].coverage.reference | split(@, '/')[1]") >> p.int(),
    "amount_allowed": p.get("item[*].adjudication[?category.coding[0].code=='eligible'].amount.value | sum(@)") >> p.float(),
    "revenue_code_concept_id": 0,
    "revenue_code_source_value": p.get("item[0].revenue.coding[0].code"),
    "drg_concept_id": 0,
    "drg_source_value": p.get("diagnosis[0].diagnosisReference.reference | split(@, '/')[1]"),
})

to_omop_cost = Piper(source=Claim, target=Cost, mapping=cost_mapping)