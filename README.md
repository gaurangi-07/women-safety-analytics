# Women Safety Analytics

An AI-powered terminal-based women safety monitoring system designed for real-time risk evaluation and emergency alert generation. Based on BEL problem statement specifications.

---

## 📌 Features (Planned & Modular Architecture)

1. **Person Detection**: Identify people in video streams / images using pretrained YOLO models.
2. **Gender Classification**: Classify detected individuals into gender categories.
3. **Gender Distribution & Counting**: Real-time ratio analysis of male and female presence in monitored zones.
4. **Lone Woman at Night Detection**: Identify isolated females present during night hours.
5. **Woman Surrounded by Men Detection**: Spatial density calculation to trigger alerts when a female is surrounded by multiple males.
6. **Basic SOS Gesture Detection**: Recognize basic hand/body gestures signifying distress.
7. **Safety Alerts System**: Generate high-priority audio-visual and log alerts.
8. **SQLite Database Storage**: Store alert events, timestamps, location coordinates, and metadata.
9. **Historical Hotspot Analysis**: Analyze recorded alert incidents to identify high-risk spatial hotspots.
10. **Safety Report Generation**: Export PDF/CSV summaries for security personnel and authorities.

---

## 📁 Directory Structure

```text
women_safety_analytics/
├── main.py              # CLI Application Entry Point
├── requirements.txt     # Python Dependencies
├── README.md            # Project Overview & Instructions
├── .gitignore          # Git ignore file
├── detection/           # Person, gender, and SOS gesture detection modules
├── analytics/           # Spatial density, lone woman, & hotspot analytics
├── database/            # SQLite connection, schemas, and queries
├── alerts/              # Real-time alert dispatch logic
├── reports/             # PDF report generator modules
├── data/                # Sample input videos, images, & DB storage
├── models/              # Pretrained model weights (.pt files)
└── utils/               # Helper functions (time, math, drawing overlays)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher

### Running the Application

1. Clone or navigate to the project directory:
   ```bash
   cd women_safety_analytics
   ```

2. Launch the terminal application:
   ```bash
   python main.py
   ```
