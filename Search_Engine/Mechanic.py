from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, template_folder='public')

# Connect To Database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',         
    'database': 'search'
}

def search_database(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "SELECT title, content FROM documents WHERE title LIKE %s OR content LIKE %s"
    wildcard_query = f"%{query}%"
    cursor.execute(sql, (wildcard_query, wildcard_query))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_database(query)
    return render_template('results.html', query=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
