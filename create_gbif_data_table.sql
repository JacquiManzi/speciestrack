-- Create table for GBIF observation data
CREATE TABLE IF NOT EXISTS gbif_data (
    id SERIAL PRIMARY KEY,
    scientific_name VARCHAR(500) NOT NULL,
    observation_count INTEGER DEFAULT 1,
    observation_type VARCHAR(100),
    fetch_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for commonly queried columns
CREATE INDEX idx_gbif_scientific_name ON gbif_data(scientific_name);
CREATE INDEX idx_gbif_fetch_date ON gbif_data(fetch_date);

-- Add comment to table
COMMENT ON TABLE gbif_data IS 'Storage for daily GBIF species observation data from Wildcat Canyon Regional Park';
