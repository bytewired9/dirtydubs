import configparser
import logging
import os
import sys

class ConfigManager:
    """Manager class for configuration operations."""

    CONFIG_FILE = './config.ini'

    @staticmethod
    def check_and_create_config():
        """Check if the config file exists, if not create one with default values."""
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            ConfigManager.create_default_config()
            logging.info("Config file created. Please edit 'config.ini' to your needs.")
            sys.exit()
        else:
            ConfigManager.ensure_config_fields()

    @staticmethod
    def create_default_config():
        """Create a default configuration file with comments."""
        with open(ConfigManager.CONFIG_FILE, 'w', encoding="utf-8") as file:
            file.write(
                """# Store ID: The store number of your BWW
[store_id]
id = INSERT_STORENO_HERE

# Order types: you can specify multiple types separated by spaces
[order]
type_of_order = call web app walkin
type_of_order_weights = 1 1 1 1

order_reception = carryout delivery dinein
order_reception_weights = 1 1 1

order_time = breakfast lunch midday dinner latenight overnight
order_time_weights = 1 1 1 1 1 1


# Survey chance: probability of receiving a survey, value between 0 and 1
survey_chance = 0.2

[automatic]
auto = False
run_in_background = False
surveys_per_hour = 1.5

"""
            )

    @staticmethod
    def ensure_config_fields():
        """Ensure all required fields are present in the config file, append missing fields with defaults."""
        # Load the existing config with comments preserved
        with open(ConfigManager.CONFIG_FILE, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        config = configparser.ConfigParser()
        config.read(ConfigManager.CONFIG_FILE)

        # Default values to check against
        default_values = {
            'store_id': {
                'id': 'INSERT_STORENO_HERE'
            },
            'order': {
                'type_of_order': 'call web app walkin',
                'type_of_order_weights': '1 1 1 1',
                'order_reception': 'carryout delivery dinein',
                'order_reception_weights': '1 1 1',
                'order_time': 'breakfast lunch midday dinner latenight overnight',
                'order_time_weights': '1 1 1 1 1 1',
                'survey_chance': '0.2'
            },
            "automatic": {
                "auto": "False",
                "run_in_background": "False",
                "surveys_per_hour": "1.5"
            }
        }

        # Track changes made
        updated = False
        new_lines = []

        # Add missing sections or options
        for section, fields in default_values.items():
            if not config.has_section(section):
                # Add the entire section if it's missing
                new_lines.append(f"\n[{section}]\n")
                for field, value in fields.items():
                    new_lines.append(f"{field} = {value}\n")
                updated = True
                logging.info(f"Added missing section: {section}")
            else:
                new_lines.append(f"[{section}]\n")
                for field, value in fields.items():
                    if not config.has_option(section, field):
                        new_lines.append(f"{field} = {value}\n")
                        updated = True
                        logging.info(f"Added missing field '{field}' in section '{section}' with default value '{value}'")
                    else:
                        # Keep existing fields as they are
                        for line in lines:
                            if line.strip().startswith(f"{field} ="):
                                new_lines.append(line)
                                break

        # Append any remaining original lines that weren't changed
        for line in lines:
            if not any(line.strip().startswith(f"[{section}]") or line.strip().startswith(f"{field} =") for section in default_values for field in default_values[section]):
                new_lines.append(line)

        # Write the updated config back to the file
        if updated:
            with open(ConfigManager.CONFIG_FILE, 'w', encoding="utf-8") as file:
                file.writelines(new_lines)
            logging.info("Config file was missing fields. Missing fields have been added with default values.")

    @staticmethod
    def read_config():
        """Read the configuration file."""
        config = configparser.ConfigParser()
        config.read(ConfigManager.CONFIG_FILE)

        store_id = config.get('store_id', 'id')

        order_types = config.get('order', 'type_of_order').split()
        order_type_weights = list(map(int, config.get('order', 'type_of_order_weights').split()))

        order_receptions = config.get('order', 'order_reception').split()
        order_reception_weights = list(map(int, config.get('order', 'order_reception_weights').split()))

        order_times = config.get('order', 'order_time').split()
        order_time_weights = list(map(int, config.get('order', 'order_time_weights').split()))

        survey_chance = config.get('order', 'survey_chance')

        auto = config.get('automatic', 'auto')
        run_in_background = config.get('automatic', 'run_in_background')
        surveys_per_hour = config.get('automatic', 'surveys_per_hour')

        print("config_manager.py", store_id, order_types, order_type_weights, order_receptions, order_reception_weights, order_times, order_time_weights, survey_chance, auto, run_in_background, surveys_per_hour )
        return [
            store_id,
            order_types,
            order_type_weights,
            order_receptions,
            order_reception_weights,
            order_times,
            order_time_weights,
            survey_chance,
            auto,
            run_in_background,
            surveys_per_hour
        ]



