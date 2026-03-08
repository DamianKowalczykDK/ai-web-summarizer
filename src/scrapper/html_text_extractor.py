import httpx
from bs4 import BeautifulSoup, Tag
from typing import cast

def fetch_page_text(url: str) -> str | None:

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        response = httpx.get(url, headers=headers, timeout=10.0)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup(["script", "style", "img", "input", "noscript", "footer", "nav", "aside"]):
            tag.decompose()

        content_root = cast(Tag, soup.find("article") or soup.body or soup)

        paragraphs = content_root.find_all("p")
        if paragraphs:
            text = '\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        else:
            text = content_root.get_text(separator='\n', strip=True)

        return text if text else None
    except Exception as e:
        print(f'Error fetching page: {e}')
        return None