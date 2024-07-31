import logging
import time

from selenium.common import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.webdriver.web_driver_waiter import WebDriverWaiter


class ClickHelper:
    """Helper class for safely clicking web elements."""

    RETRIES = 3
    DELAY = 2

    @staticmethod
    def safe_click(driver, identifier=None, use_for=False, retries=RETRIES, delay=DELAY):
        """Safely click an element with retries."""
        element = None
        locator = f'label[for="{identifier}"]' if use_for else f'#{identifier}'

        for attempt in range(retries):
            try:
                if identifier:
                    WebDriverWaiter.wait_for_presence(driver, locator, use_css_selector=True)
                    element = driver.find_element(By.CSS_SELECTOR, locator)
                    driver.execute_script("arguments[0].removeAttribute('disabled')", element)

                driver.execute_script("arguments[0].click();", element)
                return

            except (ElementClickInterceptedException, ElementNotInteractableException):
                if element:
                    element.click()
                return

            except (NoSuchElementException, StaleElementReferenceException):
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                logging.error(
                    "Error with element: %s",
                    'for=' +
                    str(identifier) if use_for else 'id=' +
                                                    str(identifier)
                )
                return

            except Exception as e:
                logging.error(
                    "Error clicking on element: %s: %s",
                    'for=' +
                    str(identifier) if use_for else 'id=' +
                                                    str(identifier),
                    e
                )
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    return

    @staticmethod
    def next_click(driver):
        """Safely click NextButton element and wait for .QuestionText's innerHTML to change."""
        while True:
            time.sleep(0.4)
            question_text_element = driver.find_element(By.CSS_SELECTOR, ".QuestionText")
            old_html = question_text_element.get_attribute("innerHTML")

            ClickHelper.safe_click(driver, "NextButton")

            try:
                WebDriverWait(driver, 2).until(
                    lambda d: d.find_element(
                        By.CSS_SELECTOR,
                        ".QuestionText"
                    ).get_attribute(
                        "innerHTML"
                    ) != old_html
                )
                break
            except Exception:
                continue
