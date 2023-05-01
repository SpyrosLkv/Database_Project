-- MySQL Script generated by MySQL Workbench
-- Mon May  1 21:08:34 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema semester_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema semester_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `semester_project` DEFAULT CHARACTER SET utf8 ;
USE `semester_project` ;

-- -----------------------------------------------------
-- Table `semester_project`.`Authors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Authors` (
  `Author_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Author_id`))
ENGINE = InnoDB
KEY_BLOCK_SIZE = 4;


-- -----------------------------------------------------
-- Table `semester_project`.`Belongs_in`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Belongs_in` (
  `category_id` INT NOT NULL,
  `Book_ISBN` BIGINT(13) NOT NULL,
  PRIMARY KEY (`category_id`, `Book_ISBN`),
  INDEX `fk_Thematic category_has_Book_Book1_idx` (`Book_ISBN` ASC) VISIBLE,
  INDEX `fk_Thematic category_has_Book_Thematic category1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk__Belongs_in_Thematic_Category`
    FOREIGN KEY (`category_id`)
    REFERENCES `semester_project`.`Thematic category` (`category_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Belongs_in_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Book` (
  `ISBN` BIGINT(13) NOT NULL,
  `Title` VARCHAR(45) NOT NULL,
  `Publisher` VARCHAR(45) NOT NULL,
  `No. of Pages` INT NOT NULL,
  `Summary` TEXT NULL,
  `image` BLOB(262144) NULL,
  `Language` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ISBN`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Card`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Card` (
  `User_Id` INT NOT NULL,
  `Card_No` TINYINT NOT NULL,
  `Status` ENUM("Pending", "Active", "Inactive", "Missing") NOT NULL,
  PRIMARY KEY (`User_Id`, `Card_No`),
  INDEX `fk_Card_Users1_idx` (`User_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Card_Users_Id`
    FOREIGN KEY (`User_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Keywords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Keywords` (
  `Keyword_id` INT NOT NULL AUTO_INCREMENT,
  `Keyword` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Keyword_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Keywords_in_book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Keywords_in_book` (
  `Keyword_id` INT NOT NULL,
  `Book_ISBN` BIGINT(13) NOT NULL,
  PRIMARY KEY (`Keyword_id`, `Book_ISBN`),
  INDEX `fk_Keywords_has_Book_Book1_idx` (`Book_ISBN` ASC) VISIBLE,
  INDEX `fk_Keywords_has_Book_Keywords1_idx` (`Keyword_id` ASC) VISIBLE,
  CONSTRAINT `fk_Keywords_Keyword_id`
    FOREIGN KEY (`Keyword_id`)
    REFERENCES `semester_project`.`Keywords` (`Keyword_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk__Keywords_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Lib_Owns_Book`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Lib_Owns_Book` (
  `Book_ISBN` BIGINT(13) NOT NULL,
  `Library_id` INT NOT NULL,
  `Total_copies` SMALLINT NOT NULL,
  `available_copies` SMALLINT NOT NULL,
  PRIMARY KEY (`Book_ISBN`, `Library_id`),
  INDEX `fk_Book_has_School - Library_School - Library1_idx` (`Library_id` ASC) VISIBLE,
  INDEX `fk_Book_has_School - Library_Book1_idx` (`Book_ISBN` ASC) VISIBLE,
  CONSTRAINT `fk_Owns_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Owns_Library_id`
    FOREIGN KEY (`Library_id`)
    REFERENCES `semester_project`.`School - Library` (`Library_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Loan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Loan` (
  `Book_ISBN` BIGINT(13) NOT NULL,
  `User_Id` INT NOT NULL,
  `Loan_date` DATETIME NOT NULL,
  `Return_date` DATETIME NULL,
  `status` ENUM("Active", "Late Active", "Returned", "Late Returned") NOT NULL,
  PRIMARY KEY (`Book_ISBN`, `User_Id`),
  INDEX `fk_Book_has_Users_Users3_idx` (`User_Id` ASC) VISIBLE,
  INDEX `fk_Book_has_Users_Book2_idx` (`Book_ISBN` ASC) VISIBLE,
  CONSTRAINT `fk_Loan_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Loan_User_Id`
    FOREIGN KEY (`User_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Operator Appointment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Operator Appointment` (
  `Operator_Id` INT NOT NULL,
  `Library_Appointment` INT NOT NULL,
  `Administrator_Id` INT NOT NULL,
  `Appointment_No` VARCHAR(45) NOT NULL,
  `Date_of_appointment` DATETIME NULL,
  PRIMARY KEY (`Operator_Id`, `Library_Appointment`, `Administrator_Id`, `Appointment_No`),
  INDEX `fk_Operator Appointment_School - Library1_idx` (`Library_Appointment` ASC) VISIBLE,
  INDEX `fk_Operator Appointment_Users2_idx` (`Administrator_Id` ASC) VISIBLE,
  CONSTRAINT `fk_OA_Operator`
    FOREIGN KEY (`Operator_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_OA_Library`
    FOREIGN KEY (`Library_Appointment`)
    REFERENCES `semester_project`.`School - Library` (`Library_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_OA_Admin`
    FOREIGN KEY (`Administrator_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Pending Registrations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Pending Registrations` (
  `Username` VARCHAR(45) NOT NULL,
  `Password_Hashed` TEXT NOT NULL,
  `First_Name` VARCHAR(45) NOT NULL,
  `Last_Name` VARCHAR(45) NOT NULL,
  `Birth_Date` DATETIME NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Role` ENUM("Admin", "Operator", "Teacher", "Student") NOT NULL,
  `Library_id` INT NOT NULL,
  PRIMARY KEY (`Username`, `Library_id`),
  INDEX `fk_Pending Registrations_School - Library1_idx` (`Library_id` ASC) VISIBLE,
  CONSTRAINT `fk_Registration_Library_id`
    FOREIGN KEY (`Library_id`)
    REFERENCES `semester_project`.`School - Library` (`Library_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Reg_ phone No`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Reg_ phone No` (
  `number` BIGINT(20) NOT NULL,
  `Registration_Username` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`number`, `Registration_Username`),
  INDEX `fk_Reg_ phone No_Registration1_idx` (`Registration_Username` ASC) VISIBLE,
  CONSTRAINT `fk_Reg_ phone No_Registration1`
    FOREIGN KEY (`Registration_Username`)
    REFERENCES `semester_project`.`Pending Registrations` (`Username`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Reservation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Reservation` (
  `Book_ISBN` BIGINT(13) NOT NULL,
  `User_Id` INT NOT NULL,
  `Reservation_Date` DATETIME NOT NULL,
  `Expiration_Date` DATETIME NOT NULL,
  `Status` ENUM("Active", "Honoured", "Expired") NULL,
  PRIMARY KEY (`Book_ISBN`, `User_Id`),
  INDEX `fk_Book_has_Users_Users2_idx` (`User_Id` ASC) VISIBLE,
  INDEX `fk_Book_has_Users_Book1_idx` (`Book_ISBN` ASC) VISIBLE,
  CONSTRAINT `fk_Res_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Res_User_Id`
    FOREIGN KEY (`User_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Reviews` (
  `Book_ISBN` BIGINT(13) NOT NULL,
  `User_Id` INT NOT NULL,
  `Likert Rating` TINYINT NOT NULL,
  `Review` TEXT NULL,
  PRIMARY KEY (`Book_ISBN`, `User_Id`),
  INDEX `fk_Book_has_Users_Users1_idx` (`User_Id` ASC) VISIBLE,
  INDEX `fk_Book_has_Users_Book_idx` (`Book_ISBN` ASC) VISIBLE,
  CONSTRAINT `fk_Rev_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Rev_User_Id`
    FOREIGN KEY (`User_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`School - Library`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`School - Library` (
  `Library_id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NOT NULL,
  `Address` VARCHAR(45) NOT NULL,
  `Town` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NOT NULL,
  `Principals_id` INT NOT NULL,
  PRIMARY KEY (`Library_id`),
  INDEX `fk_School - Library_Users1_idx` (`Principals_id` ASC) VISIBLE,
  CONSTRAINT `fk_Principal_id`
    FOREIGN KEY (`Principals_id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`School_Phone_No`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`School_Phone_No` (
  `Phone_No` BIGINT(20) NOT NULL,
  `School - Library_Library_id` INT NOT NULL,
  PRIMARY KEY (`Phone_No`, `School - Library_Library_id`),
  INDEX `fk_School_Phone_No_School - Library1_idx` (`School - Library_Library_id` ASC) VISIBLE,
  CONSTRAINT `fk_Phone_Library_id`
    FOREIGN KEY (`School - Library_Library_id`)
    REFERENCES `semester_project`.`School - Library` (`Library_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Thematic category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Thematic category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`User_Phone_No`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`User_Phone_No` (
  `number` BIGINT(20) NOT NULL,
  `User_Id` INT NOT NULL,
  PRIMARY KEY (`number`, `User_Id`),
  INDEX `fk_User_Phone_No_Users1_idx` (`User_Id` ASC) VISIBLE,
  CONSTRAINT `fk_Phone_User_Id`
    FOREIGN KEY (`User_Id`)
    REFERENCES `semester_project`.`Users` (`User_Id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Users` (
  `User_Id` INT NOT NULL AUTO_INCREMENT,
  `Username` VARCHAR(45) NOT NULL,
  `Password_Hashed` TEXT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `Birth_Date` DATETIME NOT NULL,
  `email` VARCHAR(45) NULL,
  `Role` ENUM("Admin", "Operator", "Teacher", "Student") NOT NULL,
  `last_update` TIMESTAMP NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  `users_library_id` INT NOT NULL,
  PRIMARY KEY (`User_Id`),
  UNIQUE INDEX `Username_UNIQUE` (`Username` ASC) VISIBLE,
  INDEX `fk_Users_School - Library1_idx` (`users_library_id` ASC) VISIBLE,
  UNIQUE INDEX `User_Id_UNIQUE` (`User_Id` ASC) VISIBLE,
  CONSTRAINT `fk_User_Library_id`
    FOREIGN KEY (`users_library_id`)
    REFERENCES `semester_project`.`School - Library` (`Library_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `semester_project`.`Wrote`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `semester_project`.`Wrote` (
  `Author_id` INT NOT NULL,
  `Book_ISBN` BIGINT(13) NOT NULL,
  PRIMARY KEY (`Author_id`, `Book_ISBN`),
  INDEX `fk_Authors_has_Book_Book1_idx` (`Book_ISBN` ASC) VISIBLE,
  INDEX `fk_Authors_has_Book_Authors1_idx` (`Author_id` ASC) VISIBLE,
  CONSTRAINT `fk_Wrote_Author_id`
    FOREIGN KEY (`Author_id`)
    REFERENCES `semester_project`.`Authors` (`Author_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Wrote_Book_ISBN`
    FOREIGN KEY (`Book_ISBN`)
    REFERENCES `semester_project`.`Book` (`ISBN`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
