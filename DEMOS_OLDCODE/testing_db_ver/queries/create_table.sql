CREATE TABLE IF NOT EXISTS sleep_table (
    id INTEGER auto_increment PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    pulse_sensor INT
);