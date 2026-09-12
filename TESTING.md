# Women Safety Analytics — Test Cases

> This document contains manual test cases for the Women Safety Analytics project.  
> "Actual Result" and "Status" columns should be filled in by the tester after running each test.

---

## How to Run the Application

```bash
cd /path/to/women_safety_analytics
python3 main.py
```

---

## TC-01: Application Startup

| Field | Details |
|---|---|
| **Test Case** | Verify the application starts and displays the main menu |
| **Input** | Run `python3 main.py` |
| **Expected Output** | Rich-formatted menu with options 1–8 is displayed. No errors or tracebacks. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-02: Invalid Menu Input

| Field | Details |
|---|---|
| **Test Case** | Enter an invalid option at the main menu |
| **Input** | Type `9` or `abc` and press Enter |
| **Expected Output** | `Please enter a valid option between 1 and 8.` — application does not crash |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-03: Image Analysis — Valid File

| Field | Details |
|---|---|
| **Test Case** | Analyze a valid image file |
| **Input** | Select option `2`, enter a valid `.jpg` or `.png` path |
| **Expected Output** | YOLO model loads, persons are detected, gender distribution is shown, image window opens |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-04: Image Analysis — File Not Found

| Field | Details |
|---|---|
| **Test Case** | Enter a path that does not exist for image analysis |
| **Input** | Select option `2`, enter `nonexistent_image.jpg` |
| **Expected Output** | `File not found: nonexistent_image.jpg` — no crash, returns to menu |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-05: Video Analysis — Valid File

| Field | Details |
|---|---|
| **Test Case** | Analyze a valid video file |
| **Input** | Select option `1`, enter a valid `.mp4` path |
| **Expected Output** | Video plays in a window with bounding boxes, gender labels, and person count overlay. Press `q` to stop. Summary printed on exit. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-06: Video Analysis — File Not Found

| Field | Details |
|---|---|
| **Test Case** | Enter a non-existent video path |
| **Input** | Select option `1`, enter `missing_video.mp4` |
| **Expected Output** | `File not found: missing_video.mp4` — no crash, returns to menu |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-07: Person Detection

| Field | Details |
|---|---|
| **Test Case** | Confirm that persons are detected in an image with people |
| **Input** | Select option `2`, provide an image containing people |
| **Expected Output** | Bounding boxes drawn around people with labels. Terminal prints `Detection Complete! Total People Detected: N` |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-08: Gender Counting

| Field | Details |
|---|---|
| **Test Case** | Verify gender counts are calculated and displayed |
| **Input** | Select option `2`, provide an image with multiple people |
| **Expected Output** | Gender Distribution table printed with Male/Female counts and percentages |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-09: Lone Woman Detection

| Field | Details |
|---|---|
| **Test Case** | Test lone woman at night detection rule |
| **Input** | Run analysis during night hours (8 PM – 6 AM) with a single female in the image/video |
| **Expected Output** | After 3 matching frames: `SAFETY ALERT — Lone Woman at Night — MEDIUM` displayed, alert saved to database |
| **Notes** | This rule only triggers during night hours. Test between 8 PM and 6 AM system time. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-10: Woman Surrounded by Men

| Field | Details |
|---|---|
| **Test Case** | Test woman surrounded by men detection rule |
| **Input** | Provide an image/video showing a woman with 3 or more men within close proximity |
| **Expected Output** | After 3 matching frames: `SAFETY ALERT — Woman Surrounded by Men — HIGH` displayed, alert saved to database |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-11: SOS Gesture Detection

| Field | Details |
|---|---|
| **Test Case** | Test SOS gesture detection using a raised open palm |
| **Input** | Hold hand up to camera with all four fingers extended upward (open palm gesture) for 3+ frames |
| **Expected Output** | `SOS GESTURE DETECTED — HIGH PRIORITY ALERT` displayed in terminal, alert saved to SQLite |
| **Notes** | Requires MediaPipe installed. Works best in good lighting. This is a prototype feature. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-12: Alert Storage

| Field | Details |
|---|---|
| **Test Case** | Verify alerts are saved to the SQLite database |
| **Input** | After any analysis that triggers an alert, select option `4` |
| **Expected Output** | Table of alerts displayed. Each alert shows ID, type, severity, location, and time. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-13: View Alerts — Empty Database

