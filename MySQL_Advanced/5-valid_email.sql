-- 5. Email validation to sent
-- Create a trigger to reset boolean when email was updated
DELIMITER //

CREATE TRIGGER reset_valid_email_trigger
BEFORE UPDATE
ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//

DELIMITER ;