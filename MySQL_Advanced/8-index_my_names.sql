-- 8. Optimize simple search
-- Creates an index for the names table.
CREATE INDEX idx_name_first ON names (name(1));