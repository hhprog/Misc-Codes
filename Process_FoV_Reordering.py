# ... [previous code remains unchanged] ...

# Define the desired order of Run IDs
desired_order = ['Run 1', 'Run 2', 'Run 3']  # Replace with your actual Run IDs in the desired order

# Loop through each FoV
for FOV in FOV_list:
    fov_data = df[df['Type'] == FOV]

    # Initialize a new figure for each FoV
    plt.figure(figsize=(10, 5))

    # Get unique Run IDs and sort them based on the desired order
    run_ids = fov_data['Run ID'].unique()
    ordered_run_ids = [run_id for run_id in desired_order if run_id in run_ids]

    for i, rID in enumerate(ordered_run_ids):
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

# ... [remaining code for printing FWHM results and correcting typos] ...
