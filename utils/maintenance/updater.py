import requests
import zipfile
import os
import sys
import shutil
from io import BytesIO
from packaging import version
import subprocess
import logging
import traceback


def get_latest_github_release(user, repo):
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        latest_version = response.json()['tag_name']
        zip_url = response.json()['zipball_url']
        print(f"Latest release fetched: {latest_version}")
        return latest_version, zip_url
    else:
        print(f"Error: Unable to fetch the latest release from GitHub. Status code: {response.status_code}")
        return None, None


def compare_versions(local_version, latest_version):
    if version.parse(local_version) > version.parse(latest_version):
        print(f"You are using a development version: {local_version}. Latest release: {latest_version}")
        return False
    elif version.parse(local_version) < version.parse(latest_version):
        print(f"A new version is available: {latest_version}. You are using: {local_version}")
        return True
    else:
        return False  # No print statement here



def download_and_extract_zip(url, extract_to):
    print(f"Downloading latest release from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            print(f"Extracting files to {extract_to}")
            zip_ref.extractall(extract_to)
        return True
    else:
        print(f"Error: Unable to download the zip file. Status code: {response.status_code}")
        return False


def should_skip(file_path):
    if file_path in ['config.ini', 'cleanup.log', '.git']:
        return True
    if file_path.startswith('language_packs') and file_path != 'language_packs/default.db':
        return True
    return False


def remove_unwanted_directories():
    unwanted_dirs = ['.idea', 'venv']
    for unwanted_dir in unwanted_dirs:
        if os.path.exists(unwanted_dir):
            logging.info(f"Removing unwanted directory {unwanted_dir}")
            try:
                shutil.rmtree(unwanted_dir)
                logging.info(f"Successfully removed {unwanted_dir}")
            except Exception as e:
                logging.error(f"Failed to remove {unwanted_dir}: {e}")

    logging.info("Finished removing unwanted directories")


def update_files(src_dir, dst_dir):
    try:
        src_items = set(os.listdir(src_dir))
        dst_items = set(os.listdir(dst_dir))

        # Copy items from the source to the destination
        for item in src_items:
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            relative_path = os.path.relpath(dst_path, dst_dir)

            if should_skip(relative_path):
                logging.info(f"Skipping update of {relative_path}")
                continue

            if os.path.isdir(src_path):
                if not os.path.exists(dst_path):
                    logging.info(f"Copying directory {src_path} to {dst_path}")
                    shutil.copytree(src_path, dst_path)
                else:
                    logging.info(f"Updating directory {relative_path}")
                    update_files(src_path, dst_path)  # Recursively update nested directories
            else:
                logging.info(f"Writing file {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)  # Only copy and replace files

    except Exception as e:
        logging.error(f"Error updating files: {e}")
        logging.error(traceback.format_exc())


def cleanup_temp_dir(temp_dir):
    try:
        print(f"Cleaning up temporary directory {temp_dir}")
        shutil.rmtree(temp_dir)
    except Exception as e:
        logging.error(f"Error cleaning up: {e}")
        logging.error(traceback.format_exc())


def install_requirements():
    try:
        print("Installing requirements from requirements.txt")
        subprocess.check_call(["python", "-m", "pip", "install", "-q", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")


def ask_for_update():
    while True:
        user_input = input("A new version is available. Would you like to update? (y/n): ").strip().lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            print("Update aborted.")
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")


def relaunch_main(repeat_count):
    try:
        print(f"Relaunching main.py with argument repeat_count={repeat_count}")
        subprocess.Popen([sys.executable, 'main.py', str(repeat_count)])  # Relaunch main.py with the argument
    except Exception as e:
        logging.error(f"Failed to relaunch main.py: {e}")
        logging.error(traceback.format_exc())
    finally:
        sys.exit(0)  # Exit the current process only if relaunching


def update(local_version, repeat_count):
    latest_version, zip_url = get_latest_github_release('bytewired9', 'dirtydubs')
    if latest_version and zip_url:
        if compare_versions(local_version, latest_version):
            if ask_for_update():
                temp_dir = 'temp_update'
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                if download_and_extract_zip(zip_url, temp_dir):
                    extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
                    print("Updating files...")
                    update_files(extracted_dir, '.')
                    print("Removing unwanted directories...")
                    remove_unwanted_directories()
                    print("Installing requirements...")
                    install_requirements()
                    print("Update completed successfully.")

                    # Relaunch main.py with repeat_count after update
                    relaunch_main(repeat_count)
                else:
                    print("Update failed during download and extraction.")
                    sys.exit(1)  # Exit only on failure
            else:
                print("Skipping the update.")
                return  # Exit the function without terminating the script
        else:
            print("You are already using the latest version.")
            return  # Exit the function without terminating the script
    else:
        print("Could not determine the latest version.")
        sys.exit(1)  # Exit on failure to fetch the latest version

