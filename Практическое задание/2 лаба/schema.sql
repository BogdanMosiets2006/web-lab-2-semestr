-- ============================================================
-- AutoParts Shop — MySQL Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS autoparts_shop
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE autoparts_shop;

-- ─── USERS ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         BIGINT       NOT NULL COMMENT 'Telegram user ID',
    username   VARCHAR(255) DEFAULT NULL,
    full_name  VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CARS ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cars (
    id          INT          NOT NULL AUTO_INCREMENT,
    brand       VARCHAR(100) NOT NULL,
    model       VARCHAR(100) NOT NULL,
    year_from   INT          DEFAULT NULL,
    year_to     INT          DEFAULT NULL COMMENT 'NULL = still produced',
    description TEXT         DEFAULT NULL,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_brand_model (brand, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CATEGORIES ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categories (
    id          INT          NOT NULL AUTO_INCREMENT,
    name        VARCHAR(150) NOT NULL,
    description TEXT         DEFAULT NULL,
    parent_id   INT          DEFAULT NULL COMMENT 'Self-reference for sub-categories',
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── PRODUCTS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS products (
    id          INT             NOT NULL AUTO_INCREMENT,
    name        VARCHAR(255)    NOT NULL,
    description TEXT            DEFAULT NULL,
    price       DECIMAL(10, 2)  NOT NULL,
    stock       INT             DEFAULT 0,
    category_id INT             DEFAULT NULL,
    car_id      INT             DEFAULT NULL,
    photo_url   VARCHAR(500)    DEFAULT NULL,
    article     VARCHAR(100)    DEFAULT NULL,
    created_at  TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    FOREIGN KEY (car_id)      REFERENCES cars(id)       ON DELETE SET NULL,
    INDEX idx_category (category_id),
    INDEX idx_car      (car_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── CART ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cart (
    id         INT       NOT NULL AUTO_INCREMENT,
    user_id    BIGINT    NOT NULL,
    product_id INT       NOT NULL,
    quantity   INT       DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_cart_item (user_id, product_id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── ORDERS ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS orders (
    id               INT             NOT NULL AUTO_INCREMENT,
    user_id          BIGINT          NOT NULL,
    total_amount     DECIMAL(10, 2)  NOT NULL,
    status           ENUM('pending','paid','processing','shipped','delivered','cancelled')
                                     DEFAULT 'pending',
    payment_id       VARCHAR(255)    DEFAULT NULL,
    delivery_address TEXT            DEFAULT NULL,
    created_at       TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMP       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_orders  (user_id),
    INDEX idx_order_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── ORDER ITEMS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS order_items (
    id         INT            NOT NULL AUTO_INCREMENT,
    order_id   INT            NOT NULL,
    product_id INT            NOT NULL,
    quantity   INT            NOT NULL,
    price      DECIMAL(10, 2) NOT NULL COMMENT 'Price at time of order',
    PRIMARY KEY (id),
    FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── ANALYTICS ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS analytics (
    id         INT          NOT NULL AUTO_INCREMENT,
    user_id    BIGINT       DEFAULT NULL,
    action     VARCHAR(100) DEFAULT NULL,
    details    TEXT         DEFAULT NULL,
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_analytics_date   (created_at),
    INDEX idx_analytics_user   (user_id),
    INDEX idx_analytics_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─── SEED DATA ───────────────────────────────────────────────
INSERT INTO categories (name, description) VALUES
    ('Двигатель',       'Запчасти двигателя: фильтры, свечи, прокладки'),
    ('Трансмиссия',     'КПП, сцепление, ШРУС, приводные валы'),
    ('Тормозная система','Колодки, диски, суппорты, шланги'),
    ('Подвеска',        'Амортизаторы, пружины, рычаги, сайлентблоки'),
    ('Кузов',           'Бамперы, фары, капоты, зеркала'),
    ('Электрика',       'Аккумуляторы, генераторы, стартеры, лампы');

INSERT INTO cars (brand, model, year_from, year_to, description) VALUES
    ('Toyota',     'Camry',   2017, NULL,  'Популярный бизнес-седан'),
    ('Lada',       'Vesta',   2015, NULL,  'Российский автомобиль'),
    ('Volkswagen', 'Polo',    2010, 2020,  'Компактный хэтчбек'),
    ('Kia',        'Rio',     2017, NULL,  'Бюджетный седан'),
    ('Hyundai',    'Solaris', 2017, NULL,  'Популярный седан B-класса');

INSERT INTO products (name, description, price, stock, category_id, car_id, article) VALUES
    ('Масляный фильтр Toyota Camry',    'Оригинальный масляный фильтр',         450.00, 50, 1, 1, 'TOY-OIL-001'),
    ('Воздушный фильтр Toyota Camry',   'Фильтр воздушный двигателя',           380.00, 30, 1, 1, 'TOY-AIR-001'),
    ('Тормозные колодки передние Lada', 'Комплект передних тормозных колодок',  890.00, 40, 3, 2, 'LAD-BRK-001'),
    ('Амортизатор задний Kia Rio',      'Масляный амортизатор задний',         2100.00, 20, 4, 4, 'KIA-SHK-001'),
    ('Аккумулятор 60Ah',                'Аккумулятор 60Ah/540A универсальный', 4500.00, 15, 6, NULL, 'BAT-60-001'),
    ('Свечи зажигания NGK (4 шт)',      'Комплект свечей NGK BPR6ES',           680.00, 60, 1, NULL, 'NGK-BPR6-4'),
    ('Тормозной диск передний VW Polo', 'Вентилируемый тормозной диск',        1850.00, 25, 3, 3, 'VW-DSC-001'),
    ('Сайлентблок рычага Hyundai',      'Сайлентблок переднего рычага',         320.00, 35, 4, 5, 'HYN-SLB-001');
