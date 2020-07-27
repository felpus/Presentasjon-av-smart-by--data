#drop schema apidb;

Create schema if not exists apidb;
USE apidb;

CREATE TABLE if not exists thingType (
  thingTypeId varchar(100) NOT NULL,
  thingTypeLabel varchar(1000) NOT NULL,
  thingTypeDescription varchar(1000),
  primary key(thingTypeId)
);	

CREATE TABLE if not exists sensors (
  id varchar(100) NOT null,
  label varchar(1000) NOT NULL,
  description varchar(1000),
  coordinates varchar(1000),
  typeId varchar(100) NOT NULL,
  primary key(id),
  Constraint FK_sensors_thingType Foreign Key (typeId) references thingType (thingTypeId)
);
