# DirtyDubs

## Overview

Dirtydubs is an automation script designed to automate the process of navigating and completing online surveys, specifically for Inspire Brands' Qualtrics surveys. The script leverages Selenium WebDriver to interact with the survey pages, and it can generate and input review text to the survey forms.

## Features

- **Automated Survey Navigation**: The script navigates through the survey, selecting predefined options and filling out necessary fields.
- **Review Generation**: Generates realistic review texts using predefined phrases and patterns. The probability that two randomly generated reviews will be the same is approximately \(2.70 \times 10^{-9}\), or 0.00000027%, which is extremely low.
- **Configurable**: Customizable configurations through a `config.ini` file to specify store ID, order types, order receptions, and order times.
- **Logging**: Detailed logging to track the execution process and any errors encountered.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/dirtydubs.git
    cd dirtydubs
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Setup the configuration file**:
    Ensure the `config.ini` file is in the root directory of the project. If it doesn't exist, the script will generate a template for you on the first run. Edit this file to match your requirements.

## Configuration

The configuration is managed via the `config.ini` file:

```ini
# Store ID: The store number of your BWW
[store_id]
id = INSERT_STORENO_HERE

# Order types: you can specify multiple types separated by spaces
[order]
type_of_order = call web app walkin

# Order reception modes: you can specify multiple modes separated by spaces
order_reception = carryout delivery dinein

# Order times: you can specify multiple times separated by spaces
order_time = breakfast lunch midday dinner latenight overnight
```

## Usage

Run the main script with the desired number of repetitions:

```sh
python main.py 5
```

This command will run the survey automation process 5 times.

## Project Structure

- **main.py**: Entry point of the application. Manages the overall workflow and repeats the survey process based on user input.
- **config_manager.py**: Manages configuration file operations, including checking and reading the configuration.
- **survey.py**: Core logic for running the survey, integrating various helper classes to perform specific tasks.
- **survey_selector.py**: Contains methods for selecting survey options and navigating through the survey pages.
- **review_generator.py**: Handles the generation of review text to be input into the survey.
- **click_helper.py**: Provides methods to safely click on web elements, handling potential exceptions.
- **web_driver_factory.py**: Factory class for creating web driver instances.
- **web_driver_waiter.py**: Helper class for waiting for specific conditions to be met in the web driver.
- **reviewgen.py**: Contains the logic for generating realistic review text using predefined phrases and patterns.

## Logging

Logging is configured to provide detailed information about the script's execution. The log messages include timestamps, log levels, and detailed messages. Adjust the logging configuration in `main.py` as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or support, please open an issue on the GitHub repository.

---
