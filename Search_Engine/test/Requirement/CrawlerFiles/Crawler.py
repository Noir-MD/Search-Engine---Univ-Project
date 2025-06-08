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

# Store crawled data to avoid duplicate URLs in pages_data.txt
crawled_data = {}

crawl_start_time = None
crawl_time_limit = 999999 # seconds


def crawl(url, depth=0):
    global total_visited, crawl_start_time

    # Stop if time limit exceeded
    if crawl_start_time and (time.time() - crawl_start_time > crawl_time_limit):
        print(f"[!] Time limit of {crawl_time_limit} seconds reached. Stopping crawl.")
        return

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
        # Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        # Extract main content (simple approach: all text)
        content = soup.get_text(separator=" ", strip=True)
        # Save to crawled_data dict to avoid duplicates
        if url not in crawled_data:
            crawled_data[url] = (title, content)

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
    crawl_start_time = time.time()
    crawl(start_url)

    print(f"\n[*] Crawling complete. Visited {total_visited} pages.")
    print(f"[*] Writing output files...")

    with open("failed_urls.txt", "w", encoding="utf-8") as f:
        for url in failed_urls:
            f.write(url + "\n")

    # Write header and all unique crawled data to pages_data.txt
    with open("pages_data.txt", "w", encoding="utf-8") as pf:
        pf.write("url\ttitle\tcontent\n")
        for url, (title, content) in crawled_data.items():
            # Replace tabs/newlines in title/content to avoid breaking the format
            safe_title = title.replace('\t', ' ').replace('\n', ' ')
            safe_content = content.replace('\t', ' ').replace('\n', ' ')
            pf.write(f"{url}\t{safe_title}\t{safe_content}\n")

    # Write separate files for url, title, and content
    with open("urls.txt", "w", encoding="utf-8") as uf, \
         open("titles.txt", "w", encoding="utf-8") as tf, \
         open("contents.txt", "w", encoding="utf-8") as cf:
        for url, (title, content) in crawled_data.items():
            uf.write(url + "\n")
            tf.write(title.replace('\n', ' ').replace('\t', ' ') + "\n")
            cf.write(content.replace('\n', ' ').replace('\t', ' ') + "\n")

    print("[✓] Done. Output saved.")
