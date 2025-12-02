-- 9. Optimize search and score
-- Creates an index for the names table.
CREATE INDEX idx_name_first_score ON names (name(1), score);