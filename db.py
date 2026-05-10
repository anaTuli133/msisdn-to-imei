import oracledb
import pandas as pd

# Oracle Connection — Business Intelligence Table View
def table_connection():
    """
    Establish a connection to the BI Data Server.
    Used specifically for the IMEI_TRIPLET and Materialized View operations.
    """
    return oracledb.connect(
        user="dwh_user",
        password="dwh_user_123",
        dsn="192.168.61.16:1521/datadb01"
    )

# Fetches distinct IMEI lists based on MSISDN inputs
def fetch_msisdn_to_imei(msisdns: list) -> pd.DataFrame:
    """
    Fetch distinct IMEI data for a list of given MSISDNs.
    Filters by the current month for performance optimization.
    """
    if not msisdns:
        return pd.DataFrame()

    # Create named placeholders for bind variables (:m0, :m1, etc.)
    placeholders = ", ".join([f":m{i}" for i in range(len(msisdns))])
    bind_vals = {f"m{i}": m for i, m in enumerate(msisdns)}
    
    SQL_TEMPLATE = f"""
    SELECT IMEI
    FROM (
        SELECT
            T.IMEI,
            ROW_NUMBER() OVER (
                PARTITION BY T.MSISDN
                ORDER BY T.DATE_KEY DESC
            ) AS RN
        FROM IMEI_TRIPLET T
        WHERE T.IMEI IS NOT NULL
        AND T.MSISDN IN ({placeholders})
    )
    WHERE RN = 1
    """

    conn = table_connection()
    try:
        cur = conn.cursor()
        cur.arraysize = 500  # Network optimization
        cur.execute(SQL_TEMPLATE, bind_vals)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        return pd.DataFrame(rows, columns=cols)
    finally:
        cur.close()
        conn.close()

# Uses MSISDN_IMEI_VIEW for high-speed searches on 7M+ records
def fetch_table(search_query=None):
    """
    Fetches data from MSISDN_IMEI_VIEW. 
    If search_query is provided, it searches all 7.2M records.
    Otherwise, it returns the first 500 records.
    """
    if search_query:
        # Step 1: Search the entire 7.2M database using the materialized view
        table_query = "SELECT * FROM MSISDN_IMEI_VIEW WHERE MSISDN = :s OR IMEI = :s"
        binds = {"s": search_query.strip()}
    else:
        # Step 2: Default view for the landing page to keep it fast
        table_query = "SELECT * FROM MSISDN_IMEI_VIEW WHERE ROWNUM <= 500"
        binds = {}

    conn = table_connection() 
    try:
        cursor = conn.cursor()
        # Fetching 500 rows at a time for efficiency
        cursor.arraysize = 500 
        cursor.execute(table_query, binds)
        # Get column names from the cursor description
        columns = [col[0] for col in cursor.description]
        # Fetch all matched rows
        rows = cursor.fetchall()
        return columns, rows
    
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        return [], []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

#to get the latest date on the IMEI as per date_key, output shows date_value
def get_latest_date():
    conn = table_connection()
    try:
        cur = conn.cursor()
        cur.execute("""SELECT TO_CHAR(MAX(D.DATE_VALUE), 'YYYY-MM-DD')
                       FROM IMEI_TRIPLET T
                       JOIN DATE_DIM D ON T.DATE_KEY = D.DATE_KEY""")
        row = cur.fetchone()
        if row and row[0]:
            return row[0]
        return None
    finally:
        cur.close()
        conn.close()