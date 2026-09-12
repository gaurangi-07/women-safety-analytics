# Women Safety Analytics

> **Academic Prototype** – This project is built for educational and demonstration purposes.  
> It identifies potential safety-risk patterns using computer vision.  
> **It does not determine that a crime has occurred.**  
> Human verification is required for any real-world intervention.

---

## 1. Project Title

**Women Safety Analytics** — An AI-powered terminal-based women safety monitoring system.

---

## 2. Problem Statement

Based on the **BEL (Bharat Electronics Limited) Problem Statement** for smart city safety systems:

> Design an AI-based system that can analyse CCTV footage in real-time to detect potential safety risks involving women, such as lone women at night, women surrounded by groups of men, and distress signals, and generate automated alerts for security personnel.

---

## 3. Project Objective

To build a **terminal-based Python application** that:
- Detects people in video feeds and images using computer vision
- Estimates gender distribution in a scene
- Identifies potential safety risk patterns (rule-based)
- Generates and stores safety alerts in a local database
- Provides analytics and reports for safety monitoring

---

## 4. Features

| Feature | Description | Status |
|---|---|---|
| Person Detection | Detects people in video/image using YOLOv8 | ✅ Implemented |
| Gender Classification | Estimates gender of each detected person | ✅ Implemented |
| Gender Statistics | View total male/female counts across sessions | ✅ Implemented |
| Lone Woman at Night | Detects isolated female during night hours | ✅ Implemented |
| Woman Surrounded by Men | Detects female surrounded by ≥3 males | ✅ Implemented |
| SOS Gesture Detection | Detects open-palm raised hand distress gesture | ✅ Implemented (Prototype) |
| Safety Alerts | Stores and displays safety alerts from SQLite | ✅ Implemented |
| Hotspot Analysis | Groups alerts by camera/location | ✅ Implemented |
| Report Generation | Exports a plain-text safety summary report | ✅ Implemented |
| Live Camera | Real-time processing from webcam | ✅ Implemented |
| Rich Terminal UI | Coloured tables, panels, progress indicators | ✅ Implemented |

---

## 5. Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Person Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV (`opencv-python`) |
| Gesture Detection | MediaPipe |
| Data Processing | NumPy |
| Terminal UI | Rich |
| Database | SQLite3 (built-in Python library) |

---

## 6. System Architecture

```
                  ┌──────────────────────────────┐
                  │        main.py (CLI)          │
                  │  Rich terminal interface      │
                  └────────────┬─────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
   ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐
   │  detection/  │   │  analytics/  │   │    reports/      │
   │  - YOLO      │   │  - Threats   │   │  - Report Gen    │
   │  - Gender    │   │  - Hotspots  │   └──────────────────┘
   │  - Gesture   │   └──────┬───────┘
   └──────┬───────┘          │
          │                  ▼
          └──────────► alerts/alert_manager.py
                             │
                             ▼
                    ┌────────────────┐
                    │  database/     │
                    │  SQLite DB     │
                    └────────────────┘
```

---

## 7. Project Folder Structure

```
women_safety_analytics/
│
├── main.py                      # Entry point, CLI menu
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── TESTING.md                   # Test cases
├── .gitignore
│
├── detection/                   # Detection modules
│   ├── __init__.py
│   ├── person_detector.py       # YOLOv8 person detection + integration
│   ├── gender_classifier.py     # Rule-based gender estimation
│   └── gesture_detector.py      # SOS gesture detection (MediaPipe)
│
├── analytics/                   # Analytics modules
│   ├── __init__.py
│   ├── threat_detection.py      # Lone woman / surrounded by men rules
│   └── hotspot_analysis.py      # Group alerts by location
│
├── alerts/                      # Alert system
│   ├── __init__.py
│   └── alert_manager.py         # SafetyAlert class + SQLite logging
│
├── database/                    # Database layer
│   ├── __init__.py
│   └── database.py              # SQLite schema + CRUD functions
│
├── reports/                     # Report generation
│   ├── __init__.py
│   └── report_generator.py      # Generates safety_report.txt
│
├── data/                        # Data directory
│   ├── women_safety.db          # SQLite database (auto-created)
│   └── reports/
│       └── safety_report.txt    # Generated report (auto-created)
│
└── models/                      # AI model weights
    └── yolov8n.pt               # Downloaded automatically on first run
```

---

## 8. Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- A terminal / command prompt

### Steps

**1. Clone the repository:**
```bash
git clone https://github.com/gaurangi-07/women-safety-analytics.git
cd women-safety-analytics
```

**2. (Recommended) Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

> **Note:** On first run, YOLOv8 will automatically download the `yolov8n.pt` model weights (~6 MB). An internet connection is required for the first run only.

---

## 9. How to Run

```bash
python3 main.py
```

You will see the main menu:

