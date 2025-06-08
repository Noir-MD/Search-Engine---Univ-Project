import mysql.connector

# Koneksi ke database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # ganti kalau pakai password
    database='search'
)
cursor = db.cursor()

# STEP 1: Baca URL gagal
with open('failed_urls.txt', 'r') as f:
    failed_urls = set(url.strip() for url in f if url.strip())

# STEP 2: Simpan URL ke dalam set untuk menghindari duplikat
url_to_id = {}

def get_or_create_page(url):
    url = url.strip()
    if url in failed_urls:
        return None
    if url in url_to_id:
        return url_to_id[url]

    # Cek apakah sudah ada di DB
    cursor.execute("SELECT id FROM pages WHERE url = %s", (url,))
    row = cursor.fetchone()
    if row:
        url_to_id[url] = row[0]
        return row[0]
    
    # Kalau belum ada → insert
    cursor.execute("INSERT INTO pages (url) VALUES (%s)", (url,))
    db.commit()
    page_id = cursor.lastrowid
    url_to_id[url] = page_id
    return page_id

# STEP 3: Parse file link_graph.txt
with open('link_graph.txt', 'r') as f:
    for line in f:
        if '-->' not in line:
            continue
        src, dst = line.strip().split('-->')
        src = src.strip()
        dst = dst.strip()

        src_id = get_or_create_page(src)
        dst_id = get_or_create_page(dst)

        if src_id and dst_id:
            cursor.execute(
                "INSERT INTO links (from_page, to_page) VALUES (%s, %s)",
                (src_id, dst_id)
            )

db.commit()
print("✅ Import selesai.")
