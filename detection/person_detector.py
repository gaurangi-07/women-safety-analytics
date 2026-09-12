import os
import cv2
from ultralytics import YOLO
from .gender_classifier import GenderClassifier
from .gesture_detector import SOSGestureDetector
from analytics.threat_detection import ThreatDetector

class PersonDetector:
    """
    A class to handle person detection using pretrained YOLO model,
    integrate gender classification, threat detection rules, and SOS gesture detection.
    """
    def __init__(self, model_name="yolov8n.pt"):
        """Initialize YOLO, GenderClassifier, ThreatDetector, and SOSGestureDetector."""
        # COCO dataset class index 0 corresponds to 'person'
        self.person_class_id = 0
        print("[+] Loading YOLO model...")
        self.model = YOLO(model_name)
        self.gender_classifier = GenderClassifier()
        self.threat_detector = ThreatDetector()
        self.gesture_detector = SOSGestureDetector()

    def detect_in_image(self, image_path):
        """
        Detect people in a single image and estimate gender for each detected person.
        
        Args:
            image_path (str): Path to the image file.
            
        Returns:
            tuple: (person_boxes, detected_genders)
        """
        if not os.path.exists(image_path):
            print(f"\n[X] Error: Image file not found at '{image_path}'")
            return [], []

        image = cv2.imread(image_path)
        if image is None:
            print(f"\n[X] Error: Unable to read image file at '{image_path}'")
            return [], []

        # Run inference
        results = self.model(image, verbose=False)
        person_boxes = []
        genders = []

        for result in results:
            for box in result.boxes:
                # Check if the detected class is 'person' (class_id == 0)
                cls_id = int(box.cls[0])
                if cls_id == self.person_class_id:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])

                    # Crop detected person region for gender classification
                    crop = image[max(0, y1):min(image.shape[0], y2), max(0, x1):min(image.shape[1], x2)]
                    gender, g_conf = self.gender_classifier.classify_crop(crop)
                    genders.append(gender)

                    person_boxes.append({
                        "box": (x1, y1, x2, y2),
                        "confidence": conf,
                        "gender": gender,
                        "gender_confidence": g_conf
                    })

                    # Color coding: Pink for Female, Light Blue for Male
                    color = (180, 105, 255) if gender == "Female" else (255, 191, 0)

                    # Draw bounding box around detected person
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    label = f"Person: {gender} ({int(g_conf * 100)}%)"
                    cv2.putText(image, label, (x1, max(y1 - 10, 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        count = len(person_boxes)

        # Display detection count overlay on the image
        count_text = f"People Count: {count}"
        cv2.putText(image, count_text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        print(f"\n[+] Detection Complete! Total People Detected: {count}")
        
        # Display formatted gender distribution table
        self.gender_classifier.display_distribution_summary(genders)

        # Save scene stats to database
        try:
            from database import save_gender_stat
            save_gender_stat(
                source_name=os.path.basename(image_path),
                male_count=genders.count("Male"),
                female_count=genders.count("Female")
            )
        except Exception as e:
            print(f"[!] Database Warning: Unable to save gender stat: {e}")

        # Evaluate threat detection rules & SOS gesture
        self.threat_detector.check_lone_woman_at_night(person_boxes, camera_name="IMAGE-ANALYSIS")
        self.threat_detector.check_woman_surrounded_by_men(person_boxes, camera_name="IMAGE-ANALYSIS")
        self.gesture_detector.process_frame(image, camera_name="IMAGE-ANALYSIS")

        print("[+] Displaying image window. Press any key on the image window to close.")
        cv2.imshow("Women Safety Analytics - Person & Gender Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return person_boxes, genders

    def detect_in_video(self, video_path):
        """
        Detect people in a video file frame-by-frame and estimate gender.
        
        Args:
            video_path (str): Path to the video file.
            
        Returns:
            list: Detections per frame
        """
        if not os.path.exists(video_path):
            print(f"\n[X] Error: Video file not found at '{video_path}'")
            return []

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"\n[X] Error: Unable to open video file at '{video_path}'")
            return []

        print("\n[+] Processing video... Press 'q' on the video window to exit.")

        all_frames_data = []
        all_detected_genders = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame, verbose=False)
            frame_person_boxes = []

            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    if cls_id == self.person_class_id:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])

                        crop = frame[max(0, y1):min(frame.shape[0], y2), max(0, x1):min(frame.shape[1], x2)]
                        gender, g_conf = self.gender_classifier.classify_crop(crop)
                        all_detected_genders.append(gender)

                        frame_person_boxes.append({
                            "box": (x1, y1, x2, y2),
                            "confidence": conf,
                            "gender": gender,
                            "gender_confidence": g_conf
                        })

                        color = (180, 105, 255) if gender == "Female" else (255, 191, 0)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        label = f"{gender} ({int(g_conf * 100)}%)"
                        cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            count = len(frame_person_boxes)
            all_frames_data.append(frame_person_boxes)

            # Evaluate threat detection rules & SOS gesture
            self.threat_detector.check_lone_woman_at_night(frame_person_boxes, camera_name="VIDEO-STREAM")
            self.threat_detector.check_woman_surrounded_by_men(frame_person_boxes, camera_name="VIDEO-STREAM")
            self.gesture_detector.process_frame(frame, camera_name="VIDEO-STREAM")

            # Display detection count overlay on the frame
            count_text = f"People Count: {count}"
            cv2.putText(frame, count_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            cv2.imshow("Women Safety Analytics - Video Detection", frame)

            # Press 'q' to stop video playback early
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[!] Video processing stopped by user.")
                break

        cap.release()
        cv2.destroyAllWindows()
        print("\n[+] Video processing finished.")

        # Print overall video gender distribution summary
        self.gender_classifier.display_distribution_summary(all_detected_genders)

        # Save video scene stats to database
        try:
            from database import save_gender_stat
            save_gender_stat(
                source_name=os.path.basename(video_path),
                male_count=all_detected_genders.count("Male"),
                female_count=all_detected_genders.count("Female")
            )
        except Exception as e:
            print(f"[!] Database Warning: Unable to save gender stat: {e}")

        return all_frames_data
