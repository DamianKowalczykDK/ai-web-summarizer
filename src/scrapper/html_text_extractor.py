import httpx
from bs4 import BeautifulSoup, Tag
from typing import cast

def fetch_page_text(url: str) -> str | None:
    """
    Fetch and extract readable text content from a web page.

    The function sends an HTTP GET request to the provided URL, parses
    the HTML using BeautifulSoup, removes non-content elements
    (such as scripts, styles, navigation, and images), and extracts
    textual content from paragraph tags. If no paragraphs are found,
    it falls back to extracting text from the main content container.

    Parameters
    ----------
    url : str
        The URL of the web page to fetch.

    Returns
    -------
    str | None
        Extracted text content from the page, or None if no text
        could be retrieved or an error occurred.
    """

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