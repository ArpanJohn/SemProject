# importing all needed functions
import os
from astropy.io import fits
import numpy as np
import glob
import io
from contextlib import redirect_stdout
from Tools import tools
from Calculating_det_angles import estimate_source_angles_detectors #importing ma'ams function

import pandas as pd
df = pd.read_csv('all_events.csv')

# Shuffle the DataFrame
df_shuffled = df.sample(frac=1, random_state=42)  # Set random_state for reproducibility

event_counter = {'GRB' : 0, 'SFLARE': 0 , 'TGF': 0, 'SGR':0,'DISTPAR':0}
event_limit = 10

event_type, name = [], []
for index, row in df_shuffled.iterrows():
    if event_counter[row['event_type']] < event_limit:
        event_counter[row['event_type']] += 1
        event_type.append(row['event_type'])
        name.append(row['name'])
    elif event_counter['GRB'] == event_limit and event_counter['SFLARE'] == event_limit and event_counter['TGF'] == event_limit and event_counter['SGR'] == event_limit and event_counter['DISTPAR'] == event_limit:
        break

for i,j in zip(event_type,name):
    print(i,j)

event_list = name

# getting only the event names
# for entry in html_string:
#     if 'bn' in entry:
#         event_list.append(entry)

# list of events and transient type and data set name
event_list = event_list
# transient_type = 'SFLARE'
data_set_name = '27.01-5_'

# list of bin sizes
bin_list = [0.001,0.005,0.01,0.1,0.5,1,5]

# time interval around trigger
ti = [-10,100]

dir_path = tools.json_path(r'data_path.json')

# creating the data set folder
data_set_path = os.path.join(dir_path,data_set_name)
tools.create_folder(data_set_path)

for event,type in zip(event_list,event_type):
    year = '20'+event[2:4]+"/"

    # creating a temperary folder to download the data before processing into .txt files
    temp_path = os.path.join(dir_path, r'temp')
    tools.create_folder(temp_path)
    
    # URL of the file you want to download
    url = 'wget -q -nH --no-check-certificate --cut-dirs=7 -r -l0 -c -N -np -A "*_trigdat_*" -R "index"* -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/'+year+event+'/current/'
    tools.run_wget_download(url,temp_path)

    # Finding Trigdat file
    trig_string = "_trigdat_"
    trig_pattern = os.path.join(temp_path,'current', f"*{trig_string}*")
    trigdat_file = glob.glob(trig_pattern)
    
    # Get the spacecraft pointing from here 
    event_filename = trigdat_file[0]

    # Getting the RA and DEC
    with fits.open(event_filename, memmap=True) as pha_list:
        ra_obj,dec_obj = (pha_list[0].header['RA_OBJ']) ,	(pha_list[0].header['DEC_OBJ'])

    trap = io.StringIO()
    with redirect_stdout(trap):
        brightest_nai, bright_nais, brightest_bgo = estimate_source_angles_detectors.angle_to_grb(ra_obj,dec_obj,event_filename) # Getting the values
    
    # URL of the tte file to download
    url = 'wget -q -nH --no-check-certificate --cut-dirs=7 -r -l0 -c -N -np -A "*_tte_'+brightest_nai+'_*" -R "index"* -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/fermi/data/gbm/triggers/'+year+event+'/current/'
    # Construct the wget command
    tools.run_wget_download(url,temp_path)

    # Use the glob module to search for TTE files in the directory
    target_string = "_tte_"
    file_pattern = os.path.join(temp_path,'current', f"*{target_string}*")
    NaI_detector = glob.glob(file_pattern)

    print('NaI_detector used',NaI_detector[0])

    # fetchinng data
    with fits.open(NaI_detector[0], memmap=True) as hdul:
        energy_channel_data = hdul[1].data.copy()
        all_count_data = np.array(hdul[2].data.copy())

    # getting counts accross all energy channels
    counts = [float(sublist[0]) for sublist in all_count_data]

    data_array = []

    for i in bin_list:
        # Define the range and number of bins
        range_min = ti[0]
        range_max = ti[-1]
            
        bin_size = i

        # Create bin edges
        bin_edges = np.arange(range_min, range_max, bin_size)

        # Create the histogram using numpy.histogram
        hist, edges = np.histogram(counts, bins=bin_edges)

        data_array = data_array + list(hist)

    data_array = np.array(data_array)

    # Save the array to a text file
    data = os.path.join(data_set_path,type+'_'+event)
    np.savetxt(data, data_array, fmt='%d', delimiter='\t')

print('\n----------------------------------------------------------------------------\n\nevents', event_list, ' in folder', data_set_path)
