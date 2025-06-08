import mysql.connector
from itertools import zip_longest

# Koneksi ke database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # ganti kalau pakai password
    database='search_engine'
)
cursor = conn.cursor()

# Baca file
with open('urls.txt', 'r', encoding='utf-8') as uf, \
     open('titles.txt', 'r', encoding='utf-8') as tf, \
     open('contents.txt', 'r', encoding='utf-8') as cf:
    urls = [line.strip() for line in uf]
    titles = [line.strip() for line in tf]
    contents = [line.strip() for line in cf]

for url, title, content in zip_longest(urls, titles, contents, fillvalue=''):
    cursor.execute("SELECT id FROM pages WHERE url = %s", (url,))
    row = cursor.fetchone()
    if not row:
        cursor.execute(
            "INSERT INTO pages (url, title, content) VALUES (%s, %s, %s)",
            (url, title, content)
        )
        conn.commit()

print('✅ Import selesai dari urls.txt, titles.txt, contents.txt.')
cursor.close()
conn.close()