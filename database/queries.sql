CREATE TABLE IF NOT EXISTS assets (
    id VARCHAR(50) PRIMARY KEY,
    rank INTEGER,
    symbol VARCHAR(10),
    name VARCHAR(100),
    supply NUMERIC,
    max_supply NUMERIC,
    market_cap_usd NUMERIC,
    volume_usd_24hr NUMERIC,
    price_usd NUMERIC,
    change_percent_24hr NUMERIC,
    vwap_24hr NUMERIC
);

CREATE TABLE IF NOT EXISTS asset_history (
    id SERIAL PRIMARY KEY,
    asset_id VARCHAR(50) REFERENCES assets(id),
    date TIMESTAMP,
    price_usd NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_asset_history_asset_id ON asset_history(asset_id);
CREATE INDEX IF NOT EXISTS idx_asset_history_date ON asset_history(date);