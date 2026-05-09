# Financial Risk Modeling System

An Object-Oriented Financial Risk Engine built in Python. This system was developed as a research-level project for STA 2208 to simulate extreme market volatility across a diversified portfolio using advanced system design and statistical analysis principles.

## System Architecture & Features
This project evolved through 6 major development milestones, scaling from basic procedural scripts to a robust quantitative framework:

* **Object-Oriented Design (OOP):** Utilizes the Strategy Pattern to decouple risk calculation logic (`VolatilityRiskStrategy`, `DefensiveRiskStrategy`) from the `Asset` data models.
* **Functional Data Pipelines:** Employs higher-order functions (`filter`, `map`) and generator functions (`yield`) to efficiently isolate high-risk assets dynamically.
* **Concurrency (Multithreading):** Uses `concurrent.futures.ThreadPoolExecutor` to execute parallel network I/O requests, reducing 20-asset API ingestion latency to sub-second execution times.
* **Machine Learning Integration (AI):** Replaces static deterministic logic with `scikit-learn`'s K-Means clustering algorithm. This autonomously groups assets into Low, Medium, and High-risk tranches based on multidimensional feature spaces (historical volatility and expected returns).
* **Data Visualization:** Renders professional portfolio impact charts and AI risk cluster scatterplots using `matplotlib`.

## Technology Stack
* **Language:** Python 3.x
* **Core Libraries:** `pandas`, `numpy`, `yfinance`
* **Advanced Libraries:** `scikit-learn` (Machine Learning), `matplotlib` (Visualization)

## How to Run the System Locally
To clone and run this simulation on your local machine, run the following commands in your terminal:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/maloba9-droid/Financial-Risk-Modeling-System.git](https://github.com/maloba9-droid/Financial-Risk-Modeling-System.git)
   cd Financial-Risk-Modeling-System
2. Install the required dependencies:
   ```bash
   python -m pip install pandas numpy yfinance matplotlib scikit-learn
3. Execute the simulation engine:
   ```bash
   python main.py