#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 21:02:27 2024

@author: sabine
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 14:01:50 2024

@author: sabine
"""
import numpy as np
import matplotlib.pyplot as plt
import cmcrameri.cm as cmc
colormap = cmc.batlowS
x_start, y_start = 10, 20  # Starting point of the arrow
x_end, y_end = 14.5, 18      # End point of the arrow
# Load data
data_localizer = np.loadtxt('LogFile_2024-10-24_localizer_.txt', skiprows=1, delimiter=',', usecols=(0, 1))
data_FlowSeq = np.loadtxt('LogFile_2024-10-24_SiemensFlowSeq.txt', skiprows=1, delimiter=',', usecols=(0, 1))
data_FlowSeq_wForce = np.loadtxt('LogFile_2024-11-04_19.31.50.txt', skiprows=1, delimiter=',', usecols=(0, 1))

# Adjust time to start from zero for each dataset
time_localizer = data_localizer[:, 0] - data_localizer[0, 0]
time_FlowSeq = data_FlowSeq[:, 0] - data_FlowSeq[0, 0]
time_FlowSeq_wForce = data_FlowSeq_wForce[:, 0] - data_FlowSeq_wForce[0, 0]

# Initialize figure and subplots for broken x-axis
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 8), dpi=300)
fig.subplots_adjust(wspace=0.13)  # Adjust space between the two plots

# Plot data on both axes
#ax1.plot(time_FlowSeq, data_FlowSeq[:, 1] - data_FlowSeq[1, 1], color=colormap(0), linewidth=2.5, label='4D Phase Contrast Gradient Echo Sequence')
ax1.plot(time_FlowSeq_wForce, data_FlowSeq_wForce[:, 1] - data_FlowSeq_wForce[1, 1], color=colormap(2), linewidth=2.5, label='4D Phase Contrast w/ Force')
ax1.plot(time_localizer, data_localizer[:, 1] - data_localizer[1, 1], color=colormap(4), linewidth=3.0, label='Localizer')


#ax2.plot(time_FlowSeq, data_FlowSeq[:, 1] - data_FlowSeq[1, 1], color=colormap(0), linewidth=2.5, label='4D Phase Contrast GRE Sequence')
ax2.plot(time_FlowSeq_wForce, data_FlowSeq_wForce[:, 1] - data_FlowSeq_wForce[1, 1], color=colormap(2), linewidth=2.5, label='2D Phase Contrast GRE with Force')
ax2.plot(time_localizer, data_localizer[:, 1] - data_localizer[1, 1], color=colormap(4), linewidth=3.0,label='Localizer')

# Set x-axis limits to create break
ax1.set_xlim(0, 25)
ax2.set_xlim(220, time_FlowSeq.max())

# Hide spines between the two plots to emphasize the break
ax1.spines['right'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
# Add diagonal lines to indicate the break in the x-axis
d = 0.915  # Adjust as needed for visual appeal
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle="none", color='k', clip_on=False)
ax1.plot([1], [1], transform=ax1.transAxes, **kwargs)
ax1.plot([1], [0], transform=ax1.transAxes, **kwargs)
ax2.plot([0], [1], transform=ax2.transAxes, **kwargs)
ax2.plot([0], [0], transform=ax2.transAxes, **kwargs)

# add slanted line on the graph
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle="none", color=colormap(2), clip_on=False)

ax1.plot([1], [0.43], transform=ax1.transAxes, **kwargs)
ax2.plot([0], [0.43], transform=ax2.transAxes, **kwargs) 

#kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12, linestyle="none", color=colormap(0), clip_on=False)
#ax1.plot([1], [0.28], transform=ax1.transAxes, **kwargs)
#ax2.plot([0], [0.28], transform=ax2.transAxes, **kwargs) 

# Increase x-axis tick label font size
ax1.tick_params(axis='x', labelsize=16)  # Set fontsize for x-axis ticks
ax1.tick_params(axis='y', labelsize=16)  # Set fontsize for y-axis ticks
ax2.tick_params(axis='x', labelsize=16)  # Set fontsize for x-axis ticks
ax2.tick_params(axis='y', labelsize=16)  # Set fontsize for y-axis ticks

# Set labels
fig.text(0.5, 0.04, 'Time [s]', ha='center', fontsize=18, fontweight='bold', color='black')
ax1.set_ylabel('Measured Force [kg]', fontsize=18, fontweight='bold', color='black')

#add arrow
ax1.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
             arrowprops=dict(arrowstyle='->', color='black', lw=2))

# Add legend to the first plot only
#ax1.legend(fontsize=14, loc='upper right', frameon=True, framealpha=1, edgecolor='black', fancybox=True)
# Add legend to the first plot, in the upper right
ax2.legend(fontsize=16, loc='upper right', bbox_to_anchor=(1, 1), frameon=True, framealpha=1, edgecolor='black', fancybox=True)

#add gridd to enhance readability
ax2.grid(True, linestyle='--',linewidth=0.7,color='gray',alpha=0.7)
ax1.grid(True, linestyle='--',linewidth=0.7,color='gray',alpha=0.7)

# Show plot
plt.show()