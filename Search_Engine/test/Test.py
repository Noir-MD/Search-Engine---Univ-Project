from flask import Flask, render_template, request
import mysql.connector
from example import SearchEngine

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
    # Fetch all documents for ranking
    cursor.execute("SELECT title, content FROM documents")
    all_docs = cursor.fetchall()
    conn.close()
    # Index documents using SearchEngine
    se = SearchEngine()
    doc_tuples = [(title, content) for title, content in all_docs]
    se.bulk_index(doc_tuples)
    # Rank documents using BM25
    ranked_scores = se.search(query)
    # Sort by score descending
    ranked_titles = sorted(ranked_scores.items(), key=lambda x: x[1], reverse=True)
    # Prepare results as (title, content, score)
    title_to_content = {title: content for title, content in all_docs}
    results = [(title, title_to_content[title], score) for title, score in ranked_titles if title in title_to_content]
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