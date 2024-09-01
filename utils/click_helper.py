import logging
import time

from selenium.common import ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.webdriver import web_driver_waiter as wdw


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
                    wdw.WebDriverWaiter.wait_for_presence(driver, locator, use_css_selector=True)
                    element = driver.find_element(By.CSS_SELECTOR, locator)
                    driver.execute_script("arguments[0].removeAttribute('disabled')", element)

                driver.execute_script("arguments[0].click();", element)
                return True

            except (ElementClickInterceptedException, ElementNotInteractableException):
                if element:
                    element.click()
                return True

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
                return False

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
                    return False

    @staticmethod
    def next_click(driver):
        """Safely click NextButton element and wait for .QuestionText's innerHTML to change.

        Returns "retry" if the NextButton fails 3 times, otherwise returns True or False.
        """
        retries = 3
        for attempt in range(retries):
            time.sleep(0.4)
            try:
                question_text_element = driver.find_element(By.CSS_SELECTOR, ".QuestionText")
                old_html = question_text_element.get_attribute("innerHTML")
            except NoSuchElementException:
                logging.info("Survey has ended, no more questions found.")
                return False

            if not ClickHelper.safe_click(driver, "NextButton"):
                if attempt < retries - 1:
                    logging.warning(f"NextButton click failed. Retry {attempt + 1}/{retries}")
                    continue
                else:
                    logging.error("NextButton click failed 3 times.")
                    return "retry"
            else:
                try:
                    WebDriverWait(driver, 2).until(
                        lambda d: d.find_element(
                            By.CSS_SELECTOR,
                            ".QuestionText"
                        ).get_attribute(
                            "innerHTML"
                        ) != old_html
                    )
                    return True
                except Exception:
                    continue
        return False
