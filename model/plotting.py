import matplotlib.pyplot as plt
import numpy as np

def plot_beam_size(scan_values, beam_sizes):
    # Create a list to store the plots
    plots = []
    
    for axis in beam_sizes.keys():
        fig, ax = plt.subplots()
        
        # Plot the original beam size data
        ax.plot(scan_values, beam_sizes[axis], label="Data", marker='o', linestyle="None")

        # Fit a parabolic (second degree polynomial) curve to the data
        p = np.polyfit(scan_values, beam_sizes[axis], 2)
        
        # Generate a smooth range of x values for the fitted curve
        x_smooth = np.linspace(min(scan_values), max(scan_values), 500)  # 500 points for smoothness
        fitted_values = np.polyval(p, x_smooth)

        # Plot the parabolic fit
        ax.plot(x_smooth, fitted_values, label="Parabolic Fit", linestyle="--", color='r')

        # Add labels and legend
        ax.set_xlabel('Scan Values')
        ax.set_ylabel(f'Beam Size - {axis}')
        ax.legend()

        # Store the plot (figure) in a variable
        plots.append(fig)

    return plots

def plot_phase_space(positions, angles):
    #TODO: construct curves
    # Create a plot
    # Use emittance, x_rms and angle_rms and ellipse equation
    fig, ax = plt.subplots()
    ax.plot(positions, angles)

    # Store the plot (figure) in a variable
    phase_space_plot = fig