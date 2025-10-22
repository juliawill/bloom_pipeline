-- 040_roi.sql
-- Creates table for ROI simulations linking to recommended actions
CREATE TABLE IF NOT EXISTS bloom_analytics.roi (
    id SERIAL PRIMARY KEY,  -- Unique ID for each ROI simulation
    action_id INT NOT NULL REFERENCES bloom_analytics.actions(id),  -- Link back to the differentiator/action being tested
    scenario_name TEXT NOT NULL,  -- e.g., 'DTC $35', 'Retail $40', etc.
    channel TEXT CHECK (channel IN ('DTC', 'Retail')),  -- Sales channel type
    unit_price FLOAT NOT NULL,  -- Selling price per unit in USD
    unit_cost FLOAT NOT NULL,  -- Estimated production + fulfillment cost per unit
    units_sold INT,  -- Estimated number of units sold under this scenario
    gross_profit FLOAT,  -- (unit_price - unit_cost) * units_sold
    roi_percent FLOAT,  -- (gross_profit / (unit_cost * units_sold)) * 100
    breakeven_units INT,  -- Number of units needed to break even
    assumptions TEXT,  -- Notes on scenario inputs (e.g., marketing spend, conversion rates)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
