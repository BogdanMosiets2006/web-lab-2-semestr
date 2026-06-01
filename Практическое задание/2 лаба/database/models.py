from database.db import get_pool
from typing import Optional

# сохраняем или обновляем пользователя
async def upsert_user(user_id: int, username: str, full_name: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO users (id, username, full_name) VALUES (%s, %s, %s)
                   ON DUPLICATE KEY UPDATE username=%s, full_name=%s""",
                (user_id, username, full_name, username, full_name)
            )

# получаем список машин с пагинацией
async def get_cars(page: int = 1, per_page: int = 5):
    pool = await get_pool()
    offset = (page - 1) * per_page
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT COUNT(*) as cnt FROM cars")
            total = (await cur.fetchone())["cnt"]
            await cur.execute("SELECT * FROM cars ORDER BY brand, model LIMIT %s OFFSET %s", (per_page, offset))
            rows = await cur.fetchall()
    return rows, total

async def get_car(car_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM cars WHERE id=%s", (car_id,))
            return await cur.fetchone()

async def create_car(brand: str, model: str, year_from: int, year_to: int, description: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO cars (brand, model, year_from, year_to, description) VALUES (%s,%s,%s,%s,%s)",
                (brand, model, year_from, year_to, description)
            )
            return cur.lastrowid

async def update_car(car_id: int, brand: str, model: str, year_from: int, year_to: int, description: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE cars SET brand=%s, model=%s, year_from=%s, year_to=%s, description=%s WHERE id=%s",
                (brand, model, year_from, year_to, description, car_id)
            )

# TODO: добавить проверку на связанные товары перед удалением
async def delete_car(car_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM cars WHERE id=%s", (car_id,))

async def get_categories(page: int = 1, per_page: int = 5):
    pool = await get_pool()
    offset = (page - 1) * per_page
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT COUNT(*) as cnt FROM categories")
            total = (await cur.fetchone())["cnt"]
            await cur.execute("SELECT * FROM categories ORDER BY name LIMIT %s OFFSET %s", (per_page, offset))
            rows = await cur.fetchall()
    return rows, total

async def get_category(cat_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM categories WHERE id=%s", (cat_id,))
            return await cur.fetchone()

async def create_category(name: str, description: str, parent_id: Optional[int] = None):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO categories (name, description, parent_id) VALUES (%s,%s,%s)",
                (name, description, parent_id)
            )
            return cur.lastrowid

async def update_category(cat_id: int, name: str, description: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "UPDATE categories SET name=%s, description=%s WHERE id=%s",
                (name, description, cat_id)
            )

async def delete_category(cat_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM categories WHERE id=%s", (cat_id,))

# получаем товары, можно фильтровать по категории и авто
async def get_products(page: int = 1, per_page: int = 5, category_id: int = None, car_id: int = None):
    pool = await get_pool()
    offset = (page - 1) * per_page
    where_parts = []
    params = []
    if category_id:
        where_parts.append("p.category_id=%s")
        params.append(category_id)
    if car_id:
        where_parts.append("p.car_id=%s")
        params.append(car_id)
    where = ("WHERE " + " AND ".join(where_parts)) if where_parts else ""
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(f"SELECT COUNT(*) as cnt FROM products p {where}", params)
            total = (await cur.fetchone())["cnt"]
            await cur.execute(
                f"""SELECT p.*, c.name as category_name, ca.brand, ca.model
                    FROM products p
                    LEFT JOIN categories c ON p.category_id=c.id
                    LEFT JOIN cars ca ON p.car_id=ca.id
                    {where} ORDER BY p.name LIMIT %s OFFSET %s""",
                params + [per_page, offset]
            )
            rows = await cur.fetchall()
    return rows, total

async def get_product(product_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                """SELECT p.*, c.name as category_name, ca.brand, ca.model
                   FROM products p
                   LEFT JOIN categories c ON p.category_id=c.id
                   LEFT JOIN cars ca ON p.car_id=ca.id
                   WHERE p.id=%s""", (product_id,)
            )
            return await cur.fetchone()

async def create_product(name, description, price, stock, category_id, car_id, photo_url, article):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO products (name,description,price,stock,category_id,car_id,photo_url,article)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                (name, description, price, stock, category_id, car_id, photo_url, article)
            )
            return cur.lastrowid

async def update_product(product_id, name, description, price, stock, category_id, car_id, photo_url, article):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE products SET name=%s,description=%s,price=%s,stock=%s,
                   category_id=%s,car_id=%s,photo_url=%s,article=%s WHERE id=%s""",
                (name, description, price, stock, category_id, car_id, photo_url, article, product_id)
            )

