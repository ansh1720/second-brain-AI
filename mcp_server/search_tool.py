import urllib.parse
import requests
from bs4 import BeautifulSoup

def search_web(query: str) -> str:
    """Searches the web for the given query and returns a summary of the top results.

    Args:
        query: The search query string.

    Returns:
        A markdown string summarizing search results.
    """
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise Exception(f"HTTP error {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for elem in soup.find_all("div", class_="result__body")[:5]:
            title_elem = elem.find("a", class_="result__url")
            snippet_elem = elem.find("a", class_="result__snippet")
            if title_elem and snippet_elem:
                title = title_elem.text.strip()
                link = title_elem.get("href", "")
                snippet = snippet_elem.text.strip()
                results.append(f"### {title}\nLink: {link}\n\n{snippet}\n")

        if not results:
            for i, l in enumerate(soup.find_all("a", class_="result__snippet")[:5]):
                results.append(f"Result {i+1}:\n{l.text.strip()}\n")

        if results:
            return "\n".join(results)

        return f"No results found for: {query}"

    except Exception as e:
        return f"Web search unavailable: {str(e)}. Please check your internet connection."
