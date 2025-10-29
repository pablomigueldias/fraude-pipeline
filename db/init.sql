CREATE TABLE IF NOT EXISTS raw_transactions(
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50),
    customer_id VARCHAR(50),
    amount NUMERIC(12,2)
    country VARCHAR(2),
    channel VARCHAR(20),
    timestamp TIMESTAMP,
    is_fraud INT
);
CREATE TABLE IF NOT EXISTS features_transactions(
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE,
    customer_id VARCHAR(50),
    amount NUMERIC(12,2)
    hour INT,
    is_high_amount INT,
    country_risk FLOAT,
    rolling_1h_tx INT,
    amount_zscore FLOAT,
    is_fraud INT
    )