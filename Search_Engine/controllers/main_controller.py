from flask import Flask, render_template, request
from models.database_models import search_database
import os
from math import ceil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'views', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'views', 'static')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
    # Use request.args.get() to handle queries from the form and pagination links
    query = request.args.get('query')
    if not query:
        # If the query is submitted via POST from the main page
        query = request.form.get('query')
        if not query:
            return render_template('index.html')

    page = request.args.get('page', 1, type=int)
    PER_PAGE = 10

    all_results = search_database(query)
    
    # Pagination logic
    total_results = len(all_results)
    total_pages = ceil(total_results / PER_PAGE)
    start_index = (page - 1) * PER_PAGE
    end_index = start_index + PER_PAGE
    
    paginated_results = all_results[start_index:end_index]

    return render_template(
        'results.html', 
        query=query, 
        results=paginated_results,
        page=page,
        total_pages=total_pages,
        total_results=total_results
    )

if __name__ == '__main__':
    app.run(debug=True)