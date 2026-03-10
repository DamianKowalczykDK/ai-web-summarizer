from src.scrapper.html_text_extractor import fetch_page_text
import httpx
import pytest
import pytest_httpx

def test_fetch_page_text_with_paragraphs(httpx_mock: pytest_httpx.HTTPXMock) -> None:
    html_content = """
    <html>
        <body>
            <article>
            <p>Test Article</p>
            </article>
        </body>
    </html>
    """

    httpx_mock.add_response(url="https://example.com", content=html_content.encode("utf8"))
    result = fetch_page_text(url="https://example.com")

    assert result == "Test Article"

def test_fetch_page_text_no_paragraphs(httpx_mock: pytest_httpx.HTTPXMock) -> None:
    html_content = """
    <html>
        <body>
            <article>
            <div>Text in div</div>
            </article>
        </body>
    </html>
    """

    httpx_mock.add_response(url="https://example.com", content=html_content.encode("utf8"))
    result = fetch_page_text(url="https://example.com")

    assert result is not None
    assert "Text in div" in result

def test_fetch_page_text_error(httpx_mock: pytest_httpx.HTTPXMock) -> None:
    httpx_mock.add_exception(httpx.TimeoutException("Timeout"))
    result = fetch_page_text(url="https://example.com")

    assert result is None

def test_fetch_page_text_removes_tags(httpx_mock: pytest_httpx.HTTPXMock) -> None:
    html_content = """
       <html>
           <head>
               <style>body { color: red; }</style>
               <script>console.log('test');</script>
           </head>
           <body>
               <nav>Navigation</nav>
               <footer>Footer info</footer>
               <article>
                   <p>Main content stays.</p>
                   <img src="image.jpg" />
               </article>
           </body>
       </html>
    """

    httpx_mock.add_response(url="https://example.com", content=html_content.encode('utf8'))
    result = fetch_page_text(url="https://example.com")
    assert result == "Main content stays."
    assert "Navigation" not in result
    assert "Footer info" not in result
    assert "color: red" not in result
