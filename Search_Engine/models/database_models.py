import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'search_engine'
}

def search_database(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Split the user's query into individual words
    search_words = query.split()

    # Base SQL: ambil url, title, content, rank
    sql = """
        SELECT p.url, p.title, p.content, IFNULL(pr.rank, 0)
        FROM pages p
        LEFT JOIN pagerank pr ON p.id = pr.page_id
    """

    # WHERE: cari di title atau content
    if search_words:
        where_clauses = ["(p.title LIKE %s OR p.content LIKE %s)"] * len(search_words)
        sql += " WHERE " + " AND ".join(where_clauses)

    sql += " ORDER BY pr.rank DESC"

    # Parameter: setiap kata untuk title dan content
    params = []
    for word in search_words:
        like = f"%{word}%"
        params.extend([like, like])

    cursor.execute(sql, params)
    results = cursor.fetchall()
    conn.close()
    return results