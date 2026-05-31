-- ════════════════════════════════════════════════════
-- setup_db.sql — MySQL Setup for Soil Crop Prediction System
-- Run this in MySQL Workbench or mysql CLI:
--   mysql -u root -p < setup_db.sql
-- ════════════════════════════════════════════════════

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS soil_crop_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE soil_crop_db;

-- 2. Prediction History table
CREATE TABLE IF NOT EXISTS prediction_history (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nitrogen       FLOAT NOT NULL,
    phosphorus     FLOAT NOT NULL,
    potassium      FLOAT NOT NULL,
    ph             FLOAT NOT NULL,
    temperature    FLOAT NOT NULL,
    humidity       FLOAT NOT NULL,
    rainfall       FLOAT NOT NULL,
    predicted_crop VARCHAR(100) NOT NULL,
    confidence     FLOAT NOT NULL,
    timestamp      DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Crop Dataset table (for Admin management)
CREATE TABLE IF NOT EXISTS crop_dataset (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    crop_name    VARCHAR(100) NOT NULL,
    nitrogen     FLOAT NOT NULL,
    phosphorus   FLOAT NOT NULL,
    potassium    FLOAT NOT NULL,
    ph           FLOAT NOT NULL,
    temperature  FLOAT NOT NULL,
    humidity     FLOAT NOT NULL,
    rainfall     FLOAT NOT NULL,
    season       VARCHAR(50),
    description  TEXT,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Seed the crop_dataset with sample data
INSERT INTO crop_dataset (crop_name, nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall, season, description) VALUES
('Rice',         90,  42,  43,  6.0, 23, 82, 200, 'Kharif',     'Staple grain crop requiring high water and humid conditions.'),
('Maize',        78,  48,  20,  6.5, 22, 65, 85,  'Kharif',     'Versatile cereal crop grown in warm, moderate-rainfall regions.'),
('Chickpea',     40,  68,  79,  7.2, 18, 16, 70,  'Rabi',       'Legume crop that thrives in cool, dry winter conditions.'),
('Kidney Beans', 20,  67,  20,  5.7, 19, 21, 105, 'Kharif',     'High-protein legume suited to moderate rainfall areas.'),
('Banana',       100, 82,  50,  6.0, 27, 80, 105, 'Year-round', 'Tropical fruit crop requiring warm temperatures and humidity.'),
('Mango',        20,  27,  30,  5.8, 31, 50, 95,  'Zaid',       'Popular tropical fruit preferring hot and dry summers.'),
('Grapes',       23,  132, 200, 6.0, 24, 82, 70,  'Rabi',       'Vine crop thriving on high potassium and low rainfall.'),
('Watermelon',   99,  17,  50,  6.5, 25, 85, 50,  'Zaid',       'Summer fruit needing high nitrogen and warm weather.'),
('Coffee',       101, 28,  29,  6.8, 25, 58, 158, 'Year-round', 'Cash crop grown in cool, shaded, highland regions.'),
('Coconut',      22,  16,  28,  6.0, 26, 94, 175, 'Year-round', 'Tropical palm producing versatile fruits and oil.');

SELECT 'Database setup complete!' AS status;
