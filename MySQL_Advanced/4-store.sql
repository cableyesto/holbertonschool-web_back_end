-- 4. Buy buy buy 
-- Create a trigger to reduce quantity of item after an order
DELIMITER //

CREATE TRIGGER decrease_items_trigger
AFTER INSERT
ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET
        items.quantity = items.quantity - NEW.number
    WHERE
        items.name = NEW.item_name;
END;
//

DELIMITER ;