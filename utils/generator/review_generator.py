import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# import reviewgen as rg
from utils.maintenance import telemetry


class ReviewGen:
    """Class for generating and inputting reviews."""

    @staticmethod
    def generate(driver, storeid, review):
        """Generate and input a review."""
        textbox_id = "QR~QID43"
        time.sleep(0.4)

        try:
            textbox = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.ID, textbox_id))
            )
            driver.execute_script("arguments[0].scrollIntoView();", textbox)
            driver.execute_script("arguments[0].click();", textbox)
        except Exception as e:
            logging.error("Failed to click the text box: %s", e)
            return
        if not review:
            logging.info("No review generated")
        else:
            if review:
                logging.info("Review generated: %s", review)
            else:
                logging.info("No Review Generated.")

        try:
            textbox.clear()
            textbox.send_keys(review)
            entered_text = textbox.get_attribute('value')
            if entered_text == review:
                logging.info("Review text successfully entered.")
            else:
                logging.error("Text entry failed. Entered: %s", entered_text)
                telemetry.send(storeid, "Text entry failed. Entered: {entered_text}")

            logging.info("Review chosen: %s", review)
        except Exception as e:
            logging.error("Failed to enter text: %s", e)
            telemetry.send(storeid, "Failed to enter text: {e}")
