"""
Seed script to populate the database with dummy data.
Usage: python seed_data.py
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add project root to path so imports work
sys.path.insert(0, os.path.dirname(__file__))

from faker import Faker
from app.db.database import SessionLocal, create_table, engine, Base
from app.models.users import User
from app.models.chat import ChatSession
from app.models.e_commerce import Category, Product, Customer, Order, OrderItem

fake = Faker()

# ---------- Configuration ----------
NUM_USERS = 10
NUM_CATEGORIES = 8
NUM_PRODUCTS = 40
NUM_CUSTOMERS = 25
NUM_ORDERS = 60
MAX_ITEMS_PER_ORDER = 5
NUM_CHAT_SESSIONS = 15


def seed_users(session):
    """Create users with hashed passwords."""
    roles = ["admin", "manager", "customer", "customer", "customer"]  # weighted toward customer
    users = []
    used_emails = set()
    used_usernames = set()

    for _ in range(NUM_USERS):
        # Ensure unique username and email
        username = fake.user_name()
        while username in used_usernames:
            username = fake.user_name()
        used_usernames.add(username)

        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        user = User(
            username=username,
            email=email,
            roles=random.choice(roles),
            created_at=fake.date_time_between(start_date="-1y", end_date="now"),
        )
        user.set_password("password123")  # default password for all seed users
        users.append(user)

    session.add_all(users)
    session.commit()
    print(f"  ✅ Created {len(users)} users")
    return users


def seed_categories(session):
    """Create product categories."""
    category_data = [
        ("Electronics", "Smartphones, laptops, tablets and accessories"),
        ("Clothing", "Men's and women's fashion apparel"),
        ("Home & Kitchen", "Furniture, appliances and home decor"),
        ("Books", "Fiction, non-fiction and educational books"),
        ("Sports & Outdoors", "Sports equipment and outdoor gear"),
        ("Beauty & Health", "Skincare, makeup and health products"),
        ("Toys & Games", "Children's toys and board games"),
        ("Automotive", "Car parts, tools and accessories"),
    ]

    categories = []
    for name, desc in category_data[:NUM_CATEGORIES]:
        cat = Category(name=name, description=desc)
        categories.append(cat)

    session.add_all(categories)
    session.commit()
    print(f"  ✅ Created {len(categories)} categories")
    return categories


def seed_products(session, categories):
    """Create products linked to categories."""
    product_templates = {
        "Electronics": [
            "Wireless Headphones", "Bluetooth Speaker", "USB-C Hub", "Laptop Stand",
            "Mechanical Keyboard", "Gaming Mouse", "Webcam HD", "Power Bank",
            "Smart Watch", "Tablet Case",
        ],
        "Clothing": [
            "Cotton T-Shirt", "Denim Jeans", "Winter Jacket", "Running Shoes",
            "Silk Scarf", "Leather Belt", "Wool Sweater", "Casual Shorts",
        ],
        "Home & Kitchen": [
            "Coffee Maker", "Blender Pro", "Cutting Board Set", "Non-Stick Pan",
            "Vacuum Cleaner", "LED Desk Lamp", "Storage Containers",
        ],
        "Books": [
            "Python Cookbook", "Data Science Handbook", "The Great Gatsby",
            "Clean Code", "Design Patterns", "AI Fundamentals",
        ],
        "Sports & Outdoors": [
            "Yoga Mat", "Dumbbell Set", "Camping Tent", "Water Bottle",
            "Running Armband", "Resistance Bands",
        ],
        "Beauty & Health": [
            "Face Moisturizer", "Sunscreen SPF50", "Vitamin C Serum",
            "Hair Dryer", "Electric Toothbrush",
        ],
        "Toys & Games": [
            "Building Blocks", "Board Game Classic", "Remote Control Car",
            "Puzzle 1000pc", "Card Game Pack",
        ],
        "Automotive": [
            "Car Phone Mount", "Dash Cam", "Tire Pressure Gauge",
            "Car Vacuum", "LED Headlight Bulbs",
        ],
    }

    products = []
    for cat in categories:
        templates = product_templates.get(cat.name, ["Generic Product"])
        for name in templates:
            if len(products) >= NUM_PRODUCTS:
                break
            product = Product(
                name=name,
                description=fake.sentence(nb_words=10),
                price=round(random.uniform(5.99, 499.99), 2),
                stock_quantity=random.randint(0, 200),
                category_id=cat.id,
            )
            products.append(product)

    session.add_all(products)
    session.commit()
    print(f"  ✅ Created {len(products)} products")
    return products


def seed_customers(session):
    """Create customers."""
    customers = []
    used_emails = set()

    for _ in range(NUM_CUSTOMERS):
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            address=fake.address().replace("\n", ", "),
            phone_number=fake.phone_number()[:20],
        )
        customers.append(customer)

    session.add_all(customers)
    session.commit()
    print(f"  ✅ Created {len(customers)} customers")
    return customers


def seed_orders(session, customers, products):
    """Create orders with order items. Totals are calculated from items."""
    statuses = ["pending", "paid", "shipped"]
    orders = []

    for _ in range(NUM_ORDERS):
        customer = random.choice(customers)
        order_date = fake.date_time_between(start_date="-6m", end_date="now")

        order = Order(
            customer_id=customer.id,
            status=random.choice(statuses),
            total_price=0,
            total_mount=0,
            created_at=order_date,
            order_date=order_date,
            shipping_address=fake.address().replace("\n", ", "),
        )
        session.add(order)
        session.flush()  # get order.id

        # Create 1-5 items per order
        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        selected_products = random.sample(products, min(num_items, len(products)))
        order_total = 0.0

        for prod in selected_products:
            qty = random.randint(1, 5)
            item_price = prod.price
            item = OrderItem(
                order_id=order.id,
                product_id=prod.id,
                quantity=qty,
                price=item_price,
            )
            session.add(item)
            order_total += item_price * qty

        order.total_price = round(order_total, 2)
        order.total_mount = round(order_total, 2)
        orders.append(order)

    session.commit()
    print(f"  ✅ Created {len(orders)} orders with items")
    return orders


def seed_chat_sessions(session, users):
    """Create chat session history."""
    sample_questions = [
        "How many orders do we have?",
        "What is the total revenue?",
        "Which product has the highest stock?",
        "Show me the most popular category",
        "How many customers signed up this month?",
        "What is the average order value?",
        "List all pending orders",
        "Which customer placed the most orders?",
        "What are the top 5 selling products?",
        "Show me revenue by category",
    ]

    sample_responses = [
        "We currently have 60 orders in the system! 🎉",
        "The total revenue is $12,450.00 💰",
        "The Wireless Headphones have the highest stock with 200 units 📦",
        "Electronics is the most popular category! ⚡",
        "15 new customers signed up this month 🙌",
        "The average order value is $207.50 📊",
        "There are 20 pending orders awaiting processing 📋",
        "John Smith placed the most orders with 8 purchases 🏆",
        "Top sellers: Headphones, Keyboard, Mouse, Speaker, Webcam 🔥",
        "Electronics: $5,200 | Clothing: $3,100 | Home: $2,800 📈",
    ]

    sessions = []
    for _ in range(NUM_CHAT_SESSIONS):
        user = random.choice(users)
        q = random.choice(sample_questions)
        r = random.choice(sample_responses)

        chat = ChatSession(
            user_id=user.id,
            session_name=f"Chat {fake.date_this_month().strftime('%Y-%m-%d')}",
            question=q,
            responses=r,
            created_at=fake.date_time_between(start_date="-1m", end_date="now"),
        )
        sessions.append(chat)

    session.add_all(sessions)
    session.commit()
    print(f"  ✅ Created {len(sessions)} chat sessions")
    return sessions


def main():
    print("\n🌱 Seeding database...\n")

    # Ensure all tables exist
    create_table()

    session = SessionLocal()
    try:
        # Clear existing data (in reverse dependency order)
        # session.query(OrderItem).delete()
        # session.query(Order).delete()
        # session.query(ChatSession).delete()
        # session.query(Product).delete()
        # session.query(Category).delete()
        # session.query(Customer).delete()
        # session.query(User).delete()
        # session.commit()
        # print("  🗑️  Cleared existing data\n")

        # Seed in dependency order
        users = seed_users(session)
        categories = seed_categories(session)
        products = seed_products(session, categories)
        customers = seed_customers(session)
        orders = seed_orders(session, customers, products)
        chat_sessions = seed_chat_sessions(session, users)

        print(f"\n✅ Seeding complete!")
        print(f"   Users: {len(users)}")
        print(f"   Categories: {len(categories)}")
        print(f"   Products: {len(products)}")
        print(f"   Customers: {len(customers)}")
        print(f"   Orders: {len(orders)}")
        print(f"   Chat Sessions: {len(chat_sessions)}")
        print(f"\n   🔑 All users have password: 'password123'\n")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
