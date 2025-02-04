#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 20:48:37 2024

@author: sabine
"""
import matplotlib.pyplot as plt
import napari
from read_enhanced_dicom import read_enhanced_dicom
import numpy as np
import pydicom
from skimage.filters import threshold_otsu
from skimage.measure import label
import os
from scipy import stats

### code not used due to anonymisation 
# Load Dicoms
def load_dicoms_by_category(base_folder):
    noisy_dicoms = []
    clean_dicoms = []

    # Loop through each subfolder in the base directory
    for subfolder_name in os.listdir(base_folder):
        subfolder_path = os.path.join(base_folder, subfolder_name)

        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            # Determine if the folder name indicates a noisy or clean image
            if "0_noise" in subfolder_name:
                category = "noisy"
            elif "90" in subfolder_name:
                category = "clean"
            else:
                print(f"Skipping unrecognized folder: {subfolder_name}")
                continue  # Skip folders that don't match the criteria

            # Find DICOM files in the folder and load them
            for filename in os.listdir(subfolder_path):
                filepath = os.path.join(subfolder_path, filename)
                
                # Ensure it's a DICOM file by trying to read it
                try:
                    ds = pydicom.dcmread(filepath)
                    # Append to the appropriate list based on category
                    if category == "noisy":
                        noisy_dicoms.append(ds)
                    else:
                        clean_dicoms.append(ds)
                    print(f"Loaded {category} DICOM from {subfolder_name}")
                except Exception as e:
                    print(f"Failed to load {filename} in {subfolder_name}: {e}")
    # Sort the DICOM datasets by InstanceNumber
    noisy_dicoms.sort(key=lambda x: int(x.SeriesNumber)*100+int(x.InstanceNumber))
    clean_dicoms.sort(key=lambda x: int(x.SeriesNumber)*100+int(x.InstanceNumber))

    print(f"Total noisy DICOMs loaded: {len(noisy_dicoms)}")
    print(f"Total clean DICOMs loaded: {len(clean_dicoms)}")
    return noisy_dicoms, clean_dicoms
# Get Pixel arrays 
def get_pixel_arrays(dicom_dataset_list):
    dicom_dataset_pixel_list=[]
    for i in range(len(dicom_dataset_list)):
        dicom_dataset_pixel_list.append(dicom_dataset_list[i].pixel_array)
    return(dicom_dataset_pixel_list)
#Mask/Treshold pixel arrays
def make_masks(dicom_pixel_arrary):
    label_masks=[]
    for i in range(len(dicom_pixel_arrary)):
        tresh_value=threshold_otsu(dicom_pixel_arrary[i])
        img_tresh=dicom_pixel_arrary[i]>tresh_value
        label_masks.append(label(img_tresh))
    return(label_masks)
#######################################3
######load pixel arrays#############


noisy_dicoms_pixel = np.load("noisy_dicoms_pixel.npy")
noisy_dicoms_pixel_fs = np.load("noisy_dicoms_pixel_fs.npy")
signal_dicoms_pixel = np.load("signal_dicoms_pixel.npy")
signal_dicoms_pixel_fs = np.load("signal_dicoms_pixel_fs.npy")
maskes_fs = np.load("maskes_fs.npy")
maskes = np.load("maskes.npy")




#calculate the Mean SNR for each slice
def calc_SNR(pixel_array, pixel_array_noise, mask_array):
    mean_signal_array=[]
    std_noise_array=[]
    SNR_array=[]
    for i in range(len(pixel_array)):
        region_mask=[]  
        mask=[]
        img=[]
        noise=[]

        img=pixel_array[i]
        noise=pixel_array_noise[i]
        mask=mask_array[i]
        region_mask = mask ==1
        #print(img.shape)
        #print(noise.shape)
        #print(region_mask.shape)
        
        for j in range(img.shape[0]):
            region_values_slice=[]
            region_values_noise_slice=[]
            img_slice=[]
            noise_slice=[]
            
            img_slice = img[j, :, :]
            noise_slice = noise[j, :, :]
            region_mask_slice = region_mask[j, :, :]
            #print(img_slice.shape)
            #print(noise_slice.shape)
            #print(region_mask_slice.shape)
            region_values_slice=img_slice[region_mask_slice]
            region_values_noise_slice=noise_slice[region_mask_slice]
            
            mean_signal=region_values_slice.mean()
            std_noise=region_values_noise_slice.std()
            mean_signal_array.append(mean_signal)
            std_noise_array.append(std_noise)
            SNR=0.66*mean_signal/std_noise
            SNR_array.append(SNR)
            print(SNR)
    return(mean_signal_array,std_noise_array,SNR_array)


print('SNR no force sensor')
means,stds,snrs=calc_SNR(signal_dicoms_pixel,noisy_dicoms_pixel,maskes)
print(' with force sensor')
means_fs,stds_fs,snrs_fs=calc_SNR(signal_dicoms_pixel_fs,noisy_dicoms_pixel_fs,maskes_fs)

# Perform an paired two-sample t-test
t_stat, p_value = stats.ttest_rel(snrs, snrs_fs)

# Print the results
print("t-statistic paired:", t_stat)
print("p-value paired:", p_value)

# Interpretation
if p_value < 0.05:
    print("There is a statistically significant difference between the two groups.")
else:
    print("There is no statistically significant difference between the two groups.")

# Perform an independent two-sample t-test
t_stat, p_value = stats.ttest_ind(snrs, snrs_fs)

# Print the results
print("t-statistic independent:", t_stat)
print("p-value independent:", p_value)

# Interpretation
if p_value < 0.05:
    print("There is a statistically significant difference between the two groups.")
else:
    print("There is no statistically significant difference between the two groups.")
    
# Calculate mean and standard deviation for each group
mean_snrs = np.mean(snrs)
std_snrs = np.std(snrs)

mean_snrs_fs = np.mean(snrs_fs)
std_snrs_fs = np.std(snrs_fs)

# Calculate the percentage decrease in SNR
percentage_decrease = ((mean_snrs_fs - mean_snrs) / mean_snrs_fs) * 100

# Print the results
print("SNR (no force sensor): Mean =", mean_snrs, ", Std Dev =", std_snrs)
print("SNR (with force sensor): Mean =", mean_snrs_fs, ", Std Dev =", std_snrs_fs)
print("Percentage decrease in SNR:", percentage_decrease, "%")