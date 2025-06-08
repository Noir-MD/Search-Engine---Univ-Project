# models/database_models.py (Alternative Method)

import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'search'
}

def search_database(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Split the user's query into individual words
    search_words = query.split()

    # Base of the SQL query
    sql = """
        SELECT p.url, pr.rank
        FROM pages p
        LEFT JOIN pagerank pr ON p.id = pr.page_id
    """

    # Dynamically add a 'WHERE ... LIKE' clause for each word
    if search_words:
        # Creates a list of "p.url LIKE %s" conditions
        where_clauses = ["p.url LIKE %s"] * len(search_words)
        # Joins them with " AND "
        sql += " WHERE " + " AND ".join(where_clauses)

    # Add the final ordering
    sql += " ORDER BY pr.rank DESC"

    # Create the parameters, adding wildcards to each word
    # e.g., ['seleksi', 'mandiri'] becomes ['%seleksi%', '%mandiri%']
    params = [f"%{word}%" for word in search_words]

    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return results