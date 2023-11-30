SELECT 
    F.*
FROM
    Faculty AS F
WHERE
    EXISTS( SELECT 
            1
        FROM
            Team AS T
        WHERE
            T.F_SRN = F.F_SRN)
        AND NOT EXISTS( SELECT 
            1
        FROM
            Panel AS P
        WHERE
            P.Panel_ID = F.Panel_ID);


DELIMITER //
CREATE PROCEDURE AssignStudentToTeam(IN studentSRN VARCHAR(10), IN teamID INT, IN projectID INT)
BEGIN
    UPDATE Student
    SET TeamID = teamID, ProjectID = projectID
    WHERE SRN = studentSRN;
END //
DELIMITER ;



DELIMITER $$

CREATE TRIGGER CheckPanelMembersBeforeInsert
BEFORE INSERT ON Faculty
FOR EACH ROW
BEGIN
  DECLARE max_members INT;
  
  -- Get the maximum number of members allowed in the Panel
  SELECT No_of_Members INTO max_members FROM Panel WHERE Panel_ID = NEW.Panel_ID;
  
  -- Get the current number of members in the Panel
  SELECT COUNT(*) INTO @current_members FROM Faculty WHERE Panel_ID = NEW.Panel_ID;
  
  -- If the number of current members is equal to or greater than the maximum, do not insert the new faculty
  IF @current_members >= max_members THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Panel already has the maximum number of members.';
  END IF;
END$$

DELIMITER ;
