import logging
import time
import traceback
from utils.webdriver.web_driver_waiter import WebDriverWaiter
from utils.generator.review_generator import ReviewGen
from utils.click_helper import ClickHelper
from utils import config_manager as cm
from utils import survey_selector as ss
from utils.maintenance import telemetry


class Survey:
    """Main class for running the survey."""

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.selector = ss.SurveySelector(driver)

    def run(self):
        """Run the survey process."""
        try:

            cm.ConfigManager.check_and_create_config()
            [
                store_id,
                order_types,
                order_receptions,
                order_times
            ] = cm.ConfigManager.read_config()
            logging.info("Store Number: %s", store_id)
            logging.info("Order Types: %s", order_types)
            logging.info("Order Receptions: %s", order_receptions)
            logging.info("Order Times: %s", order_times)

            start_message = f"Review started for store number {store_id}"
            telemetry.send(store_id, start_message)

            self.driver.get(f"https://inspirebrands.qualtrics.com/jfe/form/SV_74yz3vwGul2Aqb3?StoreID={store_id}")
            logging.info("Opened survey page")

            WebDriverWaiter.wait_for_invisibility(self.driver, "#pace", use_css_selector=True)
            ClickHelper.next_click(self.driver)
            self.selector.click_elements_with_pattern('label[for$="~5"]')
            ClickHelper.next_click(self.driver)
            ReviewGen.generate(self.driver, store_id)
            ClickHelper.next_click(self.driver)
            self.selector.click_elements_with_pattern('label[for$="~5"]')
            ClickHelper.next_click(self.driver)
            selected_type = self.selector.select_order_types(order_types)
            ClickHelper.next_click(self.driver)
            self.selector.select_order_reception(order_receptions, selected_type)
            ClickHelper.next_click(self.driver)
            self.selector.select_daypart(order_times)
            ClickHelper.next_click(self.driver)
            self.selector.click_elements_with_pattern('label[for$="~5"]')
            ClickHelper.next_click(self.driver)
            self.selector.click_elements_with_pattern('label[for$="~5"]')
            ClickHelper.next_click(self.driver)
            self.selector.click_elements_with_pattern('label[for$="~2"]')
            if ClickHelper.next_click(self.driver):
                self.selector.click_elements_with_pattern('label[for$="~2"]')
                time.sleep(0.4)
                ClickHelper.safe_click(self.driver, "NextButton")
                time.sleep(2)
            logging.info("Review Completed!")

        except Exception as e:
            tb_info = traceback.extract_tb(e.__traceback__)[-1]
            logging.error(
                "Unexpected error occurred in %s at line %d: %s",
                tb_info.filename,
                tb_info.lineno,
                str(e)
            )
            telemetry.send(store_id, tb_info)
            self.driver.quit()
