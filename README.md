# solar_flare_kinematics
## Project 2: Energetic Space Weather Classification via Finite-Difference Flux Kinematics

### 1. Research Objective & Engineering Scope
Solar eruptive flares release large volumes of hard and soft X-ray radiation, ionizing Earth's upper atmosphere and disrupting satellite operations. This project constructs an automated space weather event identification engine that processes satellite datasets, computes time-varying flux growth metrics, and flags solar flare anomalies without subjective visual logging dependencies.

### 2. Computational Framework & Mathematical Modeling
The numerical pipeline applies a dynamic central-difference derivative modeling approach:
- **Numerical Derivative (Kinetic Growth Velocity):** Localized plasma energetic acceleration profiles are extracted by computing the discrete finite gradient of the X-ray flux vector ($F$):
  $$\frac{dF}{dt} \approx \frac{F_{i+1} - F_{i-1}}{2\Delta t}$$
- **Event Extraction:** The system maps the flux parameters to isolate localized maximum peaks against standard astronomical baseline parameters:
  - **C-Class Events:** $10^{-6} \le F_{\text{peak}} < 10^{-5} \text{ W/m}^2$ (Minor Thermal Transients)
  - **M-Class Events:** $10^{-5} \le F_{\text{peak}} < 10^{-4} \text{ W/m}^2$ (Moderate Space Weather Disruptions)
  - **X-Class Events:** $F_{\text{peak}} \ge 10^{-4} \text{ W/m}^2$ (Extreme Space Weather Anomalies)

### 3. Pipeline Output Analytics
The classification log successfully separates background noise from solar eruptions, registering three specific transient flare peaks, including a major **X2.8** class solar storm anomaly. 

![GOES Kinematics Output](03_solar_flare_kinematics/goes_flux_kinematics_analysis.png)
