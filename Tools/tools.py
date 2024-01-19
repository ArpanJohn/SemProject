from bs4 import BeautifulSoup
import shutil
import subprocess
import os
import json

def json_path(path):
    with open(path, 'r') as f:
        data = json.load(f)
    for key,value in data.items():
        if key == 'data_path':
            return value

def extract_strings_html(html_file_path):
    try:
        # Open and read the HTML file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract all strings from the HTML content
        all_strings = soup.stripped_strings

        strings = []

        # Print the extracted strings
        for string in all_strings:
            strings.append(string)

    except FileNotFoundError:
        print(f"File '{html_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return strings


def create_folder(folder): # to create the file to store data in
    print(folder)
    try:
        shutil.rmtree(folder)
        print(f"Folder '{folder}' and its contents removed successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder}' not found.")
    except OSError as e:
        print(f"An error occurred: {e} \n also", print(folder))
    try:
        os.mkdir(folder)
        print(f"Folder '{folder}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_wget_download(url,download_folder):
    wget_command = f"{url} -P {download_folder}"
    try:
        # Run the wget command
        print('download start')
        subprocess.run(wget_command, shell=True, check=True)
        print(f"Downloaded {wget_command.split('/')[-3:-1]} to {download_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")