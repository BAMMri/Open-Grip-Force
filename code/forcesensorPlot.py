#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 18:38:57 2024

@author: sabine
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from scipy.stats import linregress
import cmcrameri.cm as cmc

#get costum colors
# Define the number of categories you want to extract
num_categories = 10  # Adjust this based on your needs

# Get the Batlow colormap
batlow_colormap = cmc.batlowS
# Extract the colors
colors = [batlow_colormap(i / num_categories) for i in range(num_categories)]
colormap = cmc.batlowS
# Step 1: Load the data
data = np.loadtxt('force_data.txt')

# Separate columns
measured_forces = data[:, :3]      # First three columns
reference_force = data[:, 3]       # Fourth column


# Step 2: Calculate the average and standard error for measured forces
mean_measured_force = np.mean(measured_forces, axis=1)
std_error_measured_force = np.std(measured_forces, axis=1, ddof=1) / np.sqrt(measured_forces.shape[1])

# Do the linear regression fit
slope, intercept, r_value, p_value, std_err = linregress(reference_force, mean_measured_force)
r_squared=r_value**2
print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"R-squared: {r_value**2}")

# Step 3: Create a high-contrast scatter plot with enhanced features
plt.figure(figsize=(10, 8), dpi=300)  # High resolution for publication

# High-contrast error bars and markers
plt.errorbar(
    reference_force, 
    mean_measured_force, 
    yerr=std_error_measured_force, 
    fmt='o', 
    markersize=10,  # Large markers
    color=colormap(2), 
    #color=colors[4],
    #alpha=0.7,  # Set transparency for markers
    ecolor=colormap(2), 
    elinewidth=2, 
    capsize=5, 
    label='Force (Mean ± SD)'
)

# Labels and title with larger, bold fonts
plt.xlabel('Reference Weight [kg]', fontsize=18, fontweight='bold', color='black')
plt.ylabel('Measured Force [kg]', fontsize=18, fontweight='bold', color='black')
#plt.title('Comparison of Measured and Reference Forces', fontsize=18, fontweight='bold', color='black')

# Step 4: Add the ideal linear line (y = x line) with a thick, high-contrast dashed line
min_force = min(reference_force.min(), mean_measured_force.min())
max_force = max(reference_force.max(), mean_measured_force.max())
plt.plot(
    [min_force, max_force], 
    [min_force, max_force], 
    'k--', 
    linewidth=2.0,  # Thicker line
    label='Identity'
)
#add the linear regression
plt.plot(reference_force, slope * reference_force + intercept, color=colormap(4), label=f'Linear fit,  R² = {r_squared:.3f})'  # Format R² value)
)

# Step 5: Improve legend readability
plt.legend(fontsize=16, loc='upper left', frameon=True, framealpha=1, edgecolor='black', fancybox=True)
plt.xticks(fontsize=16)  # Increase x-axis tick label font size
plt.yticks(fontsize=16)  # Increase y-axis tick label font size

# Step 6: Add grid for easier reference
plt.grid(True, linestyle='--', linewidth=0.7, color='gray', alpha=0.7)



# Save the figure in a high-resolution format for publications
#plt.savefig("force_vs_reference_plot.png", format="png", dpi=300, bbox_inches="tight")

# Show the plot
plt.show()