```
╭──────────────────────────────────╮
│   WOMEN SAFETY ANALYTICS         │
│   AI Safety Monitoring System    │
╰──────────────────────────────────╯

  1. Analyze Video
  2. Analyze Image
  3. Live Camera
  4. View Safety Alerts
  5. Gender Statistics
  6. Hotspot Analysis
  7. Generate Report
  8. Exit

Enter your choice (1-8):
```

---

## 10. How to Use Each Menu Option

| Option | What it does | Input required |
|---|---|---|
| **1. Analyze Video** | Processes a video file frame-by-frame, detects people, estimates gender, checks for threats | Path to `.mp4` / `.avi` video file |
| **2. Analyze Image** | Processes a single image, detects people, estimates gender | Path to `.jpg` / `.png` image file |
| **3. Live Camera** | Uses webcam for real-time detection | No input (press `q` in window to stop) |
| **4. View Safety Alerts** | Shows all recorded alerts from the database | Enter an alert ID for details |
| **5. Gender Statistics** | Shows total gender counts and latest scene stats | None |
| **6. Hotspot Analysis** | Shows alert counts grouped by camera/location | None |
| **7. Generate Report** | Creates `data/reports/safety_report.txt` | None |
| **8. Exit** | Exits the application | None |

---

## 11. AI Models and Libraries Used

### YOLOv8 (Ultralytics)
- **What it does:** Detects people (and other objects) in images and video frames.
- **Model used:** `yolov8n.pt` (nano model — lightweight and fast)
- **Class used:** COCO class index `0` = `person`

### MediaPipe (Google)
- **What it does:** Detects hand landmarks in real-time
- **Used for:** SOS gesture detection — checks if all finger tips are raised above the wrist

### Gender Classification
- **Note:** This is a **rule-based heuristic** using aspect ratio and HSV colour metrics on cropped person images.
- It is **not** a trained deep learning gender classification model.
- Accuracy is limited and intended for demonstration purposes only.

---

## 12. Database Structure

The application uses **SQLite** with one database file: `data/women_safety.db`

### Table: `alerts`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| alert_type | TEXT | e.g., "Lone Woman at Night" |
| severity | TEXT | HIGH / MEDIUM / LOW |
| timestamp | TEXT | Date and time of alert |
| location | TEXT | Camera/source identifier |
| male_count | INTEGER | Males detected in scene |
| female_count | INTEGER | Females detected in scene |
| description | TEXT | Risk description |

### Table: `gender_stats`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| timestamp | TEXT | Date and time of analysis |
| source_name | TEXT | Video/image filename |
| male_count | INTEGER | Males detected |
| female_count | INTEGER | Females detected |
| total_count | INTEGER | Total people detected |

---

## 13. Safety Detection Logic

### Rule 1: Lone Woman at Night
- **Trigger:** A female is detected who has **no other person within 250 pixels**, **during night hours (8 PM – 6 AM)**
- **Condition persists for:** 3 consecutive frames
- **Severity:** MEDIUM

### Rule 2: Woman Surrounded by Men
- **Trigger:** A female has **3 or more males within 250 pixels** of her bounding box centre
- **Condition persists for:** 3 consecutive frames
- **Severity:** HIGH

### Rule 3: SOS Gesture (Prototype)
- **Trigger:** All 4 finger tips (index, middle, ring, pinky) are **above the wrist** in MediaPipe hand landmarks (raised open palm)
- **Condition persists for:** 3 consecutive frames
- **Severity:** HIGH

> All detections are **probabilistic estimates**. Distance is measured in pixels (screen space), not real-world distance.

---

## 14. Limitations

1. **Gender classification is a heuristic** — not a trained ML model. Accuracy is limited.
2. **Pixel-based distance** does not represent real-world distance. Camera angle affects results.
3. **Night detection uses system clock** — if the camera has a different timezone, this may be inaccurate.
4. **SOS gesture is simplified** — only an open raised palm is detected. More complex gestures require training data.
5. **No camera calibration** — the system does not account for camera position, zoom, or lens distortion.
6. **No multi-camera support** — each analysis session is independent.
7. **Gender binary** — the system only classifies Male/Female, which is a simplification.

---

## 15. Future Improvements

| Priority | Improvement |
|---|---|
| High | Replace heuristic gender classifier with a trained deep learning model |
| High | Add real-time multi-camera support |
| Medium | Integrate SMS/email alerts for HIGH severity events |
| Medium | Add a proper SOS gesture recognition model trained on gesture datasets |
| Medium | Add night-vision / low-light image enhancement |
| Low | Add a web dashboard for remote monitoring |
| Low | Add face anonymisation (privacy protection) |
| Low | Support multiple video streams simultaneously |

---

## Disclaimer

> This is an **academic prototype** developed for a second-year Computer Science project.  
> The system detects **potential safety-risk patterns** — it does **not** determine that a crime has occurred.  
> All detections are probabilistic and may produce false positives.  
> **Human verification is required** before any real-world intervention.  
> The system should **not** be used as a sole basis for law enforcement action.
