import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class WebDriverFactory:
    """Factory class for creating web driver instances."""

    @staticmethod
    def get_webdriver(browser='chrome'):
        """Get the web driver with the specified browser and extension."""

        proxy_path = os.path.join(os.getcwd(), "proxy")

        if browser == 'chrome':
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument(f"--load-extension={proxy_path}")
            return webdriver.Chrome(options=chrome_options)

        elif browser == 'firefox':
            firefox_options = FirefoxOptions()
            # Add any Firefox-specific options here
            return webdriver.Firefox(options=firefox_options)

        elif browser == 'edge':
            edge_options = EdgeOptions()
            edge_options.add_argument("--log-level=3")
            edge_options.add_argument(f"--load-extension={proxy_path}")
            return webdriver.Edge(options=edge_options)

        else:
            raise ValueError(f"Unsupported browser: {browser}")
