from app import app
from flask import render_template, request
from .preprocessing import process_query, documents_iterator


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Goader')


@app.route('/search', methods=['GET', 'POST'])
def search():
    doc_iter = None
    if request.method == 'POST':
        searched = request.form.get('search-input')
        low_rank = request.form.get('svd')

        doc_iter = documents_iterator(process_query(searched, low_rank=(low_rank is not None)))

    return render_template('query.html', title='Goader - Results', doc_iter=doc_iter)
