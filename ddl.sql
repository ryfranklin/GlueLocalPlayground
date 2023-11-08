DROP DATABASE IF EXISTS TestDB;

CREATE DATABASE TestDB;


CREATE TABLE ORDERS (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    ItemCode INT,
    OrderDate DATETIME
);