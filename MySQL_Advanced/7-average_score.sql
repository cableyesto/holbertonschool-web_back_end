-- 7. Average score
-- Creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(C.score)
        FROM corrections AS C
        WHERE C.user_id = users.id
    )
    WHERE id = user_id;
END;
//

DELIMITER ;