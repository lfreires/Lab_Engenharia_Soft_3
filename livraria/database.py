import sqlite3


def get_connection(db_path: str = "livraria.db") -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL CHECK (stock >= 0)
        );

        CREATE TABLE IF NOT EXISTS carts (
            id TEXT PRIMARY KEY
        );

        CREATE TABLE IF NOT EXISTS cart_items (
            cart_id TEXT NOT NULL,
            book_id TEXT NOT NULL,
            title TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price REAL NOT NULL,
            PRIMARY KEY (cart_id, book_id),
            FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id)
        );

        CREATE TABLE IF NOT EXISTS coupons (
            code TEXT PRIMARY KEY,
            discount_pct REAL NOT NULL CHECK (discount_pct > 0 AND discount_pct <= 100),
            active INTEGER NOT NULL DEFAULT 1,
            single_use INTEGER NOT NULL DEFAULT 0,
            used INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            total REAL NOT NULL,
            status TEXT NOT NULL,
            coupon_code TEXT REFERENCES coupons(code)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            order_id TEXT NOT NULL,
            book_id TEXT NOT NULL,
            title TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS payments (
            order_id TEXT PRIMARY KEY,
            amount REAL NOT NULL,
            method TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );
        """
    )

    # Migração: adiciona coupon_code em bases que existiam antes desta versão
    try:
        connection.execute("ALTER TABLE orders ADD COLUMN coupon_code TEXT REFERENCES coupons(code)")
        connection.commit()
    except sqlite3.OperationalError:
        pass
