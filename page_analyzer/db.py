import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# conn = psycopg2.connect(DATABASE_URL)
#
#
# sql_file_path = os.path.join('..', 'database.sql')
#
# with conn.cursor() as cur, open(sql_file_path, 'r') as data_base:
#     cur.execute(data_base.read())
#
#     conn.commit()
#     conn.close()


def add_url_to_db(url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
        conn.commit()
        conn.close()


def trans_urls(urls):
    result = []
    if not isinstance(urls, list):
        return {
            'id': urls.id,
            'name': urls.name,
            'created_at': str(urls.created_at)
        }

    for url in urls:
        url_data = {
            'id': url.id,
            'name': url.name,
            'created_at': str(url.created_at)
        }

        result.append(url_data)

    return result


def get_url_by_name(url):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s", (url,))

        url = cur.fetchone()

        if url:
            url_data = trans_urls(url)
        else:
            url_data = None

        conn.commit()
        conn.close()

    return url_data


def get_url_by_id(url_id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))

        url = cur.fetchone()

        url_data = trans_urls(url)

        conn.commit()
        conn.close()

    return url_data


def get_all_urls_desc():
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls ORDER BY id DESC")

        all_urls = cur.fetchall()
        all_urls_data = trans_urls(all_urls)

        conn.commit()
        conn.close()

    return all_urls_data
