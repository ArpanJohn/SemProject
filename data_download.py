# importing all needed functions
import os
import shutil
import json
from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from fast_histogram import histogram1d
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
from astropy.io import ascii
import matplotlib.patches as mpatches
from matplotlib import rc,rcParams
from astropy.table import Table
# %matplotlib inline
# %matplotlib notebook
from astropy.io import fits
from numpy import arange
import json
import subprocess
from Calculating_det_angles import estimate_source_angles_detectors #importing ma'ams function
import matplotlib.image as mpimg

# Getting the path the data directory from json file
# Specify the path to your JSON file
json_file_path = "data_path.json"

# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Access the path from the JSON data
path_value = data.get("data_path", "")

# Print or use the path as needed
print("data_path:", path_value)


# To download new sample data 

def create_folder(folder): # to create the file to store data in
    print(folder)
    try:
        shutil.rmtree(folder)
        print(f"Folder '{folder}' and its contents removed successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder}' not found.")
    except OSError as e:
        print(f"An error occurred: {e}")
    try:
        os.mkdir(folder)
        print(f"Folder '{folder}' created successfully.")
    except FileExistsError:
        print(f"Folder '{folder}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Change according to the transients you want to download note they all have to be of same type
download_list = ['bn130623488','bn110819665'] #'bn220730659','bn120227725','bn101227195','bn160919613','bn100507577',
transient_type = 'GRB'


download_number = 0
for name in download_list:
    folder_name = transient_type + '_' + name #input("Enter the name of the folder you want to create: ")
    name = name
    year = '20'+name[2:4]+"/"

    folder_path = os.path.join(path_value, folder_name)

    create_folder(folder_path)
    
    # URL of the file you want to download
    url1 = "wget -q -nH --no-check-certificate --cut-dirs=7 -r -l0 -c -N -np -A fit -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/"+year+name+'/current/'
    url2 = "wget -q -nH --no-check-certificate --cut-dirs=7 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/"+year+name+'/quicklook/'

    # Directory where you want to save the downloaded file
    download_folder = folder_path

    # Construct the wget command
    wget_command1 = f"{url1} -P {download_folder}"
    wget_command2 = f"{url2} -P {download_folder}"

    try:
        # Run the wget command
        subprocess.run(wget_command2, shell=True, check=True)
        print(f"Downloaded {url2.split('/')[-3:]} to {download_folder}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    try:
        # Run the wget command
        subprocess.run(wget_command1, shell=True, check=True)
        print(f"Downloaded {url1.split('/')[-3:]} to {download_folder}")
        download_number = download_number + 1
    except subprocess.CalledProcessError as e:
        print(f"Error downloading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    


print(download_number,' samples downloaded')