-- Create table for California native plants
CREATE TABLE IF NOT EXISTS native_plants (
    id SERIAL PRIMARY KEY,
    botanical_name VARCHAR(255) UNIQUE NOT NULL,
    common_name VARCHAR(255),
    butterflies_and_moths_supported TEXT,
    attracts_wildlife TEXT,
    plant_type VARCHAR(100),
    form VARCHAR(100),
    height VARCHAR(100),
    width VARCHAR(100),
    growth_rate VARCHAR(50),
    seasonality VARCHAR(100),
    flower_color VARCHAR(100),
    flowering_season VARCHAR(100),
    fragrance VARCHAR(100),
    sun VARCHAR(100),
    soil_drainage VARCHAR(100),
    water_requirement VARCHAR(100),
    summer_irrigation VARCHAR(100),
    ease_of_care VARCHAR(100),
    nursery_availability VARCHAR(100),
    companions TEXT,
    special_uses TEXT,
    communities_simplified TEXT,
    communities TEXT,
    hardiness VARCHAR(100),
    sunset_zones VARCHAR(100),
    soil TEXT,
    soil_texture VARCHAR(100),
    soil_ph VARCHAR(50),
    soil_toxicity VARCHAR(100),
    mulch TEXT,
    site_type VARCHAR(100),
    elevation_min INTEGER,
    elevation_max INTEGER,
    rainfall_min NUMERIC(10, 2),
    rainfall_max NUMERIC(10, 2),
    tips TEXT,
    pests TEXT,
    propagation TEXT,
    height_min NUMERIC(10, 2),
    height_max NUMERIC(10, 2),
    width_min NUMERIC(10, 2),
    width_max NUMERIC(10, 2),
    other_names TEXT,
    alternative_common_names TEXT,
    obsolete_names TEXT,
    rarity VARCHAR(100),
    is_cultivar BOOLEAN DEFAULT FALSE,
    jepson_link VARCHAR(500),
    plant_url VARCHAR(500),
    qr_codes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for commonly queried columns
CREATE INDEX idx_botanical_name ON native_plants(botanical_name);
CREATE INDEX idx_common_name ON native_plants(common_name);
CREATE INDEX idx_plant_type ON native_plants(plant_type);
CREATE INDEX idx_sunset_zones ON native_plants(sunset_zones);

-- Add comment to table
COMMENT ON TABLE native_plants IS 'Storage for information about native California plant species';
