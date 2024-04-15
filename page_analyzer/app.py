import os
from dotenv import load_dotenv
from page_analyzer.url_validator import validate
from urllib.parse import urlparse
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    get_flashed_messages,
)
from page_analyzer.db import (
    add_url_to_db,
    get_url_by_id,
    get_url_by_name,
    get_all_urls_desc
)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def page_analyzer():
    message = get_flashed_messages(with_categories=True)

    return render_template('index.html', message=message)


@app.post('/urls')
def add_url():
    new_url = request.form.get('url')

    error = validate(new_url)

    if error:
        flash(f'{error}', 'danger')
        return redirect(url_for('page_analyzer'))

    parsed_url = urlparse(new_url)
    normal_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if get_url_by_name(normal_url):
        old_url_data = get_url_by_name(normal_url)

        flash('Страница уже существует', 'primary')

        return redirect(url_for('show_url', id=old_url_data['id']))

    add_url_to_db(normal_url)

    new_url_data = get_url_by_name(normal_url)

    flash('Страница успешно добавлена', 'success')

    return redirect(url_for('show_url', id=new_url_data['id']))


@app.get('/urls')
def show_all_urls():
    all_urls = get_all_urls_desc()

    return render_template('urls.html', all_urls=all_urls)


@app.get('/urls/<id>')
def show_url(id):
    url_data = get_url_by_id(id)
    message = get_flashed_messages(with_categories=True)

    return render_template('url.html', url_data=url_data, message=message)
