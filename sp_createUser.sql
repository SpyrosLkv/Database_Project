DELIMITER $$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_first_name VARCHAR(45),
    IN p_last_name VARCHAR(45),
    IN p_username VARCHAR(45),
    IN p_email VARCHAR(45),
    IN p_password TEXT
)

BEGIN
    if ( select exists (select 1 from Users where user_username = p_username) ) THEN
        select 'Username Exists !!';
    ELSE
        insert into semester_project.Users
        (
            user_first_name,
            user_last_name,
            user_username,
            user_email,
            user_password
        )
        values
        (
            p_first_name,
            p_last_name,
            p_username,
            p_email,
            p_password
        );

    END IF;
END$$

DELIMITER ;
