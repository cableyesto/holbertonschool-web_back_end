-- 6. Add bonus
-- Creates a stored procedure AddBonus that adds a new correction for a student
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN corrections_score FLOAT
)
BEGIN
    DECLARE is_old_project BOOLEAN;
    DECLARE project_id_match INT;

    SELECT EXISTS(SELECT 1 FROM projects WHERE name = project_name) INTO is_old_project;
    
    IF is_old_project THEN
        SELECT id INTO project_id_match FROM projects WHERE name = project_name;
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id_match, corrections_score);
    ELSE
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id_match = LAST_INSERT_ID();
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id_match, corrections_score);
    END IF;
END;
//

DELIMITER ;