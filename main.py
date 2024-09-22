"""
Survey automation script using Selenium WebDriver.
This script reads configuration settings, navigates through a survey, and generates reviews.
"""

import sys
import logging
import argparse
from colorama import Fore, init
from utils.survey import Survey
from utils.maintenance import updater
import  traceback

BROWSER = "edge"
VERSION = "1.1.0"
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=
    Fore.YELLOW + '%(asctime)s - %(levelname)s' +
    Fore.GREEN + ' - %(message)s'
)

LOGO = r"""
     ____  _      __        ____        __        
    / __ \(_)____/ /___  __/ __ \__  __/ /_  _____
   / / / / / ___/ __/ / / / / / / / / / __ \/ ___/
  / /_/ / / /  / /_/ /_/ / /_/ / /_/ / /_/ (__  ) 
 /_____/_/_/   \__/\__, /_____/\__,_/_.___/____/  
                  /____/           
                 
                     ▄▄&ΓⁿB4▄
             ¢   ▄█▀▀        ╙▀█▄   t
           ,¬▌  ▐                ▌   U,
           ▓▐▄ ▄█▄              ╒██ ,▌▓
           ▓▄▀▀████            ████▀▀▄▌
            `███▌▀▄▌█▄▀█▄,█Æ▌▀Æ▄▀▄███"
           ▄██▄██▌████      ▄███▐██▄██▄
          ╙▀▀▀████▄`]▌      ▐▌`▄████▀▀▀▀
               ████▐▌Æ▀▀¬¬▀▀&▐▌▐███
               ▐██  █ ██  ██ █  ███
               ▐██  ]██▄▄▄▄█▄▌  ██▌
                ▀▀█▌,██▀▀▀▀██µ▄█▀▀
                  ██████████████
                  "╘██`-  ¬ ▐█▀"
                     █▄▄  ╒ █
                      ██  ██
                       ▀██▀
                       
"""

def main(repeat_count):
    """Main function to run the survey specified times."""
    # Check for updates before proceeding
    if updater.update(VERSION, repeat_count):
        print(LOGO)  # Display logo only once if no update happens

    # Run the survey the specified number of times
    for _ in range(repeat_count):
        if BROWSER.lower() in ["chrome", "edge"]:
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")  # clear line
        survey = Survey(BROWSER)
        survey.run()


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
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error(traceback.format_exc())
    # Removed the finally block with sys.exit()

