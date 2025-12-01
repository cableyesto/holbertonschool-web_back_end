-- 3. Old school band 
-- Lists all bands with Glam rock as their main style, ranked by their longevity
SELECT
    band_name,
    split - formed AS lifespan
FROM
    metal_bands
WHERE
    style LIKE 'Glam%'
    AND split IS NOT NULL
    AND formed IS NOT NULL
ORDER BY lifespan DESC;