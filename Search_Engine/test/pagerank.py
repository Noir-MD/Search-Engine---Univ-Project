import mysql.connector
import networkx as nx

# Konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'search'
}

# Step 1: Ambil data link dari database
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

# Step 3: Simpan hasil ke database
def save_pagerank(pagerank_scores):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Buat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagerank (
            page_id INT PRIMARY KEY,
            rank FLOAT
        )
    """)

    # Hapus data lama
    cursor.execute("DELETE FROM pagerank")

    # Masukkan data baru
    for page_id, score in pagerank_scores.items():
        cursor.execute("INSERT INTO pagerank (page_id, rank) VALUES (%s, %s)", (page_id, score))

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
