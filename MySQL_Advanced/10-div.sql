-- 10. Safe divide
-- Creates a function SafeDiv that divides (and returns) the first by the second number
-- or returns 0 if the second number is equal to 0.
DELIMITER //

CREATE FUNCTION SafeDiv(
    a INT,
    b INT
)
RETURNS DOUBLE
DETERMINISTIC
BEGIN
    DECLARE result FLOAT;
    IF b = 0 THEN
        SET result = 0;
    ELSE
        SET result = CAST(a / b AS DOUBLE);
    END IF;
    RETURN (result);
END;
//

DELIMITER ;