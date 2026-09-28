-- NEXUS Database Schema

CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(20),
    date_of_birth DATE,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    signup_date DATE,
    customer_segment VARCHAR(50)
);


CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    supplier_id BIGINT,
    unit_cost DECIMAL(12,2),
    selling_price DECIMAL(12,2)
);


CREATE TABLE warehouses (
    warehouse_id BIGINT PRIMARY KEY,
    warehouse_name VARCHAR(150),
    city VARCHAR(100),
    state VARCHAR(100),
    capacity INT,
    operating_cost DECIMAL(12,2)
);


CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    warehouse_id BIGINT,
    order_date TIMESTAMP,
    order_status VARCHAR(50),
    total_amount DECIMAL(12,2),
    discount_amount DECIMAL(12,2),
    shipping_cost DECIMAL(12,2),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id)
);


CREATE TABLE order_items (
    order_item_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    unit_price DECIMAL(12,2),
    discount DECIMAL(12,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


CREATE TABLE payments (
    payment_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    payment_date TIMESTAMP,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    amount DECIMAL(12,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


CREATE TABLE inventory (
    inventory_id BIGINT PRIMARY KEY,
    product_id BIGINT,
    warehouse_id BIGINT,
    stock_quantity INT,
    reorder_level INT,
    last_updated TIMESTAMP,

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES warehouses(warehouse_id)
);


CREATE TABLE deliveries (
    delivery_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    carrier VARCHAR(100),
    shipped_date TIMESTAMP,
    expected_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    delivery_status VARCHAR(50),
    delivery_delay_days INT,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


CREATE TABLE returns (
    return_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    product_id BIGINT,
    return_date DATE,
    return_reason VARCHAR(200),
    return_quantity INT,
    refund_amount DECIMAL(12,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);