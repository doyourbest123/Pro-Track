# Pro-Track - Ticker Tracker

ProTrack is a project that pulls current and historical financial data from specified stock tickers using the `yfinance` Python library, while providing qualitative AI insights using the Gemini 3.6 flash LLM model.

## Repository Structure

- **`backend/`**: The Python backend application directory.
  - **`app/`**: Contains core Python source files for the API.
    - `main.py`: The entry point for the FastAPI server (manages endpoints and watchlist functions).
  - `key.env`: Local file containing private API keys (Excluded from Git).
  - `requirements.txt`: Python package dependencies (including `yfinance` and `google-genai`).
- **`frontend/`**: The React frontend application directory.
  - **`src/`**: React source code and application logic.
    - **`components/`**: UI components, including `StockChart.jsx` (utilises Recharts to plot data points).
  - `package.json`: Frontend dependencies and scripts.
- **`.gitignore`**: Global rules instructing Git to ignore sensitive files like `key.env` and `node_modules`.
- **`README.md`**: Project documentation and setup instructions.

## Local Development

Follow these steps to set up and run Pro-Track on your local machine. You will need to run the backend and frontend simultaneously in two separate terminal windows.

### 1. Prerequisites
Clone the repository and create a `key.env` file in your `backend/` directory to store your API key safely:
```text
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 2. Backend Setup (FastAPI)
Open a terminal window and navigate to the backend folder:

1. **Navigate to backend:**
   ```bash
   cd backend
   ```
2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows (Command Prompt):
   venv\Scripts\activate
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start the backend development server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   *The backend will now be live and auto-reloading at `http://localhost:8000`.*

### 3. Frontend Setup (React + Vite)
Open a **second terminal window** and navigate to the frontend folder:

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```
2. **Install frontend dependencies:**
   ```bash
   npm install
   ```
3. **Start the React development server:**
   ```bash
   npx vite --force
   ```
   *Vite will compile your UI and provide a local URL (typically `http://localhost:5173`) to view the application in your browser.*

