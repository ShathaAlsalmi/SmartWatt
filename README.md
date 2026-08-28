# ⚡ SmartWatt: Energy Forecast & Analytics

> An intelligent, machine learning-powered web application designed to forecast daily and monthly household energy consumption and provide actionable AI-driven recommendations for energy efficiency.

## 🌟 Features

*   **🔮 Accurate Predictions:** Utilizes a trained XGBoost machine learning model to predict energy loads based on real historical consumption data.
*   **📊 Interactive Dashboard:** A sleek, modern, and fully responsive frontend featuring dynamic charts (powered by Chart.js) to visualize energy trends.
*   **💡 Smart AI Recommendations:** Automatically analyzes the forecasted load and provides customized energy-saving tips based on usage levels.
*   **📄 PDF Report Generation:** Users can seamlessly download their energy forecast plans and recommendations as beautifully styled PDF reports.
*   **⚡ High-Performance Backend:** Built with FastAPI for lightning-fast, asynchronous API responses.

## 🛠️ Tech Stack

**Frontend:**
*   HTML5, CSS3, Vanilla JavaScript
*   [Chart.js](https://www.chartjs.org/) (Data Visualization)
*   [html2pdf.js](https://ekoopmans.github.io/html2pdf.js/) (PDF Generation)

**Backend & Machine Learning:**
*   Python 3.x
*   [FastAPI](https://fastapi.tiangolo.com/) & Uvicorn (Server)
*   [XGBoost](https://xgboost.readthedocs.io/) (Predictive Modeling)
*   Pandas & NumPy (Data Processing)
*   Joblib (Model serialization)

## 🚀 Getting Started

Follow these steps to run the SmartWatt project locally on your machine.

### Prerequisites
*   Python 3.8+ installed.
*   The trained ML models (`daily_xgb_model.joblib`, `monthly_xgb_model.joblib`) placed in the `models/` directory.
*   The historical dataset (`household_load_start_end (1).csv`) placed in the root directory.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/SmartWatt.git](https://github.com/YourUsername/SmartWatt.git)
    cd SmartWatt
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the FastAPI backend server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

4.  **Launch the Frontend:**
    *   Simply open the `index.html` file in your preferred web browser.
    *   *Alternatively*, serve it via a local Python HTTP server: `python -m http.server 3000` and visit `http://localhost:3000`.

## 🔌 API Endpoints

The backend provides the following RESTful endpoints:

*   **`POST /api/v1/predict/daily`**
    *   **Payload:** `{"target_date": "YYYY-MM-DD"}`
    *   **Returns:** Predicted load (kWh) and estimated cost (SAR) for the specified day.

*   **`POST /api/v1/predict/monthly`**
    *   **Payload:** `{"target_month": "YYYY-MM"}`
    *   **Returns:** Predicted load (kWh) and estimated cost (SAR) for the specified month.

## 👨‍💻 Author
**Shatha Alsalmi** 

---
*Built with ❤️ for a sustainable future.*
