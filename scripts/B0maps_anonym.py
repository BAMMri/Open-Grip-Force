#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:43:21 2024

@author: sabine
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:20:44 2024

@author: sabine
"""
# Imports
import pydicom
import os
import numpy as np 
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
import ipywidgets as widgets  # make sure ipywidgets is imported

from scipy import ndimage
from IPython.display import clear_output
from scipy.stats import linregress
from scipy import ndimage, datasets
from skimage.filters import threshold_otsu
from skimage.measure import label

# Functions
#######---- functions used but not applied for anonym purpose ----- #####

def transfrom_siemens_phase_img(dicom_datasets):
    phase_pixel_data=dicom_datasets.pixel_array
    transformed_volume = (phase_pixel_data - phase_pixel_data.max() / 2) / phase_pixel_data.max() * 2 * np.pi
    print(transformed_volume.max())
    print(transformed_volume.min())
    return(transformed_volume)
def get_echo_times(ds):
    #input pydicom elemnt from pydicom.dcmread, enhanced dicoms
    effective_echo_time = ds[(0x5200, 0x9230)][0][(0x0018, 0x9114)][0][(0x0018, 0x9082)].value
    return(effective_echo_time)

def read_dicoms_in_folder(folder_path):
    """
    Reads all DICOM files in the specified folder and returns them as a list of datasets.

    Parameters:
        folder_path (str): Path to the folder containing DICOM files.

    Returns:
        list: A list of pydicom Dataset objects for each DICOM file read.
    """
    dicom_datasets = []

    # Loop through all files in the directory
    for filename in os.listdir(folder_path):
        # Construct full file path
        filepath = os.path.join(folder_path, filename)
        
        # Ensure it's a DICOM file (you can add more checks if needed)
        if os.path.isfile(filepath):
            try:
                # Load the DICOM file and append it to the list
                ds = pydicom.dcmread(filepath)
                dicom_datasets.append(ds)
                print(f"Loaded DICOM file unsorted: {filename}")
            except Exception as e:
                print(f"Could not read {filename}: {e}")

    # Sort the DICOM datasets by InstanceNumber
    dicom_datasets.sort(key=lambda x: int(x.InstanceNumber))
    
    print(f"Total DICOM files loaded and sorted: {len(dicom_datasets)}")
    return dicom_datasets

##### B0 Diff map code #####

def calc_B0_Sabine(true_phase_img_list,echos_list):
    phaseDifference=true_phase_img_list[0]-true_phase_img_list[1]
    BzMap = phaseDifference/((echos_list[1]-echos_list[0])/1000) # in rad/s
    BzMapHz = BzMap/2/np.pi #Offresonance Map in Hz -BzMap
    return(BzMapHz)


#LoadData
# Load all saved arrays
echotimes_array_fs = np.load("echotimes_array_fs.npy")
echotimes_array = np.load("echotimes_array.npy")
phase_img_pixel_rescaled_fs = np.load("phase_img_pixel_rescaled_fs.npy")
phase_img_pixel_rescaled = np.load("phase_img_pixel_rescaled.npy")
label_image = np.load("label_image.npy")

#Do the B0 maps SM
B_0_Hz_SM_fs=calc_B0_Sabine(phase_img_pixel_rescaled_fs,echotimes_array_fs)
B_0_Hz_SM=calc_B0_Sabine(phase_img_pixel_rescaled,echotimes_array)

#make difference image and plot
image_data=(B_0_Hz_SM_fs-B_0_Hz_SM)*label_image
masked_image_data = np.where(image_data == 0, np.nan, image_data)

print('Mean Difference', np.nanmean(masked_image_data))
print('STD Difference',np.nanstd(masked_image_data))

## Visualize the B0 difference map for the abstract and export
import cmcrameri.cm as cmc  # Import cmcrameri colormaps
image_data=(B_0_Hz_SM_fs-B_0_Hz_SM)*label_image
# Set zero values to NaN so they appear as white in the plot
masked_image_data = np.where(image_data == 0, np.nan, image_data)
slice_index=16;

# Create the plot
plt.figure(figsize=(10, 8), dpi=300)  
im=plt.imshow(masked_image_data[slice_index, :, : ], cmap=cmc.batlow)  # Use the 'fir' color map from cmcrameri
cbar = plt.colorbar(im, label="Off-Resonance Difference [Hz]")
cbar.ax.tick_params(labelsize=14)  # Increase font size for color bar ticks
cbar.set_label(r"$\Delta B_0$ [Hz]", fontsize=16)  # Bold label for color bar
#plt.colorbar(label="Difference [Hz]")  # Add color bar for reference
plt.title("Off-Resonance Difference Map", fontsize=20,fontweight='bold')
plt.axis("off")  # Optional: hide the axis for a cleaner image

# Specify a directory path where the image should be saved
output_path = "/home/sabine/Projects/SM_ForceSensor/FiguresISMRM/Off-Resonance-Diff.png"

# Save the figure to the specified location
plt.savefig(output_path, format="png", dpi=300, bbox_inches="tight")
# Display the plot
plt.show()