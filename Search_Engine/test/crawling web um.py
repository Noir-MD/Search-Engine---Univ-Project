import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import networkx as nx
from tqdm import tqdm

visited = set()
graph = nx.DiGraph()
base_domain = "um.ac.id"
failed_urls = []
max_depth = 2
total_visited = 0

def crawl(url, depth=0):
    global total_visited

    if depth > max_depth or url in visited:
        return

    print(f"[{len(visited)}] Visiting: {url} (depth {depth})")
    try:
        response = requests.get(url, timeout=15)
        if "text/html" not in response.headers.get("Content-Type", ""):
            return
        visited.add(url)
        total_visited += 1

        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for a_tag in soup.find_all("a", href=True):
            link = urljoin(url, a_tag['href'])
            parsed = urlparse(link)
            if base_domain in parsed.netloc:
                clean_link = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_link not in visited:
                    graph.add_edge(url, clean_link)
                    links.add(clean_link)

        for link in tqdm(list(links), desc=f"Depth {depth+1}"):
            time.sleep(0.5)  # Bisa dikurangi jika tidak diblok
            crawl(link, depth + 1)

    except Exception as e:
        print(f"[!] Error: {url} --> {e}")
        failed_urls.append(url)


if __name__ == "__main__":
    start_url = "https://um.ac.id/"
    print("[*] Starting crawl...")
    crawl(start_url)

    print(f"\n[*] Crawling complete. Visited {total_visited} pages.")
    print(f"[*] Writing output files...")

    with open("failed_urls.txt", "w", encoding="utf-8") as f:
        for url in failed_urls:
            f.write(url + "\n")

    with open("link_graph.txt", "w", encoding="utf-8") as f:
        for edge in graph.edges():
            f.write(f"{edge[0]} --> {edge[1]}\n")

    print("[✓] Done. Output saved.")
