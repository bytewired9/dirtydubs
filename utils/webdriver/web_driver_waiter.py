from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WebDriverWaiter:
    """Helper class for waiting for web driver conditions."""

    WAIT_TIMEOUT = 20

    @staticmethod
    def wait_for_invisibility(driver, identifier, use_css_selector=False):
        """Wait for an element to become invisible."""
        locator = (By.CSS_SELECTOR, identifier) if use_css_selector else (By.ID, identifier)
        WebDriverWait(driver, WebDriverWaiter.WAIT_TIMEOUT).until(
            EC.invisibility_of_element_located(locator)
        )

    @staticmethod
    def wait_for_presence(driver, identifier, use_css_selector=False):
        """Wait for an element to become present."""
        locator = (By.CSS_SELECTOR, identifier) if use_css_selector else (By.ID, identifier)
        WebDriverWait(driver, WebDriverWaiter.WAIT_TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )
