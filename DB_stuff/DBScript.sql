-- MySQL Script generated by MySQL Workbench
-- Mon Jun 14 13:17:42 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema scraperpy
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema scraperpy
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `scraperpy` DEFAULT CHARACTER SET utf8 ;
USE `scraperpy` ;

-- -----------------------------------------------------
-- Table `scraperpy`.`Data`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `scraperpy`.`Data` (
  `gameID` INT NOT NULL,
  `steamUrl` VARCHAR(100) NULL,
  `cardExchange` VARCHAR(100) NULL,
  `cardOutliers` INT NULL,
  `foilOutliers` INT NULL,
  `badData` TINYINT NULL,
  `reason` VARCHAR(200) NULL,
  `avgPriceCard` FLOAT NULL,
  `avgPriceCardF` FLOAT NULL,
  `packBuyPrice` FLOAT NULL,
  `packBuyProfit` FLOAT NULL,
  `packMakePrice` FLOAT NULL,
  `packMakeProfit` FLOAT NULL,
  `badgeBuyPrice` FLOAT NULL,
  `badgeMakePrice` FLOAT NULL,
  `expectEmote` FLOAT NULL,
  `expectBG` FLOAT NULL,
  `expectBuyBadgeProfit` FLOAT NULL,
  `expectMakeBadgeProfit` FLOAT NULL,
  PRIMARY KEY (`gameID`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
