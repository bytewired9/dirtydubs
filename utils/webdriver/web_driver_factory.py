import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriverFactory:
    """Factory class for creating web driver instances."""

    @staticmethod
    def get_webdriver():
        """Get the web driver with the extension."""
        chrome_options = Options()
        proxy_path = os.path.join(os.getcwd(), "proxy")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument(f"--load-extension={proxy_path}")
        return webdriver.Chrome(options=chrome_options)
