CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(50) NOT NULL,  -- References user_id of customer
    restaurant_id VARCHAR(50) NOT NULL,  -- References user_id of restaurant
    delivery_personnel_id VARCHAR(50),  -- References user_id of delivery personnel
    order_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending'  -- Status can be 'Pending', 'Confirmed', 'Delivered', etc.
);

-- Table to store ordered items
CREATE TABLE ordered_items (
    id SERIAL PRIMARY KEY,
    order_item_id VARCHAR(50) UNIQUE NOT NULL,
    restaurant_item_id VARCHAR(50) NOT NULL,  -- References restaurant_menu_items
    order_id VARCHAR(50) REFERENCES orders(order_id),
    quantity INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL
);
