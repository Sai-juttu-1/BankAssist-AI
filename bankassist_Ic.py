"""BankAssist LLM and tool-calling workflow."""

import math
import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from banking_services import (
    check_loan_eligibility,
    get_customer_account,
    get_interest_rate,
)

load_dotenv(override=False)

SYSTEM = """
You are BankAssist, the AI assistant for the fictional Northwind Bank demo.

Your responsibilities:
- Answer banking questions clearly and in simple language.
- Use the available tools whenever a question requires an EMI calculation,
  an interest rate lookup, a basic loan eligibility check, or sample account
  information.
- Never invent tool results, rates, customer records, or calculations.
- If a required input for a tool is missing, ask the user for that input.
- Explain calculation assumptions and show currency amounts in INR.
- The sample rates and customer records are fictional demonstration data.
- The eligibility checker applies only simple demo rules. It is not a loan
  approval, credit decision, or financial recommendation.
- Never ask for or encourage sharing passwords, PINs, OTPs, or full card
  details.
- Do not claim that you accessed a real bank account or live banking system.

Fictional branch hours:
- Monday to Friday: 10:00 AM to 4:00 PM
- Saturday: 10:00 AM to 1:00 PM
- Sunday: Closed

Fictional rate card:
- Home loan: 8.5% floating, 9.0% fixed
- Personal loan: 12.0% floating, 13.0% fixed

Use the tools as the source of truth for rates, eligibility, account records,
and EMI calculations.
""".strip()


def _required_env(name: str) -> str:
    """Read a required environment variable with a helpful error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing {name} in your .env file. Please add {name}=..."
        )
    return value



llm = ChatOpenAI(
    model="bankassist",
    base_url=os.getenv("BASE_URL", "http://localhost:4000/v1"),
    api_key=_required_env("LITELLM_MASTER_KEY"),
    temperature=0,
    max_tokens=1500,
)



@tool
def calculate_emi(
    principal: float,
    annual_rate: float,
    tenure_months: int,
) -> str:
    """Calculate the monthly EMI for a loan.

    Args:
        principal: Loan principal amount in INR. Must be greater than zero.
        annual_rate: Annual interest rate as a percentage, such as 8.5.
        tenure_months: Loan duration in months. Must be greater than zero.

    Returns:
        Monthly EMI amount in INR, rounded to two decimal places.
    """
    if not math.isfinite(principal) or principal <= 0:
        return "Invalid principal: enter a loan amount greater than zero."

    if not math.isfinite(annual_rate) or annual_rate < 0:
        return "Invalid annual rate: enter a non-negative percentage."

    if tenure_months <= 0:
        return "Invalid tenure: enter a number of months greater than zero."

    monthly_rate = annual_rate / (12 * 100)

    # Handle a zero-interest loan separately to avoid division by zero.
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        factor = (1 + monthly_rate) ** tenure_months
        emi = principal * monthly_rate * factor / (factor - 1)

    return f"Estimated monthly EMI: INR {emi:,.2f}."


@tool
def get_rate(product: str, rate_type: str) -> str:
    """Look up the fictional Northwind Bank rate for a loan product.

    Args:
        product: Product name, such as home loan or personal loan.
        rate_type: Rate type, either floating or fixed.

    Returns:
        The matching annual interest rate or a not-available message.
    """
    rate = get_interest_rate(product, rate_type)

    if rate is None:
        return (
            f"Rate not available for '{product}' with rate type "
            f"'{rate_type}'. Supported products are home loan and "
            "personal loan; rate types are floating and fixed."
        )

    return (
        f"The fictional Northwind Bank {product.strip().lower()} "
        f"{rate_type.strip().lower()} rate is {rate:.2f}% per year."
    )


@tool
def check_eligibility(age: int, income: float, credit_score: int) -> str:
    """Check basic eligibility using the demo's illustrative rules.

    Args:
        age: Applicant age in years.
        income: Applicant annual income in INR.
        credit_score: Applicant credit score.

    Returns:
        A basic demo eligibility result, not a loan approval.
    """
    if age <= 0:
        return "Invalid age: enter a positive age."

    if not math.isfinite(income) or income < 0:
        return "Invalid income: enter a non-negative annual income."

    if credit_score < 0 or credit_score > 900:
        return "Invalid credit score: enter a score between 0 and 900."

    return check_loan_eligibility(age, income, credit_score)


@tool
def get_customer_account_tool(customer_id: str) -> str:
    """Get fictional demo account details for a customer.

    Args:
        customer_id: Sample customer ID, such as CUST001 or CUST002.

    Returns:
        Sample account details, or a not-found message.
    """
    account = get_customer_account(customer_id)
    if isinstance(account, str):
        return account

    return (
        "Fictional demo account record: "
        f"Name: {account['name']}; "
        f"Balance: INR {account['balance']:,.2f}; "
        f"Existing EMI: INR {account['existing_emi']:,.2f}; "
        f"Status: {account['account_status']}."
    )


TOOLS = {
    calculate_emi.name: calculate_emi,
    get_rate.name: get_rate,
    check_eligibility.name: check_eligibility,
    get_customer_account_tool.name: get_customer_account_tool,
}

llm_with_tools = llm.bind_tools(list(TOOLS.values()))


def execute_tool(tool_call: dict[str, Any]) -> ToolMessage:
    """Execute one model-requested tool and return its matching ToolMessage."""
    tool_name = tool_call.get("name", "")
    tool_args = tool_call.get("args", {})
    tool_call_id = tool_call.get("id")

    if not tool_call_id:
        raise ValueError("The model returned a tool call without an ID.")

    if tool_name not in TOOLS:
        result = f"Tool '{tool_name}' is not available."
    else:
        try:
            result = TOOLS[tool_name].invoke(tool_args)
        except Exception as error:
            result = f"Tool execution failed: {type(error).__name__}: {error}"

    return ToolMessage(
        content=str(result),
        tool_call_id=tool_call_id,
    )


def _message_content_to_text(content: Any) -> str:
    """Convert common LangChain message content formats into readable text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)

    return str(content)


