import mysql.connector
import networkx as nx

# Konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'search_engine'
}

# Step 1: Ambil data link dari database (pastikan tabel links ada kolom from_page dan to_page yang mengacu ke pages.id)
def get_links():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT from_page, to_page FROM links")
    edges = cursor.fetchall()
    conn.close()
    return edges

# Step 2: Hitung PageRank
def compute_pagerank(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)
    pr = nx.pagerank(G, alpha=0.85)
    return pr

# Step 3: Simpan hasil ke tabel pages (kolom: id, title, url, content, pagerank)
def save_pagerank(pagerank_scores):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Tambahkan kolom pagerank jika belum ada
    cursor.execute("""
        ALTER TABLE pages
        ADD COLUMN IF NOT EXISTS pagerank FLOAT
    """)

    # Update nilai pagerank untuk setiap halaman
    for page_id, score in pagerank_scores.items():
        cursor.execute("UPDATE pages SET pagerank = %s WHERE id = %s", (score, page_id))

    conn.commit()
    conn.close()

# Main execution
if __name__ == '__main__':
    edges = get_links()
    if not edges:
        print("Tidak ada data link ditemukan.")
    else:
        pagerank_scores = compute_pagerank(edges)
        save_pagerank(pagerank_scores)
        print("PageRank berhasil dihitung dan disimpan.")