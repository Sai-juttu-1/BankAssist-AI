"""Lightweight question router for BankAssist."""

TOOL_KEYWORDS = (
    "emi",
    "monthly installment",
    "monthly payment",
    "calculate",
    "interest rate",
    "floating rate",
    "fixed rate",
    "eligibility",
    "eligible",
    "credit score",
    "loan rate",
    "account details",
    "account balance",
    "customer account",
)


def route_question(question: str) -> str:
    """
    Classify a question for display/observability.

    The LLM tool-calling loop remains responsible for deciding whether a
    tool is actually required. This router does not execute any tool.
    """
    normalized_question = question.casefold()

    if any(keyword in normalized_question for keyword in TOOL_KEYWORDS):
        return "TOOL"

    return "NO_TOOL"


if __name__ == "__main__":
    examples = [
        "Hello, how are you?",
        "Calculate EMI for 25 lakhs",
        "What is the home loan floating interest rate?",
        "Show account details for CUST001",
    ]

    for example in examples:
        print(f"{example} -> {route_question(example)}")
