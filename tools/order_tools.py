"""
Agent tools - the concrete actions agents can take

Order Status Discovery (1 tool):
    - get_order_status: Retrieve the status of a user's order - order lookup by ID or email
"""
from __future__ import annotations

from langchain_core.tools import tool

from snackstack.logger import get_logger
from data.orders import ORDERS

logger = get_logger("order_tools")

def normalize_order_id(raw: str) -> str:
    """Accept 'ORD101', 'ORD-101', 'ord-101', or just '101' → 'ORD-101'."""
    upper = raw.upper().strip()
    clean = upper.replace("ORD-", "").replace("ORD", "").strip()
    return f"ORD-{clean}"

def lookup_order_by_email(email: str) -> dict | None:
    """Find the first order matching a customer email."""
    email_lower = email.lower().strip()
    for oid, order in ORDERS.items():
        if order["customer_email"].lower() == email_lower:
            return {"order_id": oid, **order}
    return None

# ═══════════════════════════════════════════════════════════
#  ORDER STATUS TOOLS
# ═══════════════════════════════════════════════════════════
@tool
def get_order_status(identifier: str) -> str:
    """
    Look up the current status of a customer order.

    Args:
        identifier: an order ID (e.g. "ORD101") OR a customer email address
    """
    logger.info("get_order_status  identifier=%r", identifier)

    # Try email first
    if "@" in identifier:
        match = lookup_order_by_email(identifier)
        if match:
            oid = match["order_id"]
            order = {k: v for k,v in match.items() if k != "order_id"}
        else:
            return f"No order found for the email: {identifier}"
    else:
        oid = normalize_order_id(identifier)
        order = ORDERS.get(oid)
        if not order:
            return f"Order {oid} not found. Please verify the order ID."

    info = (
        f"Order {oid}:\n"
        f"  Customer : {order['customer_name']} ({order['customer_email']})\n"
        f"  Product  : {order['item_name']}\n"
        f"  Price    : ₹{order['price']:,}\n"
        f"  Status   : {order['status']}\n"
        f"  Ordered  : {order['order_date']}\n"
        f"  ETA      : {order['estimated_delivery']}"
    )
    if order.get("delay_reason"):
        info += f"\n  Delay    : {order['delay_reason']}"

    return info
