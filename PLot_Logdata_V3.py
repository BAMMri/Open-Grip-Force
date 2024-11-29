#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 15:35:41 2024

@author: sabine
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:01:50 2024

@author: sabine

Plot Logdata of a single file with triggers 
"""
# Load data using numpy
import numpy as np
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
colormap = cmc.batlowS

FORCE_DELAY_MS = 50

# Load data
#filename = '/home/sabine/Projects/SM_ForceSensor/Measurements/2024_11_21_Pavlos_Bine_Marta/LogFile_2024-11-21_11.10.06.txt' # Replace with your actual file name
filename='/home/sabine/Projects/SM_ForceSensor/Measurements/2024_11_26_Sabine/LogFile_2024-11-26_Sabine_1.txt'
data = np.genfromtxt(filename, delimiter=",", dtype=None, encoding=None, names=["time", "force", "other"],skip_header=1)

#mean_signal_mri=np.load('/home/sabine/Projects/SM_ForceSensor/Measurements/2024_11_26_Sabine/mean_signal_roi4.npy')
#mean_signal_mri_filename='/home/sabine/Projects/SM_ForceSensor/Measurements/2024_11_26_Sabine/mean_signal.npy'
#mean_signal_mri_data=np.genfromtxt(mean_signal_mri_filename, dtype=None, encoding=None, names=["image","roi", "velocity", "vlecity_std"],skip_header=1 )
#mean_signal_mri=mean_signal_mri_data["velocity"]

#optional, make derivative plt.plot(np.linspace(0,22.1*len(disp),disp), -disp)


# Parse columns
time = data["time"]
time=np.squeeze(time[500:,])
force = data["force"]
force=np.squeeze(force[500 :,])
other = data["other"]
other=np.squeeze(other[500 :,])

## Conver focre from scale factor old fs to scalefaktor new SM

# Clean the 'other' column: remove quotes and strip spaces
other_clean = np.char.strip(np.char.replace(other, '"', ''))

# Identify trigger points
trigger_indices = np.where(other_clean == "TRIG")[0]
trigger_times = time[other_clean == "TRIG"]
print(len(trigger_times))
print(trigger_indices)

### make a total plot, just for visualization, naviagation purpose
# Plot force over time
plt.figure(figsize=(12, 6))
plt.plot(time, force, label="Force", color="blue")

# Add vertical lines for triggers
for trigger_time in trigger_times:
    plt.axvline(trigger_time, color="red", linestyle="-", label="Trigger",alpha=0.2)

# Customize plot
plt.xlabel("Time (s)")
plt.ylabel("Force")
plt.title("Force Over Time with Triggers")
plt.legend(["Force", "Trigger"])
plt.grid()
plt.show()

##### Make the actual figure plot 
# Bin data between triggers
binned_data = []
for i in range(len(trigger_indices) - 1):
    start_idx = trigger_indices[i]
    end_idx = trigger_indices[i + 1]
    bin_time = time[start_idx:end_idx] - time[start_idx]  # Relative time within the bin
    bin_force = force[start_idx:end_idx]
    binned_data.append((bin_time, bin_force))

# Universal time scale
max_bin_time = max([bin_time[-1] for bin_time, _ in binned_data])  # Find the longest time bin
#universal_time = np.linspace(0, max_bin_time, 500)  # Resample bins to a common time scale, with 500 steps
universal_time = np.linspace(0, max_bin_time, len(time))  # Universal time scale

# calculate the mean force     
# Resample each bin and calculate the mean force
resampled_forces = []
for bin_time, bin_force in binned_data:
    resampled_force = np.interp(universal_time, bin_time, bin_force)
    resampled_forces.append(resampled_force)


mean_force = np.mean(resampled_forces, axis=0)


# Plotting
plt.figure(figsize=(12, 6))

# Create primary axis
fig, ax1 = plt.subplots(figsize=(12, 6))  # Adjust the size of the figure

# Plot each bin in gray with its actual force
for i, (bin_time, bin_force) in enumerate(binned_data):
    if i == 0:  # Add label only to the first gray line
        ax1.plot(bin_time-float(FORCE_DELAY_MS)/1000, bin_force, color=colormap(2), alpha=0.3, label="Force profile per contraction cycle")
    else:
        ax1.plot(bin_time-float(FORCE_DELAY_MS)/1000, bin_force, color=colormap(2), alpha=0.3)

# Plot mean force in red on the primary y-axis
ax1.plot(universal_time-float(FORCE_DELAY_MS)/1000, mean_force, color=colormap(4), label="Mean force", linewidth=4)
ax1.set_ylabel('Measured Force [kg]', fontsize=18, fontweight='bold', color=colormap(2))
ax1.tick_params(axis='y', labelsize=16, colors=colormap(2))  # Tick params for primary y-axis
ax1.set_xlabel('Time [s]', fontsize=18, fontweight='bold', color='black')
ax1.grid(True, linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
ax1.tick_params(axis='x', labelsize=16)
ax1.set_xlim(0, 1.56)


# legends from both axes

fig.legend(fontsize=16, edgecolor='black', loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
# Show the plot
plt.show()