| Field | Details |
|---|---|
| **Test Case** | View alerts on a fresh installation (no alerts stored) |
| **Input** | Select option `4` without running any prior analysis |
| **Expected Output** | `No safety alerts recorded yet. Run a video or image analysis first.` — no crash |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-14: View Alert Details

| Field | Details |
|---|---|
| **Test Case** | View details of a specific alert by entering its ID |
| **Input** | Select option `4`, enter a valid alert ID shown in the table |
| **Expected Output** | Detailed panel displayed showing all fields of the alert |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-15: View Alert Details — Invalid ID

| Field | Details |
|---|---|
| **Test Case** | Enter an ID that does not exist |
| **Input** | Select option `4`, enter `9999` (an ID that does not exist) |
| **Expected Output** | `Alert ID #9999 not found.` — no crash, returns to menu |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-16: Hotspot Analysis

| Field | Details |
|---|---|
| **Test Case** | View hotspot analysis after alerts have been generated |
| **Input** | Select option `6` after running analysis that produced alerts |
| **Expected Output** | Table listing locations with total/high/medium/low alert counts, sorted by total alerts. Highest alert location shown at bottom. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-17: Hotspot Analysis — Empty Database

| Field | Details |
|---|---|
| **Test Case** | View hotspot analysis with no alerts in database |
| **Input** | Select option `6` on a fresh installation |
| **Expected Output** | `No alert data found. Alerts are saved automatically during video/image analysis.` — no crash |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-18: Gender Statistics — Empty Database

| Field | Details |
|---|---|
| **Test Case** | View gender statistics with no data |
| **Input** | Select option `5` on a fresh installation |
| **Expected Output** | `No gender data yet. Analyze a video or image first.` — no crash |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-19: Gender Statistics — With Data

| Field | Details |
|---|---|
| **Test Case** | View gender statistics after running analysis |
| **Input** | Select option `5` after analyzing a video or image |
| **Expected Output** | Table showing total people, male count, female count, male %, female %. Latest scene table shown below. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-20: Report Generation

| Field | Details |
|---|---|
| **Test Case** | Generate a safety report |
| **Input** | Select option `7` |
| **Expected Output** | `Report generated successfully` message shown. File `data/reports/safety_report.txt` is created and readable. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-21: Report Content Verification

| Field | Details |
|---|---|
| **Test Case** | Verify the content of the generated report |
| **Input** | Open `data/reports/safety_report.txt` after running option `7` |
| **Expected Output** | File contains: report header, alert summary with counts, gender statistics, hotspot info, most common alert type, and recent alerts list |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-22: Live Camera — Camera Available

| Field | Details |
|---|---|
| **Test Case** | Open live camera stream |
| **Input** | Select option `3` with a webcam connected |
| **Expected Output** | Camera window opens. Persons detected in real-time with bounding boxes and gender labels. Press `q` to stop. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-23: Live Camera — Camera Not Available

| Field | Details |
|---|---|
| **Test Case** | Try to open live camera without a webcam connected |
| **Input** | Select option `3` with no webcam available |
| **Expected Output** | `Camera could not be opened. Check if it is connected and not in use.` — no crash |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-24: Invalid File Path (Empty Input)

| Field | Details |
|---|---|
| **Test Case** | Press Enter without typing a file path |
| **Input** | Select option `1` or `2`, then press Enter immediately |
| **Expected Output** | `Error: No path entered.` — returns to menu without crashing |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## TC-25: Keyboard Interrupt (Ctrl+C)

| Field | Details |
|---|---|
| **Test Case** | Press Ctrl+C during the main menu prompt |
| **Input** | Press `Ctrl+C` at the `Enter your choice:` prompt |
| **Expected Output** | `Interrupted. Exiting...` message shown. Application exits cleanly. No Python traceback displayed. |
| **Actual Result** | *(fill after testing)* |
| **Status** | ⬜ Not Tested |

---

## Test Summary

| Total Tests | Passed | Failed | Not Tested |
|---|---|---|---|
| 25 | *(fill)* | *(fill)* | 25 |

---

## Status Legend

| Symbol | Meaning |
|---|---|
| ✅ | Passed |
| ❌ | Failed |
| ⚠️ | Partially Passed |
| ⬜ | Not Tested |
