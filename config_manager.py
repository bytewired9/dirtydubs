import configparser
import logging
import os
import sys


class ConfigManager:
    """Manager class for configuration operations."""

    CONFIG_FILE = 'config.ini'

    @staticmethod
    def check_and_create_config():
        """Check if the config file exists, if not create one with default values."""
        if not os.path.exists(ConfigManager.CONFIG_FILE):
            with open(ConfigManager.CONFIG_FILE, 'w', encoding="utf-8") as file:
                file.write(
                    """# Store ID: The store number of your BWW"
[store_id]
id = INSERT_STORENO_HERE

# Order types: you can specify multiple types separated by spaces
[order]
type_of_order = call web app walkin

# Order reception modes: you can specify multiple modes separated by spaces
order_reception = carryout delivery dinein

# Order times: you can specify multiple times separated by spaces
order_time = breakfast lunch midday dinner latenight overnight
"""
                )
            logging.info("Config file created. Please edit 'config.ini' to your needs.")
            sys.exit()

    @staticmethod
    def read_config():
        """Read the configuration file."""
        config = configparser.ConfigParser()
        config.read(ConfigManager.CONFIG_FILE)
        store_id = config.get('store_id', 'id')
        order_types = config.get('order', 'type_of_order').split()
        order_receptions = config.get('order', 'order_reception').split()
        order_times = config.get('order', 'order_time').split()
        return store_id, order_types, order_receptions, order_times
