import logging
import time
import traceback
from utils.webdriver.web_driver_waiter import WebDriverWaiter
from utils.webdriver.web_driver_factory import WebDriverFactory
from utils.generator.review_generator import ReviewGen
import utils.generator.reviewgen as rg
from utils.click_helper import ClickHelper
from utils import config_manager as cm
from utils import survey_selector as ss
from utils.maintenance import telemetry

class Survey:
    """Main class for running the survey."""

    def __init__(self, browser):
        super().__init__()
        cm.ConfigManager.check_and_create_config()
        [
            self.store_id,
            self.order_types,
            self.order_type_weights,
            self.order_receptions,
            self.order_reception_weights,
            self.order_times,
            self.order_time_weights,
            self.survey_chance

        ] = cm.ConfigManager.read_config()
        self.driver = WebDriverFactory.get_webdriver(browser.lower())
        self.selector = ss.SurveySelector(self.driver)


    @staticmethod
    def execute(action, driver):
        """executes the given action and attempts to click NextButton, retrying if necessary."""
        while True:
            action()  # Perform the action (e.g., selecting an option)
            result = ClickHelper.next_click(driver)
            if result != "retry":
                break  # Exit the loop if the click was successful or failed without needing a retry

    def run(self):
        """Run the survey process."""
        try:
            logging.info("Store Number: %s", self.store_id)
            logging.info("Order Types: %s", self.order_types)
            logging.info("Order Receptions: %s", self.order_receptions)
            logging.info("Order Times: %s", self.order_times)
            logging.info("Chance of Survey: %s", self.survey_chance)

            selected_type, type_suffix = self.selector.select_order_type(self.order_types, self.order_type_weights)
            reception, reception_suffix = self.selector.select_order_reception(self.order_receptions, selected_type, self.order_reception_weights)
            order_time, time_suffix = self.selector.select_daypart(self.order_times, self.order_time_weights)
            review = rg.generate_review(self.survey_chance)
            if review == "":
                review_message = "None"
            else:
                review_message = review
            start_message = (
                f"Review started: \n" +
                f"Order Type: `{selected_type}` \n" +
                f"Order Reception: `{reception}` \n" +
                f"Order Time: `{order_time}` \n" +
                f"Review Chosen: `{review_message}`"
            )
            telemetry.send(self.store_id, start_message)

            self.driver.get(f"https://inspirebrands.qualtrics.com/jfe/form/SV_74yz3vwGul2Aqb3?StoreID={self.store_id}")
            logging.info("Opened survey page")

            WebDriverWaiter.wait_for_invisibility(self.driver, "#pace", use_css_selector=True)
            ClickHelper.next_click(self.driver)
            self.execute(lambda: self.selector.click_elements_with_pattern('label[for$="~5"]'), self.driver)
            self.execute(lambda: ReviewGen.generate(self.driver, self.store_id, review), self.driver)
            self.execute(lambda: self.selector.click_elements_with_pattern('label[for$="~5"]'), self.driver)
            self.execute(lambda: self.selector.click_element_by_suffix(type_suffix), self.driver)
            self.execute(lambda: self.selector.click_element_by_suffix(reception_suffix), self.driver)
            self.execute(lambda: self.selector.click_element_by_suffix(time_suffix), self.driver)
            self.execute(lambda: self.selector.click_elements_with_pattern('label[for$="~5"]'), self.driver)
            self.execute(lambda: self.selector.click_elements_with_pattern('label[for$="~5"]'), self.driver)
            self.execute(lambda: self.selector.click_elements_with_pattern('label[for$="~2"]'), self.driver)

            # Additional logic for conditional retries
            if ClickHelper.next_click(self.driver):
                self.selector.click_elements_with_pattern('label[for$="~2"]')
                if ClickHelper.next_click(self.driver):
                    self.selector.click_elements_with_pattern('label[for$="~5"]')
                    ClickHelper.next_click(self.driver)
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
