import logging
import random

from selenium.webdriver.common.by import By

from web_driver_waiter import WebDriverWaiter
from click_helper import ClickHelper


class SurveySelector:
    """Selector class for survey operations."""

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def click_elements_with_pattern(self, pattern):
        """Click elements matching a pattern."""
        WebDriverWaiter.wait_for_presence(self.driver, pattern, use_css_selector=True)
        elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
        for elem in elements:
            ClickHelper.safe_click(self.driver, identifier=elem.get_attribute("for"), use_for=True)

    def select_random_option(self, options, ids, label):
        """Select a random option from the provided options and click the corresponding input."""
        selected_option = random.choice(options)
        suffix = ids[selected_option]
        WebDriverWaiter.wait_for_presence(
            self.driver,
            f'label[for$="{suffix}"]',
            use_css_selector=True
        )
        element = self.driver.find_element(By.CSS_SELECTOR, f'[for$="{suffix}"]')
        ClickHelper.safe_click(self.driver, identifier=element.get_attribute("for"), use_for=True)
        logging.info("Selected %s: %s", label, selected_option)
        return selected_option

    def select_order_types(self, types):
        """Select order types randomly from the provided types
        and click the corresponding inputs."""
        type_ids = {
            'call': '~1',
            'web': '~2',
            'app': '~3',
            'walkin': '~4'
        }
        return self.select_random_option(types, type_ids, "order type")

    def select_order_reception(self, receptions, selected_type):
        """Select order reception randomly from the provided types
        and click the corresponding inputs."""
        reception_ids = {
            'delivery': '~1',
            'carryout': '~3',
            'dinein': '~2'
        }

        possible_receptions = {
            "walkin": ['carryout', 'dinein'],
            "web": ['carryout', 'delivery'],
            "app": ['carryout', 'delivery'],
            "call": ['carryout']
        }.get(selected_type, receptions)

        valid_receptions = [r for r in possible_receptions if r in receptions]

        if not valid_receptions:
            valid_receptions = [r for r in receptions if r in reception_ids]

        return self.select_random_option(valid_receptions, reception_ids, "order reception")

    def select_daypart(self, order_times):
        """Select a daypart randomly from the provided order times
        and click the corresponding input."""
        daypart_ids = {
            "breakfast": "~1",
            "lunch": "~2",
            "midday": "~3",
            "dinner": "~4",
            "latenight": "~5",
            "overnight": "~6",
        }
        self.select_random_option(order_times, daypart_ids, "daypart")

    def select_highest_suffix(self, pattern):
        """Select the label with the highest for$=~# suffix."""
        WebDriverWaiter.wait_for_presence(self.driver, pattern, use_css_selector=True)
        elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
        highest_suffix_elem = max(
            elements,
            key=lambda e: int(e.get_attribute("for").split("~")[-1])
        )
        ClickHelper.safe_click(
            self.driver,
            identifier=highest_suffix_elem.get_attribute("for"),
            use_for=True
        )
