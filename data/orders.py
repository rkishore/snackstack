"""
Static data for orders

In production, these would come from a persistent store like a database. Keeping it simple
here to focus first on the core functionality.

Each order has: order_id, item_id, item_name, customer_name, customer_email, status,
price (INR), order_date, estimated_delivery, and tracking_id. Defined as a Python
dictionary keyed by order_id.

"""

orders: dict[str, dict] = {
    "ORD-201": {
        "order_id": "ORD-201",
        "item_id": "MENU003",
        "item_name": "Butter Chicken",
        "customer_name": "Priya Nair",
        "customer_email": "priya@example.com",
        "status": "Out for Delivery",
        "price": 379,
        "order_date": "2026-06-23",
        "estimated_delivery": "2026-06-23",
        "tracking_id": "SS201TRK",
    },
    "ORD-202": {
        "order_id": "ORD-202",
        "item_id": "MENU001",
        "item_name": "Margherita Pizza",
        "customer_name": "Arjun Mehta",
        "customer_email": "arjun@example.com",
        "status": "Placed",
        "price": 299,
        "order_date": "2026-06-23",
        "estimated_delivery": "2026-06-24",
        "tracking_id": "SS202TRK",
    },
    "ORD-203": {
        "order_id": "ORD-203",
        "item_id": "MENU005",
        "item_name": "Classic Cheeseburger",
        "customer_name": "Sneha Roy",
        "customer_email": "sneha@example.com",
        "status": "Preparing",
        "price": 259,
        "order_date": "2026-06-23",
        "estimated_delivery": "2026-06-23",
        "tracking_id": "SS203TRK",
    },
    "ORD-204": {
        "order_id": "ORD-204",
        "item_id": "MENU004",
        "item_name": "Vegan Buddha Bowl",
        "customer_name": "Rahul Das",
        "customer_email": "rahul@example.com",
        "status": "Delivered",
        "price": 319,
        "order_date": "2026-06-21",
        "estimated_delivery": "2026-06-22",
        "tracking_id": "SS204TRK",
    },
    "ORD-205": {
        "order_id": "ORD-205",
        "item_id": "MENU006",
        "item_name": "Paneer Tikka",
        "customer_name": "Kavya Sharma",
        "customer_email": "kavya@example.com",
        "status": "Placed",
        "price": 199,
        "order_date": "2026-06-23",
        "estimated_delivery": "2026-06-24",
        "tracking_id": "SS205TRK",
    },
}