def ask(
    model_with_tools,
    question: str,
    max_steps: int = 4,
) -> str:
    """Ask the model a question and run any requested tools."""
    if not question or not question.strip():
        return "Please enter a banking question."

    messages = [
        SystemMessage(content=SYSTEM),
        HumanMessage(content=question.strip()),
    ]

    for _ in range(max_steps):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        tool_calls = getattr(ai_message, "tool_calls", None) or []

        if not tool_calls:
            answer = _message_content_to_text(ai_message.content).strip()
            return answer or "I could not generate an answer. Please try again."

        for tool_call in tool_calls:
            messages.append(execute_tool(tool_call))

    return (
        "I could not complete the request within the tool-call limit. "
        "Please try asking in a simpler way."
    )


def stream_answer(
    model_with_tools,
    question: str,
    max_steps: int = 4,
):
    """Yield streamed answer chunks and tool traces for a chat UI."""
    if not question or not question.strip():
        yield "done", "Please enter a banking question."
        return

    messages = [
        SystemMessage(content=SYSTEM),
        HumanMessage(content=question.strip()),
    ]

    for _ in range(max_steps):
        ai_message = model_with_tools.invoke(messages)
        messages.append(ai_message)

        tool_calls = getattr(ai_message, "tool_calls", None) or []

        if not tool_calls:
            answer = _message_content_to_text(ai_message.content).strip()
            final_answer = answer or "I could not generate an answer. Please try again."
            yield "done", final_answer
            return

        for tool_call in tool_calls:
            tool_result = execute_tool(tool_call)
            tool_name = tool_call.get("name", "unknown_tool")
            tool_args = tool_call.get("args", {})
            trace = f"{tool_name}({tool_args}) -> {tool_result.content}"
            yield "tool", trace
            messages.append(tool_result)

    fallback = (
        "I could not complete the request within the tool-call limit. "
        "Please try asking in a simpler way."
    )
    yield "done", fallback