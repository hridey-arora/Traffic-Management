# 🚦 Smart Traffic Management System

## 📌 Overview
This project is a prototype for an adaptive traffic management system designed to reduce urban congestion, improve emergency response, and support pedestrian safety.

It currently uses simulated traffic data with random vehicle counts, and it is structured so the simulation layer can later be replaced with computer-vision or IoT sensor inputs.

The system supports:

- Smarter traffic-light cycles based on congestion and time of day
- Emergency vehicle priority
- Pedestrian crossing requests
- Fairness rules so no lane waits too long
- A real-time browser dashboard

---

## ✨ Features
- ✅ **Adaptive Signal Control**: gives green time to the lane that needs it most.
- ✅ **Fairness Mechanism**: prevents any lane from being starved too long.
- ✅ **Pedestrian Crossing System**: handles crossing requests with wait and crossing windows.
- ✅ **Emergency Vehicle Priority**: clears a selected lane when emergency mode is active.
- ✅ **Real-Time Dashboard**: displays lane counts, green signal state, countdowns, emergency status, and pedestrian state.
- ✅ **Prototype-Friendly Simulation**: random traffic generator refreshes vehicle counts every 7 seconds.

---

## 🖥️ Tech Stack
- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** HTML, CSS, JavaScript
- **Simulation:** Randomized traffic counts
- **Future Integration:** OpenCV, IoT sensors, AQI sensors, SMS alerts

---

## 🗂️ Repository Structure

```text
traffic/
  app.py
  signal_logic.py
  traffic_simulation.py
  static/
README.md
requirements.txt
```

---

## ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/hridey-arora/Traffic-Management.git
cd Traffic-Management
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux, activate it with:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask app:

```bash
cd traffic
python app.py
```

5. Open the local dashboard URL shown in the terminal, usually:

```text
http://127.0.0.1:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serves the dashboard |
| `GET` | `/data` | Returns vehicle counts, signal state, and pedestrian/emergency status |
| `POST` | `/emergency` | Sets emergency priority for lane `0` to `3` |
| `POST` | `/clear_emergency` | Clears emergency priority |
| `POST` | `/pedestrian` | Requests pedestrian crossing |

Example emergency request:

```bash
curl -X POST http://127.0.0.1:5000/emergency ^
  -H "Content-Type: application/json" ^
  -d "{\"lane\": 1}"
```

---

## 🚀 Future Improvements
- Replace random vehicle counts with camera-based detection.
- Add persistent logs for signal decisions and emergency events.
- Add tests for `signal_logic.py` fairness and priority behavior.
- Add deployment instructions for a hosted demo.
- Integrate live IoT sensors for real-world traffic or AQI data.
