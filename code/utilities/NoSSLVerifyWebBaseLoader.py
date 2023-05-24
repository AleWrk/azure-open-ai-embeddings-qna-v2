from langchain.document_loaders import WebBaseLoader

from typing import Any, List, Optional, Union

class NoSSLVerifyWebBaseLoader(WebBaseLoader):
    """Custom Loader with NoSSL verify that uses urllib and beautiful soup to load webpages."""
    web_paths: List[str]

    requests_per_second: int = 2
    """Max number of concurrent requests to make."""

    default_parser: str = "html.parser"
    """Default parser to use for BeautifulSoup."""

    def __init__(self, web_path: Union[str, List[str]], header_template: Optional[dict] = None):
        WebBaseLoader.__init__(self, web_path, header_template)
        self.session.verify = False