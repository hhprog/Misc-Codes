import os  # Import the os module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Change the current working directory
os.chdir(r'C:\Users\Dell\OneDrive\Documents\FoV')  # Replace with your desired directory path

# Function to calculate FWHM and return the min/max angle and the bandwidth
def calculate_fwhm(angle, intensity):
    max_intensity = np.max(intensity)
    half_max = max_intensity / 2
    
    # Find where intensity crosses half max
    indices_above_half = np.where(intensity >= half_max)[0]
    
    if len(indices_above_half) > 1:  # Ensure there are at least two crossings
        left_index = indices_above_half[0]
        right_index = indices_above_half[-1]
        fwhm_min_angle = angle[left_index]
        fwhm_max_angle = angle[right_index]
        fwhm_bandwidth = fwhm_max_angle - fwhm_min_angle
        return fwhm_min_angle, fwhm_max_angle, fwhm_bandwidth, half_max
    else:
        return None, None, None, None

# Load the dataset
df = pd.read_csv('FoV.csv', sep=',')  # The path can be relative since we changed the directory

# Print first few lines of the dataset
print(df.head(),'\n')

# Convert necessary columns to the right types
df['Run ID'] = df['Run ID'].astype(str)
df['Type'] = df['Type'].astype(str)
df['Intensity'] = pd.to_numeric(df['Intensity'], errors='coerce')
df['Angle'] = pd.to_numeric(df['Angle'], errors='coerce')

# Get unique values from 'Type' (FoV)
FOV_list = df['Type'].unique()

# Initialize list to store the results
fwhm_results = []

# Toggle for raw or normalized data
use_normalized_data = True  # Change to False for raw data

# Define line styles and colorplate
line_styles = ['-', '--', '-.', ':', (0, (3, 5, 1, 5)),  
               (0, (1, 1)), (0, (5, 10)), (0, (3, 1, 1, 1)), (0, (1, 5))]  

high_contrast_colors = [
    'black', 'red', 'blue', 'green', 
    'orange', 'purple', 'cyan', 'magenta', 
    'brown', 'pink'
]

# Loop through each FoV
for FOV in FOV_list:
    fov_data = df[df['Type'] == FOV]
    
    # Initialize a new figure for each FoV
    plt.figure(figsize=(10, 5))
    
    run_ids = fov_data['Run ID'].unique()  # Get unique Run IDs
    for i in range(len(run_ids)):
        rID = run_ids[i]
        run_data = fov_data[fov_data['Run ID'] == rID]
        
        # Get the angles and intensities for this run
        angles = run_data['Angle'].values
        intensities = run_data['Intensity'].values
        
        # Normalize intensities if needed
        if use_normalized_data:
            max_intensity = np.max(intensities)
            if max_intensity > 0:
                intensities = intensities / max_intensity  # Normalize to maximum
        
        # Calculate FWHM
        fwhm_min_angle, fwhm_max_angle, fwhm_bandwidth, half_max = calculate_fwhm(angles, intensities)

        fwhm_results.append([FOV, rID, fwhm_min_angle, fwhm_max_angle, fwhm_bandwidth])
        
        # Plotting the intensity data for each rID with different line styles and colors
        plt.plot(angles, intensities, linestyle=line_styles[i % len(line_styles)],
                 color=high_contrast_colors[i % len(high_contrast_colors)], label=f'{rID}')
        
        # Draw the half-max line without adding it to the legend
        plt.axhline(y=half_max, color='grey', linestyle=':', label='_nolegend_')
        

    # Customize the plot for each FoV
    plt.title(f'{FOV}')
    plt.xlabel('Angle (\u00b0)')
    plt.ylabel('Normalized PS Counts' if use_normalized_data else 'PS Counts')
    
    # Set x and y limits
    plt.xlim(-90, 90)  # X-axis limits
    plt.ylim(0)  # Y-axis limits based on intensity

    # Set x-ticks in increments of 10 degrees
    plt.xticks(np.arange(-90, 91, 10))

    plt.legend()
    plt.grid(True)
    plt.show()

# Output the FWHM table
print("Field of View, Run ID, FWHM (Left Bound), FWHM (Right Bound), FWHM")
for result in fwhm_results:
    print(f"{result[0]}, {result[1]}, {result[2]:.2f}, {result[3]:.2f}, {result[4]:.2f}")

# Correct typos using pandas
# Example: suppose there are typos in 'Type' like 'FoV1', 'FoV2', that should be 'FoV 1', 'FoV 2'
typo_corrections = {
    'FoV1': 'FoV 1',
    'FoV2': 'FoV 2'
}
df['Type'] = df['Type'].replace(typo_corrections)
