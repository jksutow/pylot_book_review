-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema book_reviews
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema book_reviews
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `book_reviews` DEFAULT CHARACTER SET utf8 ;
USE `book_reviews` ;

-- -----------------------------------------------------
-- Table `book_reviews`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_reviews`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `alias` VARCHAR(45) NULL,
  `email` VARCHAR(65) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `book_reviews`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `book_reviews`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `book_title` VARCHAR(100) NULL,
  `author` VARCHAR(65) NULL,
  `review` TEXT NULL,
  `rating` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reviews_users_idx` (`users_id` ASC),
  CONSTRAINT `fk_reviews_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `book_reviews`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
