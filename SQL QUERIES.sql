USE expenses_db;
#1. Total Amount Spent in Each Category
SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category;

#2. Total Amount Spent Using Each Payment Mode
SELECT payment_mode, SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_mode;

# 3. Total Cashback Received Across All Transactions
SELECT SUM(cashback) AS total_cashback
FROM expenses;

# 4. Top 5 Most Expensive Categories
SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;

# 5. Spending on Transportation by Payment Mode
SELECT payment_mode, SUM(amount) AS total_spent
FROM expenses
WHERE category = 'Transportation'
GROUP BY payment_mode;

# 6. Transactions with Cashback
SELECT *
FROM expenses
WHERE cashback > 0;

# 7. Total Spending Per Month
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
FROM expenses
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;

#8. Months with Highest Spending in Travel, Entertainment, or Gifts
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
FROM expenses
WHERE category IN ('Travel', 'Entertainment', 'Gifts')
GROUP BY YEAR(date), MONTH(date)
ORDER BY total_spent DESC;

# 9. Recurring Expenses in Specific Months
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_subscription_spent
FROM expenses
WHERE category = 'Subscription'
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;

# 10. Cashback Earned Per Month
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(cashback) AS total_cashback
FROM expenses
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;

# 11. Overall Spending Trend Over Time
SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
FROM expenses
GROUP BY YEAR(date), MONTH(date)
ORDER BY year, month;

# 12. Typical Costs for Travel
SELECT AVG(amount) AS average_travel_cost
FROM expenses
WHERE category = 'Travel';

# 13. Patterns in Grocery Spending (e.g., Weekends)
SELECT 
    CASE 
        WHEN DAYOFWEEK(date) = 1 OR DAYOFWEEK(date) = 7 THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    SUM(amount) AS total_spent
FROM expenses
WHERE category = 'Groceries'
GROUP BY day_type;

# 14. High and Low Priority Categories
SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC
LIMIT 1;

SELECT category, SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent ASC
LIMIT 1;

# 15. Category with Highest Percentage of Total Spending
SELECT category, (SUM(amount) / (SELECT SUM(amount) FROM expenses)) * 100 AS percentage
FROM expenses
GROUP BY category
ORDER BY percentage DESC
LIMIT 1;