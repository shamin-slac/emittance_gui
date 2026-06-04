import matplotlib.pyplot as plt
import numpy as np

from slac_measurements.emittance_measurement import QuadScanEmittanceResult

def plot_quad_scan_result(emittance_result: QuadScanEmittanceResult):
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

    fig, ax = plt.subplots(1, 3)
    # fig.set_size_inches(3, 5)

    c = ["x", "y"]
    for i in range(2):
        sorted_indices = np.argsort(emittance_result.quadrupole_pv_values[i])
        k = emittance_result.quadrupole_pv_values[i][sorted_indices]
        beta = emittance_result.twiss[i][sorted_indices][:, 0]
        epsilon = emittance_result.geometric_emittance[i]

        ax[0].plot(
            k,
            emittance_result.rms_beamsizes[i][sorted_indices],
            "+",
            label=f"rms_{c[i]}",
        )

        # plot fit from twiss at screen calculation
        ax[0].plot(
            k,
            np.sqrt(epsilon * beta) * 1e3,
            "--",
            label=f"{c[i]}_fit",
        )

        psi_list = np.deg2rad(emittance_result.phase_advances[i])
        # plot normalized phase space circle
        phi = np.linspace(0, 2*np.pi, 400)
        R = np.sqrt(epsilon)
        X_c = R * np.cos(phi)
        Xp_c = -R * np.sin(phi)
        ax[i+1].plot(X_c, Xp_c, 'k-', lw=1.5)

        # Lock the limits so phase advance lines can properly rescale
        lim = 1.4 * R
        ax[i+1].set_xlim(-lim, lim)
        ax[i+1].set_ylim(-lim, lim)
        xlim, ylim = ax[i+1].get_xlim(), ax[i+1].get_ylim()

        def ray_to_edge(dx, dy, xlim, ylim):
            cands = []
            if dx > 0: cands.append(xlim[1]/dx)
            if dx < 0: cands.append(xlim[0]/dx)
            if dy > 0: cands.append(ylim[1]/dy)
            if dy < 0: cands.append(ylim[0]/dy)
            t = min(cands)
            return dx*t, dy*t
        
        cmap = plt.cm.viridis
        for j, psi in enumerate(psi_list):
            color = cmap(j / max(1, len(psi_list)-1))

            # Point on the circle at phase psi
            Xr  =  R * np.cos(psi)
            Xpr = -R * np.sin(psi)

            # Ray extended to the edge
            xe, ye = ray_to_edge(Xr, Xpr, xlim, ylim)
            ax[i+1].plot([0, xe], [0, ye], '-', color=color, lw=1.2, alpha=0.8)

            # Dot on the circle
            ax[i+1].plot(Xr, Xpr, 'o', color=color)

            # Label at edge
            ha = 'left'   if xe < 0 else 'right' if xe > 0 else 'center'
            va = 'bottom' if ye < 0 else 'top'   if ye > 0 else 'center'
            pad_x = 0.02*(xlim[1]-xlim[0]) * (-1 if xe>0 else 1 if xe<0 else 0)
            pad_y = 0.02*(ylim[1]-ylim[0]) * (-1 if ye>0 else 1 if ye<0 else 0)
            ax[i+1].text(xe + pad_x, ye + pad_y,
                    fr"$\psi={np.rad2deg(psi):.0f}^\circ$",
                    color=color, ha=ha, va=va, fontsize=10,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

        ax[i+1].axhline(0, color='gray', lw=0.5)
        ax[i+1].axvline(0, color='gray', lw=0.5)
        ax[i+1].set_aspect('equal')
        ax[i+1].set_title(f"{c[i]}-plane Normalized Phase Space")

    ax[0].set_xlabel("Quadrupole Strength [T/m]")
    ax[0].set_ylabel("Beam size [um]")
    ax[0].set_title("Beam size plot")
    ax[0].legend()

    for ele in ax:
        ele.grid(True, alpha=0.3)

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

    fig, ax = plt.subplots(1, 3)
    # fig.set_size_inches(4, 6)

    c = ["x", "y"]
    for i in range(2):
        beam_profile_devices_z = np.array(emittance_result.beam_profile_devices_z)
        sorted_indices = np.argsort(beam_profile_devices_z)
        z = beam_profile_devices_z[sorted_indices]

        beta = emittance_result.twiss[i][sorted_indices][:, 0]
        epsilon = emittance_result.geometric_emittance[i]

        ax[0].plot(
            z,
            emittance_result.rms_beamsizes[i][sorted_indices],
            "+",
            label=f"rms_{c[i]}",
        )

        # plot fit from twiss at screen calculation
        ax[0].plot(
            z,
            np.sqrt(epsilon * beta) * 1e3,
            "--",
            label=f"{c[i]}_fit",
        )

        psi_list = np.deg2rad(emittance_result.phase_advances[i])
        # plot normalized phase space circle
        phi = np.linspace(0, 2*np.pi, 400)
        R = np.sqrt(epsilon)
        X_c = R * np.cos(phi)
        Xp_c = -R * np.sin(phi)
        ax[i+1].plot(X_c, Xp_c, 'k-', lw=1.5)

        # Lock the limits so phase advance lines can properly rescale
        lim = 1.4 * R
        ax[i+1].set_xlim(-lim, lim)
        ax[i+1].set_ylim(-lim, lim)
        xlim, ylim = ax[i+1].get_xlim(), ax[i+1].get_ylim()

        def ray_to_edge(dx, dy, xlim, ylim):
            cands = []
            if dx > 0: cands.append(xlim[1]/dx)
            if dx < 0: cands.append(xlim[0]/dx)
            if dy > 0: cands.append(ylim[1]/dy)
            if dy < 0: cands.append(ylim[0]/dy)
            t = min(cands)
            return dx*t, dy*t
        
        cmap = plt.cm.viridis
        for j, psi in enumerate(psi_list):
            color = cmap(j / max(1, len(psi_list)-1))

            # Point on the circle at phase psi
            Xr  =  R * np.cos(psi)
            Xpr = -R * np.sin(psi)

            # Ray extended to the edge
            xe, ye = ray_to_edge(Xr, Xpr, xlim, ylim)
            ax[i+1].plot([0, xe], [0, ye], '-', color=color, lw=1.2, alpha=0.8)

            # Dot on the circle
            ax[i+1].plot(Xr, Xpr, 'o', color=color)

            # Label at edge
            ha = 'left'   if xe < 0 else 'right' if xe > 0 else 'center'
            va = 'bottom' if ye < 0 else 'top'   if ye > 0 else 'center'
            pad_x = 0.02*(xlim[1]-xlim[0]) * (-1 if xe>0 else 1 if xe<0 else 0)
            pad_y = 0.02*(ylim[1]-ylim[0]) * (-1 if ye>0 else 1 if ye<0 else 0)
            ax[i+1].text(xe + pad_x, ye + pad_y,
                    fr"$\psi={np.rad2deg(psi):.0f}^\circ$",
                    color=color, ha=ha, va=va, fontsize=10,
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

        ax[i+1].axhline(0, color='gray', lw=0.5)
        ax[i+1].axvline(0, color='gray', lw=0.5)
        ax[i+1].set_aspect('equal')
        ax[i+1].set_title(f"{c[i]}-plane Normalized Phase Space")

    ax[0].set_xlabel("z [m]")
    ax[0].set_ylabel("Beam size [um]")
    ax[0].set_title("Beam size plot")
    ax[0].legend()

    for ele in ax:
        ele.grid(True, alpha=0.3)

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