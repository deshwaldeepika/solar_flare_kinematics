# solar_flare_kinematics

## Project 2: GOES Satellite X-Ray Flux Kinematics Engine & Automated Flare Classifier

### 1. Project Overview & Objective
Solar flares are massive explosions in the sun's atmosphere caused by magnetic reconnection. These events release intense streams of radiation across space. The soft X-ray spectrum (0.5 to 8.0 Å) is the industry standard baseline for tracking space weather because these specific high-energy photons ionize Earth's upper atmosphere, causing radio blackouts and satellite disruptions.

This project is an automated data processing pipeline that models telemetry from NOAA's GOES-16 and GOES-18 satellites. Instead of logging events by eye, this pipeline ingests multi-channel X-ray streams, filters out background sensor noise, calculates the velocity of the flare's growth, and automatically logs the event category (C, M, or X-class).

---

### 2. Pipeline Architecture
The pipeline is built using Object-Oriented Programming (OOP) in Python and leverages fast, vectorized matrix math rather than slow loops.

The data flows through four clean stages:
`[Raw Data Ingestion] ──> [Logarithmic Scaling] ──> [Finite-Difference Gradient Engine] ──> [Threshold Windowing] ──> [Automated Alert Logs]`

*   **Data Ingestion:** Simulates dual-channel data streams from GOES silicon photodiodes at a 1-minute cadence (1,440 readings per day). 
    *   *Short Channel (0.5 to 4.0 Å):* Tracks high-energy thermal bursts.
    *   *Long Channel (1.0 to 8.0 Å):* The primary stream used to calculate flare sizes.
*   **Kinematic Engine:** Applies numerical calculus via a central finite-difference gradient to find the first derivative (dF/dt). This isolates the exact speed of the flare's energy growth.
*   **Event Classifier:** Checks if the growth rate spikes past the threshold (dF/dt >= 5e-5 W/m²/hr). When triggered, it scans the immediate time window, grabs the absolute peak flux, and outputs a space weather alert.

---

### 3. Core Math & Logic

#### Central Finite-Difference Derivative
To find the exact moment a flare explodes without causing an artificial time lag, the engine calculates a centered gradient step across the continuous flux array (F). Instead of a simple forward difference which causes a structural delay, the derivative at any discrete time index `i` is derived from its immediate neighbors:

`dF/dt = (F[i+1] - F[i-1]) / (2 * dt)`

*   **Why this matters:** Simple forward differences (`(F[i+1] - F[i]) / dt`) push the recorded peak forward in time, creating a false phase lag. This is unacceptable for real-time space weather alerts. The central difference matches the exact alignment of physical transitions.
*   **Boundary Constraints:** At the exact boundaries of the data array where `i = 0` or `i = max`, the engine automatically drops back to a single-sided forward or backward difference step to prevent out-of-bounds indexing errors.
*   **Time Step Calculation:** The historical data stream runs on a 1-minute cadence. To keep the physical unit scaling accurate to standard metrics (Watts per square meter per hour), `dt` is defined explicitly as `1 / 60` or `0.01667` hours.

#### Logarithmic Scaling and Multi-Scale Analysis
Solar background flux values during a solar minimum hover at sub-microscopic thresholds near 10^-8 W/m². Conversely, catastrophic solar storms scale directly past 10^-4 W/m². This creates an immense four-orders-of-magnitude dynamic range that linear charting cannot display simultaneously. 

To visualize both the fine background noise and the massive peak outputs clearly on a single reference layout, the ingestion engine passes raw metrics through a base-10 logarithmic transformation:

`Scaled_Flux = log10(F)`

*   **Linear vs Logarithmic:** On a traditional linear scale, a standard C-class flare would register as a completely flat line pinned to zero when placed next to an extreme X-class eruption. Shifting to `log10` guarantees uniform fractional visibility across the entire data range.
*   **Data Conditioning:** To ensure the mathematical stability of the log engine during high-frequency sensor noise cycles, the code uses `np.clip` to force a strict minimum threshold of 10^-9 W/m², preventing math runtime crashes from negative numbers or zero values.

#### Classification Thresholds & Continuous Suffix Parsing
The system categorizes events by comparing the maximum long-channel flux peak directly against the official NOAA Space Weather Scales:
*   **X-Class (Extreme Storms):** Peak Flux >= 10^-4 W/m²
*   **M-Class (Moderate Disruptions):** 10^-5 <= Peak Flux < 10^-4 W/m²
*   **C-Class (Minor Events):** 10^-6 <= Peak Flux < 10^-5 W/m²
*   **B-Class (Ambient Background):** Peak Flux < 10^-6 W/m²

To calculate the specific numerical intensity value attached to a flare class (turning an abstract flux value into a readable stamp like M3.5 or X2.8), the parser isolates the scale's base magnitude. It extracts the numerical multiplier using a floor logarithmic division strategy:

`Base_Power = 10 ** floor(log10(Peak_Flux))`
`Class_Suffix = Peak_Flux / Base_Power`

For instance, if the engine captures a peak flux value of `0.00028` W/m², the mathematical floor step identifies the core magnitude limit at `10^-4` (the X-class baseline). Dividing the raw peak by this base scale returns a clean multiplier of exactly `2.8`, cataloging the storm automatically as an **X2.8** class solar event.

---

### 4. Output & Verification

When you run the code, the terminal automatically prints out a real-time event log:

```text
==================================================
          AUTOMATED GOES SOLAR FLARE REPORT        
==================================================
Timestamp: 6.00 Hours  | Peak Flux: 3.50e-05 W/m² | Classification: M3.5
Timestamp: 14.01 Hours | Peak Flux: 2.80e-04 W/m² | Classification: X2.8
Timestamp: 20.01 Hours | Peak Flux: 6.20e-06 W/m² | Classification: C6.2
==================================================
```

#### Graph Analysis
The exported visual (`goes_flux_kinematics_analysis.png`) provides immediate analytical proof:
*   **Top Plot:** Shows the raw flux lines tracking perfectly together, proving a shared thermal origin. The color-coded background bands make it instantly obvious when data breaches danger zones.
*   **Bottom Plot:** Shows the dF/dt derivative flattening out background noise while generating sharp, vertical spikes at the exact moment of a flare's onset. The largest spike catches an extreme ionization acceleration near Hour 14.

![GOES Kinematics Output](02_solar_flare_kinematics/goes_flux_kinematics_analysis.png)



