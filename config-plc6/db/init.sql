-- Create the database
CREATE DATABASE IF NOT EXISTS banking;
USE banking;

-- Create customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    customer_id BIGINT NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'transfer') NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_date DATETIME NOT NULL,
    status ENUM('pending', 'completed', 'failed') NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Insert sample customers
INSERT INTO customers (name, email) VALUES
('Alice Sharma', 'alice@example.com'),
('Bob Verma', 'bob@example.com'),
('Charlie Dey', 'charlie@example.com');

-- Insert sample transactions
INSERT INTO transactions (customer_id, transaction_type, amount, transaction_date, status) VALUES
(1, 'deposit', 5000.00, '2025-01-01 10:00:00', 'completed'),
(1, 'withdrawal', 1500.00, '2025-01-02 11:00:00', 'completed'),
(2, 'deposit', 7000.00, '2025-02-01 14:30:00', 'completed'),
(2, 'transfer', 2000.00, '2025-02-03 09:15:00', 'pending'),
(3, 'withdrawal', 1000.00, '2025-03-10 16:00:00', 'completed');


