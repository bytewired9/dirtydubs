# DirtyDubs

## Overview

Dirtydubs is an automation script designed to automate the process of navigating and completing BWW surveys.

## Features

- **Automated Survey Navigation**: The script navigates through the survey, selecting predefined options and filling out necessary fields.
- **Review Generation**: Generates realistic review texts using predefined phrases and patterns. The probability that two randomly generated reviews will be the same is approximately $\( \frac{1}{1000000000000} \)$. You have better chances of becoming an *astronaut*.
- **Configurable**: Customizable configurations through a `config.ini` file to specify store ID, order types, order receptions, and order times.
- **Logging**: Detailed logging to track the execution process and any errors encountered.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/bytewired9/dirtydubs.git
    cd dirtydubs
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Setup

1. **Run `install.bat`**

2. **Set up the configuration file**:
    Ensure the `config.ini` is edited to your needs.\
    *Suggestion: remove breakfast and overnight from your config*
   
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

```
dirtydubs/
├── language_packs/
│   └── default.db
│
├── proxy/
│   ├── background.js
│   └── manifest.json
│
├── utils/
│   ├── generator/
│   │   ├── review_generator.py
│   │   └── reviewgen.py
│   │ 
│   ├── packmaker/
│   │   ├── example.py
│   │   ├── reviewlist.py
│   │   └── tree.py
│   │ 
│   ├── webdriver/
│   │   ├── web_driver_factory.py
│   │   └── web_driver_waiter.py
│   │ 
│   ├── click_helper.py
│   ├── config_manager.py
│   ├── survey.py
│   └── survey_selector.py
│
├── requirements.txt
├── main.py
└── setup.bat
```
## Logging

Logging is configured to provide detailed information about the script's execution. The log messages include timestamps, log levels, and detailed messages. Adjust the logging configuration in `main.py` as needed.

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or support, please open an issue on the GitHub repository.

---
