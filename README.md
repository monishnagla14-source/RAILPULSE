# RailPulse — Train Delay Analytics Dashboard

RailPulse is a beginner-friendly second-year CSE project built with Python, Streamlit, Pandas, NumPy, and Matplotlib. It analyzes an included **sample dataset** of train-day timing records. It does not provide live train status or official railway information.

## Features
- Railway-themed dashboard with KPI cards
- Filters for date range, train, route, and maximum delay
- Average delay, median delay, and on-time percentage calculations
- Train-wise average-delay bar chart
- On-time vs delayed pie chart
- Month-wise delay trend line chart
- Filtered record table and CSV download
- Explanation of the project's calculations

## Folder structure

```text
RailPulse/
├── app.py
├── requirements.txt
├── README.md
└── data/
    └── train_delays.csv
```

## Run on Windows with VS Code

1. Install Python 3.11, 3.12, or 3.13 from the official Python website. During installation, enable **Add Python to PATH** if that option appears.
2. Extract the `RailPulse.zip` file.
3. Open VS Code, choose **File → Open Folder**, and select the extracted `RailPulse` folder.
4. Open **Terminal → New Terminal**.
5. Create a virtual environment:

   ```powershell
   py -3.13 -m venv .venv
   ```

   If Python 3.13 is not installed but another supported Python version is, use `py -3.12 -m venv .venv` or the installed version number.

6. Install dependencies using the virtual environment's Python (this avoids PowerShell activation-policy problems):

   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

7. Start the website:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

8. Streamlit will show a local URL in the terminal, usually `http://localhost:8501`. Open it in your browser.
9. To stop the app, click the terminal and press `Ctrl+C`.

## What each library does

- **Pandas:** reads the CSV into a DataFrame, filters rows, creates delay/route/month columns, groups records by train and month, and prepares the table/download.
- **NumPy:** calculates the mean and median delay and the percentage of records meeting the project's on-time rule.
- **Matplotlib:** renders the train-wise bar chart, punctuality pie chart, and monthly trend line chart.
- **Streamlit:** provides the interactive web UI, filters, metrics, data table, and download button.

## Data and assumptions

- `scheduled_minutes` and `actual_minutes` are illustrative journey-duration values in minutes, not clock timestamps.
- `delay_minutes = max(actual_minutes - scheduled_minutes, 0)` in this simplified demo.
- A record counts as on-time when its calculated delay is 10 minutes or less. This is a project-defined rule, not an official railway standard.
- The included rows are generated sample records intended for learning and demonstration. Do not use them to make actual travel decisions.

## Viva talking points

1. **Problem statement:** Train punctuality data can be difficult to compare across dates and routes. RailPulse summarizes timing records in a visual dashboard.
2. **Input:** A CSV file containing date, train number/name, origin, destination, scheduled duration, actual duration, and distance.
3. **Processing:** Pandas cleans and filters records; NumPy calculates summary statistics; Matplotlib visualizes patterns.
4. **Output:** KPI cards, three charts, a filterable table, and downloadable filtered records.
5. **Limitation:** The demo uses sample data, so it cannot report current delays. Live data would require a verified and permitted data source/API.
