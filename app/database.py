import sqlite3

DATABASE_NAME = "finmark.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL UNIQUE,
            service_category TEXT NOT NULL,
            description TEXT NOT NULL,
            base_price REAL NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            client_type TEXT NOT NULL,
            service_id INTEGER NOT NULL,
            order_status TEXT NOT NULL DEFAULT 'pending',
            order_notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_id) REFERENCES service_catalog(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'pending',
            payment_method TEXT NOT NULL DEFAULT 'simulation',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES service_orders(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            actor_email TEXT,
            details TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS event_bus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            source_service TEXT NOT NULL,
            payload TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'recorded',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    seed_service_catalog(cursor)

    connection.commit()
    connection.close()


def seed_service_catalog(cursor):
    services = [
        (
            "Financial Analysis",
            "Finance",
            "Detailed financial analysis to assess financial health, uncover growth opportunities, and optimize resources.",
            25000.00
        ),
        (
            "Marketing Analytics",
            "Marketing",
            "Market and customer behavior analytics to support stronger campaigns and improve ROI.",
            30000.00
        ),
        (
            "Business Intelligence",
            "Business Intelligence",
            "Custom dashboards and reports that turn raw business data into actionable insights.",
            40000.00
        ),
        (
            "Consulting Services",
            "Consulting",
            "Strategic consulting for SMEs in retail, e-commerce, healthcare, and manufacturing.",
            35000.00
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO service_catalog (
            service_name,
            service_category,
            description,
            base_price
        )
        VALUES (?, ?, ?, ?)
    """, services)


def create_user(name, email, password_hash, role, department):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password_hash, role, department)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, password_hash, role, department))

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    return user_id


def find_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    connection.close()

    return dict(user) if user else None


def get_service_catalog():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM service_catalog
        WHERE is_active = 1
        ORDER BY service_name
    """)

    services = cursor.fetchall()
    connection.close()

    return [dict(service) for service in services]


def find_service_by_id(service_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM service_catalog
        WHERE id = ? AND is_active = 1
    """, (service_id,))

    service = cursor.fetchone()
    connection.close()

    return dict(service) if service else None


def create_service_order(customer_name, customer_email, client_type, service_id, order_notes):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO service_orders (
            customer_name,
            customer_email,
            client_type,
            service_id,
            order_notes
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        customer_name,
        customer_email,
        client_type,
        service_id,
        order_notes
    ))

    connection.commit()
    order_id = cursor.lastrowid
    connection.close()

    return order_id


def get_service_orders():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            service_orders.id,
            service_orders.customer_name,
            service_orders.customer_email,
            service_orders.client_type,
            service_orders.order_status,
            service_orders.order_notes,
            service_orders.created_at,
            service_catalog.service_name,
            service_catalog.service_category,
            service_catalog.base_price
        FROM service_orders
        JOIN service_catalog
            ON service_orders.service_id = service_catalog.id
        ORDER BY service_orders.created_at DESC
    """)

    orders = cursor.fetchall()
    connection.close()

    return [dict(order) for order in orders]


def create_payment(order_id, amount, payment_status="pending", payment_method="simulation"):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO payments (
            order_id,
            amount,
            payment_status,
            payment_method
        )
        VALUES (?, ?, ?, ?)
    """, (
        order_id,
        amount,
        payment_status,
        payment_method
    ))

    connection.commit()
    payment_id = cursor.lastrowid
    connection.close()

    return payment_id


def get_payments():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM payments
        ORDER BY created_at DESC
    """)

    payments = cursor.fetchall()
    connection.close()

    return [dict(payment) for payment in payments]


def create_audit_log(action, actor_email=None, details=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (
            action,
            actor_email,
            details
        )
        VALUES (?, ?, ?)
    """, (
        action,
        actor_email,
        details
    ))

    connection.commit()
    log_id = cursor.lastrowid
    connection.close()

    return log_id


def get_audit_logs(limit=50):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    logs = cursor.fetchall()
    connection.close()

    return [dict(log) for log in logs]


def create_event(event_type, source_service, payload, status="recorded"):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO event_bus (
            event_type,
            source_service,
            payload,
            status
        )
        VALUES (?, ?, ?, ?)
    """, (
        event_type,
        source_service,
        payload,
        status
    ))

    connection.commit()
    event_id = cursor.lastrowid
    connection.close()

    return event_id


def get_events(limit=50):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM event_bus
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    events = cursor.fetchall()
    connection.close()

    return [dict(event) for event in events]