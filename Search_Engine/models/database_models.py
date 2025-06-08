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
    sql = """
        SELECT p.url, pr.rank
        FROM pages p
        LEFT JOIN pagerank pr ON p.id = pr.page_id
        WHERE p.url LIKE %s
        ORDER BY pr.rank DESC
    """
    wildcard_query = f"%{query}%"
    cursor.execute(sql, (wildcard_query,))
    results = cursor.fetchall()
    conn.close()
    return results
