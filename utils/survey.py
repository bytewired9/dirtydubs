import logging
import traceback
from pprint import pprint
from typing import Callable
from selenium import webdriver
from .maintenance import telemetry
from utils import config_manager
from utils.click_helper import ClickHelper as click_helper
from utils.survey_selector import SurveySelector as survey_selector
from utils.generator.reviewgen import generate_review
from utils.generator.review_generator import ReviewGen
from utils.webdriver.web_driver_factory import WebDriverFactory
from utils.webdriver.web_driver_waiter import WebDriverWaiter

type WebDriverType = webdriver.chrome.webdriver.WebDriver | webdriver.firefox.webdriver.WebDriver | webdriver.edge.webdriver.WebDriver


class Survey:
    """Main class for running the survey."""

    def __init__(self, browser: str):
        super().__init__()
        self.browser = browser
        self.driver: WebDriverType = WebDriverFactory.get_webdriver(self.browser.lower())
        self.selector = survey_selector(self.driver)
        self._setup_config()

    def _setup_config(self):
        print("Browser: ", self.browser)
        print("Config File: ", config_manager.ConfigManager.CONFIG_FILE)
        print("Checking and creating config...")
        config_manager.ConfigManager.check_and_create_config()
        print("Reading config...")
        (
            self.store_id, self.order_types, self.order_type_weights,
            self.order_receptions, self.order_reception_weights,
            self.order_times, self.order_time_weights, self.survey_chance,
            self.auto, self.run_in_background, self.surveys_per_hour
        ) = config_manager.ConfigManager.read_config()
        print("Config read successfully!")
        print("Configurations:", self.store_id, self.order_types, self.order_type_weights, self.order_receptions,
              self.order_reception_weights, self.order_times, self.order_time_weights, self.survey_chance, self.auto,
              self.run_in_background, self.surveys_per_hour)
        pprint(self.__dict__)

    def click_elements_with_high_rating(self):
        """Clicks elements with a high rating pattern."""
        self.selector.click_elements_with_pattern('label[for$="~5"]')

    def click_elements_with_low_rating(self):
        """Clicks elements with a low rating pattern."""
        self.selector.click_elements_with_pattern('label[for$="~2"]')

    def generate_review_action(self, review: str):
        """Generates a review using ReviewGen."""
        ReviewGen.generate(self.driver, self.store_id, review)

    def click_element_with_suffix_action(self, suffix: str):
        """Clicks elements matching a suffix."""
        self.selector.click_element_by_suffix(suffix)

    def execute(self, action: Callable, *args, **kwargs):
        """
        Executes the given action with provided arguments and attempts to click NextButton,
        retrying if necessary.
        """
        while True:
            action(*args, **kwargs)  # Perform the action with arguments
            result = click_helper.next_click(self.driver)
            if result != "retry":
                break  # Exit the loop if the click was successful or failed without needing a retry

    def perform_survey_steps(self, type_suffix: str, reception_suffix: str, time_suffix: str, review: str):
        """Performs the steps of the survey."""
        self.execute(self.click_elements_with_high_rating)
        self.execute(self.generate_review_action, review)
        self.execute(self.click_elements_with_high_rating)
        self.execute(self.click_element_with_suffix_action, type_suffix)
        self.execute(self.click_element_with_suffix_action, reception_suffix)
        self.execute(self.click_element_with_suffix_action, time_suffix)
        self.execute(self.click_elements_with_high_rating)
        self.execute(self.click_elements_with_high_rating)
        self.execute(self.click_elements_with_low_rating)

        # Additional logic for conditional retries
        if click_helper.next_click(self.driver):
            self.execute(self.click_elements_with_low_rating)
            if click_helper.next_click(self.driver):
                self.execute(self.click_elements_with_high_rating)
                click_helper.next_click(self.driver)

    def run(self):
        """Run the survey process."""
        try:
            logging.info("Store Number: %s", self.store_id)
            logging.info("Order Types: %s", self.order_types)
            logging.info("Order Receptions: %s", self.order_receptions)
            logging.info("Order Times: %s", self.order_times)
            logging.info("Chance of Survey: %s", self.survey_chance)

            selected_type, type_suffix = self.selector.select_order_type(self.order_types, self.order_type_weights)
            reception, reception_suffix = self.selector.select_order_reception(
                self.order_receptions, selected_type=selected_type, weights=self.order_reception_weights
            )
            order_time, time_suffix = self.selector.select_daypart(self.order_times, self.order_time_weights)
            review = generate_review(self.survey_chance)
            review_message = review if review else "None"
            start_message = (
                f"Review started: \n"
                f"Order Type: `{selected_type}` \n"
                f"Order Reception: `{reception}` \n"
                f"Order Time: `{order_time}` \n"
                f"Review Chosen: `{review_message}`"
            )
            telemetry.send(self.store_id, start_message)

            self.driver.get(f"https://inspirebrands.qualtrics.com/jfe/form/SV_74yz3vwGul2Aqb3?StoreID={self.store_id}")
            logging.info("Opened survey page")

            WebDriverWaiter.wait_for_invisibility(self.driver, "#pace", use_css_selector=True)
            click_helper.next_click(self.driver)

            self.perform_survey_steps(type_suffix, reception_suffix, time_suffix, review)

            logging.info("Review Completed!")
            self.driver.quit()
        except Exception as e:
            tb_info = traceback.extract_tb(e.__traceback__)[-1]
            logging.error(
                "Unexpected error occurred in %s at line %d: %s",
                tb_info.filename,
                tb_info.lineno,
                str(e)
            )
            telemetry.send(self.store_id, tb_info)
            self.driver.quit()

