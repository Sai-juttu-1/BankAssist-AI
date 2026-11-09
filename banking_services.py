"""
Northwind Bank demo services.

All rates and customer records in this module are fictional sample data.
Do not use this module for real banking decisions or customer records.
"""

BANK_RATES = {
    "home loan": {
        "floating": 8.5,
        "fixed": 9.0,
    },
    "personal loan": {
        "floating": 12.0,
        "fixed": 13.0,
    },
}

# Fictional demonstration records only.
CUSTOMER_ACCOUNTS = {
    "CUST001": {
        "name": "Rahul",
        "balance": 50000,
        "existing_emi": 12000,
        "account_status": "Active",
    },
    "CUST002": {
        "name": "Priya",
        "balance": 75000,
        "existing_emi": 8000,
        "account_status": "Active",
    },
}


def _normalize_product(product: str) -> str:
    """Normalize common product-name variations."""
    value = product.strip().lower()
    aliases = {
        "home loans": "home loan",
        "housing loan": "home loan",
        "housing loans": "home loan",
        "personal loans": "personal loan",
    }
    return aliases.get(value, value)


def get_interest_rate(product: str, rate_type: str):
    """Return a configured rate, or None when no matching rate exists."""
    normalized_product = _normalize_product(product)
    normalized_rate_type = rate_type.strip().lower()

    if normalized_rate_type not in {"fixed", "floating"}:
        return None

    return BANK_RATES.get(normalized_product, {}).get(normalized_rate_type)


def check_loan_eligibility(age: int, income: float, credit_score: int) -> str:
    """
    Apply the demo's basic eligibility rules.

    These are illustrative rules, not an actual bank underwriting policy.
    """
    if age < 21 or age > 60:
        return "Not Eligible: age must be between 21 and 60."

    if income < 250000:
        return "Not Eligible: annual income must be at least INR 250,000."

    if credit_score < 650:
        return "Not Eligible: credit score must be at least 650."

    return (
        "Eligible under the demo's basic criteria. "
        "This is not a loan approval or a credit decision."
    )


def get_customer_account(customer_id: str):
    """Return a fictional sample account or a not-found message."""
    normalized_id = customer_id.strip().upper()
    account = CUSTOMER_ACCOUNTS.get(normalized_id)

    if account is None:
        return "Customer account not found in the fictional demo dataset."

    # Return a copy so callers cannot modify the in-memory source record.
    return dict(account)
