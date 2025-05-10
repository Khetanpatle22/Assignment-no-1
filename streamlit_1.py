import streamlit as st
import pandas as pd
import mysql.connector

# Function to execute SQL queries and return a DataFrame
def run_query(query):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Khetan2@2",  
        database="expenses_db"     
    )
    cursor = cnx.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return pd.DataFrame(result, columns=columns)

# Predefined queries for the dropdown menu
queries = {
    "1. Total amount spent in each category": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC;
    """,
    "2. Total amount spent using each payment mode": """
        SELECT payment_mode, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY payment_mode
        ORDER BY total_spent DESC;
    """,
    "3. Total cashback received across all transactions": """
        SELECT SUM(cashback) AS total_cashback
        FROM expenses;
    """,
    "4. Top 5 most expensive categories": """
        SELECT category, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY category
        ORDER BY total_spent DESC
        LIMIT 5;
    """,
    "5. Spending trend by month": """
        SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY DATE_FORMAT(date, '%Y-%m')
        ORDER BY month;
    """,
    "6. Transactions with Cashback":"""
        SELECT *
        FROM expenses 
        WHERE cashback > 0;
    """,
    "7. Total Spending Per Month":"""
        SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
        FROM expenses
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY year, month;
    """,
    "8. Months with Highest Spending in Travel, Entertainment, or Gifts":"""
        SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
        FROM expenses
        WHERE category IN ('Travel', 'Entertainment', 'Gifts')
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY total_spent DESC;
    """,
   "9. Recurring Expenses in Specific Months":"""
        SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_subscription_spent
        FROM expenses
        WHERE category = 'Subscription'
        GROUP BY YEAR(date), MONTH(date)
        ORDER BY year, month;
    """,
    "10. Cashback Earned Per Month":"""
       SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(cashback) AS total_cashback
       FROM expenses
       GROUP BY YEAR(date), MONTH(date)
       ORDER BY year, month;
   """,
  "11. Overall Spending Trend Over Time":"""
       SELECT YEAR(date) AS year, MONTH(date) AS month, SUM(amount) AS total_spent
       FROM expenses
       GROUP BY YEAR(date), MONTH(date)
       ORDER BY year, month;
    """,
   "12. Typical Costs for Travel":"""
       SELECT AVG(amount) AS average_travel_cost
       FROM expenses
       WHERE category = 'Travel';
    """,
    "13. Patterns in Grocery Spending (e.g., Weekends)":"""
       SELECT 
       CASE 
        WHEN DAYOFWEEK(date) = 1 OR DAYOFWEEK(date) = 7 THEN 'Weekend'
        ELSE 'Weekday'
        END AS day_type,
        SUM(amount) AS total_spent
        FROM expenses
        WHERE category = 'Groceries'
        GROUP BY day_type;
    """,
    "14. High and Low Priority Categories":"""
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
   """,
    "15. Category with Highest Percentage of Total Spending":"""
      SELECT category, (SUM(amount) / (SELECT SUM(amount) FROM expenses)) * 100 AS percentage
      FROM expenses
      GROUP BY category
      ORDER BY percentage DESC
      LIMIT 1;
    """  
      }

# Streamlit app layout
st.title("Personal Expense Tracker")
st.write("Explore your spending habits by selecting a question below or running a custom query.")

# Dropdown for predefined questions
question = st.selectbox("Select a question to answer:", list(queries.keys()))

if question:
    query = queries[question]
    try:
        df = run_query(query)
        st.subheader(question)

        # Visualization logic based on DataFrame structure
        if len(df) == 1 and len(df.columns) == 1:
            st.metric(label="Result", value=f"{df.iloc[0, 0]:.2f}")
        elif len(df.columns) == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
            if df.iloc[:, 0].dtype == 'object' and df.iloc[:, 0].str.match(r'\d{4}-\d{2}').all():
                df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
                st.line_chart(df.set_index(df.columns[0])[df.columns[1]])
            else:
                st.bar_chart(df.set_index(df.columns[0])[df.columns[1]])
        else:
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error executing query: {e}")

# Sidebar for custom queries
st.sidebar.header("Custom Query")
custom_query = st.sidebar.text_area("Enter your SQL query:", height=150, value="SELECT * FROM expenses LIMIT 5;")
if st.sidebar.button("Run Custom Query"):
    try:
        df_custom = run_query(custom_query)
        st.sidebar.write("Custom Query Result:")
        st.dataframe(df_custom)
    except Exception as e:
        st.sidebar.error(f"Error executing query: {e}")

# Instructions for next steps
st.write("""
### Next Steps
- Formulate your own 10-15 insightful queries using the custom query section.
- Take screenshots of key visualizations for your project submission.
- Run the app locally with `streamlit run expense_tracker_app.py`.
""")