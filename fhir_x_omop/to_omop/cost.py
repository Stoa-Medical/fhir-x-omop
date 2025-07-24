from fhir.resources.claim import Claim
from omop_pydantic import Cost

from chidian import DataMapping, Mapper
import chidian.partials as p

def get_adjudication_sum(items, category):
    total = 0
    if not items:
        return None
    for item in items:
        if item.adjudication:
            for adj in item.adjudication:
                if adj.category.coding and adj.category.coding[0].code == category and adj.amount:
                    total += adj.amount.value
    return total

def get_total_paid(src):
    payment_value = p.get("payment.amount.value")(src)
    if payment_value is not None:
        return float(payment_value)
    
    benefit_sum = get_adjudication_sum(p.get("item")(src), 'benefit')
    if benefit_sum is not None:
        return float(benefit_sum)
    return None

cost_mapper = Mapper(
    lambda src: {
        "cost_id": (p.get("id") | p.int())(src),
        "cost_event_id": (p.get("id") | p.int())(src),
        "cost_domain_id": p.case(p.get("type.coding[0].code")(src), {
            "institutional": "Visit",
            "professional": "Procedure",
            "pharmacy": "Drug",
        }, default="Procedure"),
        "cost_type_concept_id": p.case(p.get("type.coding[0].code")(src), {
            "institutional": 32810,
            "professional": 32812,
            "pharmacy": 32813,
        }, default=32814),
        "currency_concept_id": 44818668,  # USD
        "total_charge": (p.get("total.value") | p.float())(src),
        "total_cost": (p.get("total.value") | p.float())(src),
        "total_paid": get_total_paid(src),
        "paid_by_payer": get_total_paid(src), # Same logic as total_paid
        "paid_by_patient": p.get("item", getter=lambda x: get_adjudication_sum(x, 'copay') or 0.0)(src),
        "paid_patient_copay": p.get("item", getter=lambda x: get_adjudication_sum(x, 'copay') or 0.0)(src),
        "paid_patient_coinsurance": p.get("item", getter=lambda x: get_adjudication_sum(x, 'coins') or 0.0)(src),
        "paid_patient_deductible": p.get("item", getter=lambda x: get_adjudication_sum(x, 'deductible') or 0.0)(src),
        "paid_by_primary": p.get("insurance[?focal==`true`].coverage.display[0]")(src), # This JMESPath might need a custom getter
        "paid_ingredient_cost": p.get("item", getter=lambda items: sum(i.net.value for i in items if i.net and i.net.value) if items else None)(src),
        "paid_dispensing_fee": p.get("item", getter=lambda x: get_adjudication_sum(x, 'dispensefee'))(src),
        "payer_plan_period_id": p.get("insurance[0].coverage.reference", getter=lambda x: int(x.split('/')[1]) if x else None)(src),
        "amount_allowed": p.get("item", getter=lambda x: get_adjudication_sum(x, 'eligible'))(src),
        "revenue_code_concept_id": 0,
        "revenue_code_source_value": p.get("item[0].revenue.coding[0].code")(src),
        "drg_concept_id": 0,
        "drg_source_value": p.get("diagnosis[0].diagnosisReference.reference", getter=lambda x: x.split('/')[1] if x else None)(src),
    }
)

to_omop_cost = DataMapping(
    mapper=cost_mapper,
    input_schema=Claim,
    output_schema=Cost,
)