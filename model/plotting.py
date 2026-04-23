import matplotlib.pyplot as plt
import numpy as np

def plot_quad_scan_result(emittance_result):
    """
    Plot the results of a quad scan emittance measurement.

    Parameters
    ----------
    emittance_results : EmittanceMeasurementResult
        The results of a quad scan emittance measurement.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object.
    ax : numpy.ndarray
        The axis objects.
    """

    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(4, 6)

    c = ["x", "y"]
    for i in range(2):
        sorted_indices = np.argsort(emittance_result.quadrupole_pv_values[i])
        k = emittance_result.quadrupole_pv_values[i][sorted_indices]
        beta = emittance_result.twiss[i][sorted_indices][:, 0]

        ax[0].plot(
            k,
            emittance_result.rms_beamsizes[i][sorted_indices] * 1e6,
            "+",
            label=f"rms_{c[i]}",
        )

        # plot fit from twiss at screen calculation
        ax[0].plot(
            k,
            np.sqrt(beta * emittance_result.emittance[i]) * 1e3,
            "--",
            label=f"{c[i]}_fit",
        )

        if emittance_result.bmag is not None:
            ax[1].plot(
                k, emittance_result.bmag[i][sorted_indices], "+", label=f"bmag {c[i]}"
            )
            ax[1].set_xlabel("Quadrupole Strength [T/m]")
            ax[1].set_ylabel("bmag")
            ax[1].axhline(1.0, color="black", linestyle="--")
        else:
            # add text to the middle of the axis that says "BMAG not available"
            ax[1].text(
                0.5,
                0.5,
                "bmag not available",
                ha="center",
                va="center",
                transform=ax[1].transAxes,
            )

    ax[0].set_xlabel("Quadrupole Strength [T/m]")
    ax[0].set_ylabel("Beam size [um]")

    for ele in ax:
        ele.legend()

    fig.tight_layout()
    return fig, ax

def plot_multi_result(emittance_result):
    """
    Plot the results of a multi device emittance measurement.

    Parameters
    ----------
    emittance_results : EmittanceMeasurementResult
        The results of a multi device emittance measurement.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object.
    ax : numpy.ndarray
        The axis objects.
    """

    fig, ax = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(4, 6)

    c = ["x", "y"]
    for i in range(2):
        sorted_indices = np.argsort(emittance_result.beam_profile_devices_z)
        z = emittance_result.beam_profile_devices_z[sorted_indices]
        beta = emittance_result.twiss[i][sorted_indices][:, 0]

        ax[0].plot(
            z,
            emittance_result.rms_beamsizes[i][sorted_indices] * 1e6,
            "+",
            label=f"rms_{c[i]}",
        )

        # plot fit from twiss at screen calculation
        ax[0].plot(
            z,
            np.sqrt(beta * emittance_result.emittance[i]) * 1e3,
            "--",
            label=f"{c[i]}_fit",
        )

        if emittance_result.bmag is not None:
            ax[1].plot(
                z, emittance_result.bmag[i][sorted_indices], "+", label=f"bmag {c[i]}"
            )
            ax[1].set_xlabel("z [m]")
            ax[1].set_ylabel("bmag")
            ax[1].axhline(1.0, color="black", linestyle="--")
        else:
            # add text to the middle of the axis that says "BMAG not available"
            ax[1].text(
                0.5,
                0.5,
                "bmag not available",
                ha="center",
                va="center",
                transform=ax[1].transAxes,
            )

    ax[0].set_xlabel("z [m]")
    ax[0].set_ylabel("Beam size [um]")

    for ele in ax:
        ele.legend()

    fig.tight_layout()
    return fig, ax

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