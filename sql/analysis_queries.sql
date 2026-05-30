-- Total Customers

SELECT COUNT(*) AS total_customers
FROM customers;


-- Total Churn Customers

SELECT COUNT(*) AS churn_customers
FROM customers
WHERE Churn = 1;


-- Churn By Contract

SELECT Contract,
       COUNT(*) AS total_customers
FROM customers
GROUP BY Contract;