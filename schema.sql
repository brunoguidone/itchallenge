--DROP DATABASE IF EXISTS challenge;--
--CREATE DATABASE challenge;--

CREATE TABLE cats(
	id 				VARCHAR(50) PRIMARY KEY,
	name 			VARCHAR (50) UNIQUE NOT NULL,
	origin 			VARCHAR (50) NULL,
	temperament 	VARCHAR (355) NULL,
	description 	VARCHAR (500) NULL
);

CREATE TABLE img(
	breed_id    	varchar(50) NULL,
	imgurl			varchar(500),
	hashat			boolean,
	hassunglass		boolean
);