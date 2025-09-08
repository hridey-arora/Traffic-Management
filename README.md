# 🚦 Smart Traffic Management System  

## 📌 Overview  
This project is a **prototype for an adaptive traffic management system** designed to reduce urban congestion, improve emergency response, and ensure pedestrian safety.  
It uses **simulated traffic data** (random vehicle counts) but is built to integrate with **Computer Vision (CV)** or IoT sensors for real-world deployment.  

The system ensures:  
- Smarter traffic light cycles (based on congestion & time of day)  
- Priority for **emergency vehicles** 🚑  
- Safe pedestrian crossings 🚶  
- Fairness so no lane is starved for too long  
- Practical safeguards against misuse  

---

## ✨ Features  

- ✅ **Adaptive Signal Control** – only the most congested lane gets green, others stay red  
- ✅ **Fairness Mechanism** – no lane waits longer than a max time  
- ✅ **Smart Scheduling** – adjusts lane priorities based on **time of day**  
- ✅ **Pedestrian Crossing System** – safe crossing with 30s wait + 15s red light window  
- ✅ **Emergency Vehicle Priority** – instantly clears a path for ambulances/fire trucks  
- ✅ **Real-Time Dashboard** – web-based UI with:  
  - Vehicle counts per lane  
  - Active green lane indicator  
  - Countdown timer ⏱  
  - Emergency status 🚑  
  - Pedestrian request status 🚶  
- ✅ **Prototype-friendly** – random traffic generator (every 7s), ready to swap with live CV  

---

## 🖥 Tech Stack  

- **Backend:** Python (Flask + Flask-CORS)  
- **Frontend:** HTML, CSS, Vanilla JS  
- **Simulation:** Randomized traffic counts (7s refresh)  
- **Future Integration:** OpenCV / IoT sensors, Twilio (for SMS alerts), AQI sensors

---

## ⚙️ Setup Instructions  

1. Clone the repo:  
   ```bash
   git clone https://github.com/your-username/smart-traffic.git
   cd smart-traffic
