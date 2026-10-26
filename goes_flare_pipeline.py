import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GOESFlareKinematicsEngine:
    """
    Advanced Space Weather Pipeline designed to parse multi-channel GOES X-ray 
    flux data, compute energetic derivatives, and automate solar flare event classification.
    """
    def __init__(self, time_steps: int = 1440):
        self.time_steps = time_steps
        self.time_array = None
        self.short_flux = None  # 0.5 - 4.0 Angstrom channel
        self.long_flux = None   # 1.0 - 8.0 Angstrom channel (Primary classification band)
        
    def generate_synthetic_goes_stream(self):
        """
        Simulates raw 1-minute resolution GOES-16 X-ray sensor time-series data streams,
        modeling background solar minimum irradiance coupled with transient eruptive events.
        """
        np.random.seed(88)
        self.time_array = np.linspace(0, 24, self.time_steps)  # 24-hour observation window
        
        # Base solar background irradiance level (A/B class background noise)
        base_noise = 1e-8 + np.random.normal(0, 2e-9, self.time_steps)
        self.long_flux = np.clip(base_noise, 1e-9, None)
        
        # Inject structural flare events using standard asymmetrical flare profiles
        # Flare 1: Moderate M-class eruption at Hour 6
        t1, peak1, duration1 = 6.0, 3.5e-5, 0.4
        flare1 = peak1 * np.exp(-((self.time_array - t1) / duration1)**2) * (self.time_array >= t1 - 0.1)
        
        # Flare 2: Massive X-class extreme space weather event at Hour 14
        t2, peak2, duration2 = 14.0, 2.8e-4, 0.8
        flare2 = peak2 * np.exp(-((self.time_array - t2) / duration2)**2) * (self.time_array >= t2 - 0.1)
        
        # Flare 3: Minor C-class thermal event at Hour 20
        t3, peak3, duration3 = 20.0, 6.2e-6, 0.3
        flare3 = peak3 * np.exp(-((self.time_array - t3) / duration3)**2) * (self.time_array >= t3 - 0.05)
        
        # Aggregate fluxes and simulate the secondary short-wavelength channel response
        self.long_flux += flare1 + flare2 + flare3
        self.short_flux = self.long_flux * 0.15 + np.random.normal(0, 1e-9, self.time_steps)
        
        print("[STATUS] Ingested 1440 continuous epochs of multi-channel satellite X-ray streams.")

    def compute_flux_kinematics(self):
        """
        Applies discrete numerical calculus (central finite difference) to evaluate 
        the derivative of the long-channel flux vector, mapping ionization growth rates (dF/dt).
        """
        dt = 24.0 / self.time_steps  # Time delta in hours
        df_dt = np.gradient(self.long_flux, dt)
        return df_dt

    def run_automated_event_classifier(self):
        """
        Processes the raw X-ray timeseries to isolate peak amplitudes, classifies them 
        using formal NOAA Space Weather scales, and prints an operational physics report.
        """
        df_dt = self.compute_flux_kinematics()
        
        # Isolate indices where ionization growth rate spikes sharply (flare onset detection threshold)
        threshold = 5e-5
        peaks = []
        
        # Simple window peak finder based on derivative changes
        for i in range(1, len(df_dt) - 1):
            if df_dt[i] > df_dt[i-1] and df_dt[i] > df_dt[i+1] and df_dt[i] > threshold:
                # Find maximum flux index in the immediate neighborhood of the derivative spike
                neighborhood = self.long_flux[i:i+40]
                if len(neighborhood) > 0:
                    max_idx = i + np.argmax(neighborhood)
                    if max_idx not in peaks:
                        peaks.append(max_idx)

        print("\n" + "="*50)
        print("          AUTOMATED GOES SOLAR FLARE REPORT        ")
        print("="*50)
        
        for p_idx in peaks:
            peak_time = self.time_array[p_idx]
            peak_val = self.long_flux[p_idx]
            
            # Astrophysical classification logic
            if peak_val >= 1e-4:
                flare_class = f"X{(peak_val / 1e-4):.1f}"
            elif peak_val >= 1e-5:
                flare_class = f"M{(peak_val / 1e-5):.1f}"
            elif peak_val >= 1e-6:
                flare_class = f"C{(peak_val / 1e-6):.1f}"
            else:
                flare_class = f"B{(peak_val / 1e-7):.1f}"
                
            print(f"Timestamp: {peak_time:.2f} Hours | Peak Flux: {peak_val:.2e} W/m² | Classification: {flare_class}")
        print("="*50 + "\n")

    def render_publication_plots(self):
        """Generates high-resolution multi-panel plots matching professional space weather standards."""
        df_dt = self.compute_flux_kinematics()
        
        fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        
        # Top Panel: Irradiance Light Curves (Logarithmic Scale)
        axes[0].plot(self.time_array, self.long_flux, color='darkorange', linewidth=2, label=r'GOES Long Channel ($1.0 - 8.0$ Å)')
        axes[0].plot(self.time_array, self.short_flux, color='navy', linewidth=1, alpha=0.7, label=r'GOES Short Channel ($0.5 - 4.0$ Å)')
        axes[0].set_yscale('log')
        axes[0].set_ylim(1e-9, 1e-3)
        axes[0].set_ylabel(r'X-ray Flux ($W \cdot m^{-2}$)', fontsize=11)
        axes[0].set_title("NOAA GOES Satellite X-ray Solar Flare Irradiance Streams", fontsize=12, fontweight='bold')
        
        # Draw physical classification boundary regions
        axes[0].axhspan(1e-4, 1e-3, color='red', alpha=0.08, label='X-Class Threshold')
        axes[0].axhspan(1e-5, 1e-4, color='orange', alpha=0.08, label='M-Class Threshold')
        axes[0].axhspan(1e-6, 1e-5, color='yellow', alpha=0.08, label='C-Class Threshold')
        axes[0].legend(loc='lower left', frameon=True)
        axes[0].grid(True, which="both", linestyle=':', alpha=0.5)
        
        # Bottom Panel: Numerical Derivative Vector (Kinetic Growth Rate)
        axes[1].plot(self.time_array, df_dt, color='crimson', linewidth=1.5, label='Ionization Growth Rate (dF/dt)')
        axes[1].set_ylabel(r'Flux Derivative ($W \cdot m^{-2} \cdot hr^{-1}$)', fontsize=11)
        axes[1].set_xlabel('Observation Timestamp (Hours from Epoch)', fontsize=11)
        axes[1].set_title("Energetic Kinematics: First-Order Flux Variations", fontsize=12, fontweight='bold')
        axes[1].legend(loc='upper right')
        axes[1].grid(True, linestyle=':', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig('goes_flux_kinematics_analysis.png', dpi=300)
        plt.show()

if __name__ == "__main__":
    engine = GOESFlareKinematicsEngine(time_steps=1440)
    engine.generate_synthetic_goes_stream()
    engine.run_automated_event_classifier()
    engine.render_publication_plots()
