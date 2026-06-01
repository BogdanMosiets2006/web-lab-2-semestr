import aiomysql
import logging
from typing import Optional

logger = logging.getLogger(__name__)
pool: Optional[aiomysql.Pool] = None

async def init_db():
    from config import config
    global pool
    pool = await aiomysql.create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db=config.DB_NAME,
        charset="utf8mb4",
        autocommit=True,
        minsize=1,
        maxsize=10,
    )
    logger.info("Database pool created")
    await create_tables()

async def get_pool() -> aiomysql.Pool:
    return pool

async def create_tables():
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    full_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    brand VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    year_from INT,
                    year_to INT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    description TEXT,
                    parent_id INT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    stock INT DEFAULT 0,
                    category_id INT,
                    car_id INT,
                    photo_url VARCHAR(500),
                    article VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
                    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE SET NULL
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_cart_item (user_id, product_id)
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    total_amount DECIMAL(10,2) NOT NULL,
                    status ENUM('pending','paid','processing','shipped','delivered','cancelled') DEFAULT 'pending',
                    payment_id VARCHAR(255),
                    delivery_address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """)
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT,
                    action VARCHAR(100),
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    logger.info("Tables created/verified")
