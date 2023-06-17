CREATE TABLE warehouses(
	id SERIAL NOT NULL PRIMARY KEY,
	name varchar(50) NOT NULL,
	location varchar(100) NOT NULL
);

CREATE TABLE goods(
	id SERIAL NOT NULL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
  	quantity INTEGER NOT NULL,
  	warehouse_id INTEGER NOT NULL REFERENCES warehouses(id),
  	updated_at TIMESTAMP NOT NULL
);

INSERT INTO warehouses (name, location) VALUES
  	('North Warehouse', 'North Point Street 11'),
  	('South Warehouse', 'South Point Street 22'),
  	('West Warehouse', 'West Point Street 33');

INSERT INTO goods (name, quantity, warehouse_id, updated_at) VALUES
	('Expensive Product', 50, 3, '2023-06-17 12:30:00'),
	('Amazing Product', 70, 3, '2023-06-16 15:30:00'),
  	('Popular Product', 10, 1, NOW()),
 	('Strange Product', 30, 2, '2023-06-10 10:00:00'),
  	('Some Product', 20, 2, '2023-06-17 13:45:00'),
	('Just Product', 50, 2, '2023-06-16 19:30:00'),
 	('Cool Product', 60, 1, '2023-06-17 11:30:00'),
	('Best Product', 40, 3, current_timestamp),
  	('Real Product', 80, 1, '2023-06-15 15:15:00'),
  	('Rare Product', 5, 3, current_timestamp);

UPDATE goods SET quantity = 1 WHERE name = 'Rare Product';

DELETE FROM goods WHERE warehouse_id = 2;

CREATE INDEX idx_product_name ON goods (name);