async def delete_product(product_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM products WHERE id=%s", (product_id,))

# корзина пользователя
async def get_cart(user_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                """SELECT c.*, p.name, p.price, p.photo_url, p.stock,
                          (c.quantity * p.price) as subtotal
                   FROM cart c JOIN products p ON c.product_id=p.id
                   WHERE c.user_id=%s""", (user_id,)
            )
            return await cur.fetchall()

async def add_to_cart(user_id: int, product_id: int, quantity: int = 1):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO cart (user_id, product_id, quantity) VALUES (%s,%s,%s)
                   ON DUPLICATE KEY UPDATE quantity=quantity+%s""",
                (user_id, product_id, quantity, quantity)
            )

async def update_cart_item(user_id: int, product_id: int, quantity: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if quantity <= 0:
                await cur.execute("DELETE FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
            else:
                await cur.execute(
                    "UPDATE cart SET quantity=%s WHERE user_id=%s AND product_id=%s",
                    (quantity, user_id, product_id)
                )

async def clear_cart(user_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))

# создаём заказ
async def create_order(user_id: int, total_amount: float, delivery_address: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO orders (user_id, total_amount, delivery_address) VALUES (%s,%s,%s)",
                (user_id, total_amount, delivery_address)
            )
            return cur.lastrowid

# создаём заказ
async def create_order_items(order_id: int, items: list):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for item in items:
                await cur.execute(
                    "INSERT INTO order_items (order_id,product_id,quantity,price) VALUES (%s,%s,%s,%s)",
                    (order_id, item["product_id"], item["quantity"], item["price"])
                )
                await cur.execute(
                    "UPDATE products SET stock=stock-%s WHERE id=%s",
                    (item["quantity"], item["product_id"])
                )

async def get_orders(user_id: int, page: int = 1, per_page: int = 5):
    pool = await get_pool()
    offset = (page - 1) * per_page
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT COUNT(*) as cnt FROM orders WHERE user_id=%s", (user_id,))
            total = (await cur.fetchone())["cnt"]
            await cur.execute(
                "SELECT * FROM orders WHERE user_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (user_id, per_page, offset)
            )
            rows = await cur.fetchall()
    return rows, total

async def get_order_detail(order_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM orders WHERE id=%s", (order_id,))
            order = await cur.fetchone()
            await cur.execute(
                """SELECT oi.*, p.name FROM order_items oi
                   JOIN products p ON oi.product_id=p.id WHERE oi.order_id=%s""",
                (order_id,)
            )
            items = await cur.fetchall()
    return order, items

async def update_order_status(order_id: int, status: str, payment_id: str = None):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            if payment_id:
                await cur.execute(
                    "UPDATE orders SET status=%s, payment_id=%s WHERE id=%s",
                    (status, payment_id, order_id)
                )
            else:
                await cur.execute("UPDATE orders SET status=%s WHERE id=%s", (status, order_id))

async def get_all_orders_admin(page: int = 1, per_page: int = 5):
    pool = await get_pool()
    offset = (page - 1) * per_page
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT COUNT(*) as cnt FROM orders")
            total = (await cur.fetchone())["cnt"]
            await cur.execute(
                """SELECT o.*, u.username, u.full_name FROM orders o
                   JOIN users u ON o.user_id=u.id
                   ORDER BY o.created_at DESC LIMIT %s OFFSET %s""",
                (per_page, offset)
            )
            rows = await cur.fetchall()
    return rows, total

# логируем действие для статистики
async def log_action(user_id: int, action: str, details: str = ""):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO analytics (user_id, action, details) VALUES (%s,%s,%s)",
                (user_id, action, details)
            )

# статистика за период (дни)
async def get_stats(days: int = 1):
    pool = await get_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT COUNT(DISTINCT user_id) as visitors FROM analytics WHERE created_at >= NOW() - INTERVAL %s DAY",
                (days,)
            )
            visitors = (await cur.fetchone())["visitors"]
            await cur.execute(
                """SELECT COALESCE(SUM(oi.quantity),0) as sold
                   FROM order_items oi JOIN orders o ON oi.order_id=o.id
                   WHERE o.status IN ('paid','processing','shipped','delivered')
                   AND o.created_at >= NOW() - INTERVAL %s DAY""",
                (days,)
            )
            sold = (await cur.fetchone())["sold"]
            await cur.execute(
                """SELECT COALESCE(SUM(o.total_amount),0) as revenue
                   FROM orders o
                   WHERE o.status IN ('paid','processing','shipped','delivered')
                   AND o.created_at >= NOW() - INTERVAL %s DAY""",
                (days,)
            )
            revenue = (await cur.fetchone())["revenue"]
    return {"visitors": visitors, "sold": sold, "revenue": float(revenue)}

import aiomysql
