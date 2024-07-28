"""
Survey automation script using Selenium WebDriver.
This script reads configuration settings, navigates through a survey, and generates reviews.
"""

import sys
import logging
import argparse
from colorama import Fore, Back, init
from survey import Survey
from web_driver_factory import WebDriverFactory

init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=
    Fore.YELLOW + '%(asctime)s - %(levelname)s' +
    Fore.GREEN + ' - %(message)s'
)


LOGO = """\
                  -=## #  # ##::
               ## #            # ##
        ##    #                    #    ##
       # #   *                      +   # #
       # #  ##                      ##  # *
       # ##*### #                # ###*#+ #
         ##  # +              -   # #  ##
          #### #  # #  #  #  # *  # ####
        #.# ### ###-         ==### ### # #
      #########   .#-        *#   +#########
           ######  #          -  ######
            ##### # ##      ## # #####
             ###  ## ##    ## ##  ###
            ####   # ###  ### #   ####
            *###   ##        ##   ###.
             ###*#  ###    ###  #####
                ##*#=        =#*##
                ##################
                # ###  *  *  ### *
                   *#        #=
                    #=#    ###
                     ##    ##
                      ## -##
                       ####"""


def main(repeat_count):
    """Main function to run the survey specified times."""
    for _ in range(repeat_count):
        driver = WebDriverFactory.get_webdriver()
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        survey = Survey(driver)
        survey.run()
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the survey script multiple times.")
    parser.add_argument(
        "repeat",
        type=int,
        nargs='?',
        default=1,
        help="Number of times to repeat the survey"
    )
    args = parser.parse_args()

    try:
        print(LOGO)
        main(args.repeat)
    except KeyboardInterrupt:
        logging.info("\nKeyboardInterrupt caught. Cleaning up...")
    finally:
        sys.exit()
