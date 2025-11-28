-- Fix NULL awarded_at values in existing records
-- Run this script to update existing stipends and scholarships with NULL awarded_at

USE ssmp;

-- Update stipends with NULL awarded_at to current timestamp
UPDATE stipends 
SET awarded_at = CURRENT_TIMESTAMP 
WHERE awarded_at IS NULL;

-- Update scholarships with NULL awarded_at to current timestamp
UPDATE scholarships 
SET awarded_at = CURRENT_TIMESTAMP 
WHERE awarded_at IS NULL;

-- Verify the changes
SELECT 'Stipends' as table_name, COUNT(*) as total, 
       SUM(CASE WHEN awarded_at IS NULL THEN 1 ELSE 0 END) as null_count 
FROM stipends
UNION ALL
SELECT 'Scholarships' as table_name, COUNT(*) as total, 
       SUM(CASE WHEN awarded_at IS NULL THEN 1 ELSE 0 END) as null_count 
FROM scholarships;
