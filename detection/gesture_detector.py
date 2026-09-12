from alerts.alert_manager import generate_alert

class SOSGestureDetector:
    """
    A prototype rule-based SOS Gesture Detector module using MediaPipe.
    
    Prototype Logic:
    Detects raised open-palm Distress / SOS hand gesture landmarks.
    
    Disclaimer:
    This is a prototype feature for educational & demonstration purposes,
    not a production-grade emergency response system.
    """
    def __init__(self, min_consecutive_frames=3):
        """
        Args:
            min_consecutive_frames (int): Required consecutive positive frames before alert
        """
        self.MIN_CONSECUTIVE_FRAMES = min_consecutive_frames
        self.consecutive_sos_frames = 0
        
        self.use_mediapipe = False
        self.mp_hands = None
        self.hands = None

        # Initialize MediaPipe Hands if available
        try:
            import mediapipe as mp
            self.mp_hands = mp.solutions.hands
            self.mp_draw = mp.solutions.drawing_utils
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.use_mediapipe = True
        except Exception:
            self.use_mediapipe = False

    def detect_sos_in_crop(self, image_frame):
        """
        Detects potential SOS hand gesture in an image/frame.
        
        Rule:
        If hand landmarks are detected where all 4 finger tips (index, middle, ring, pinky)
        are extended above the wrist (y_tip < y_wrist), it indicates a raised open-palm SOS signal.
        
        Returns:
            tuple: (gesture_detected: bool, confidence: float)
        """
        if image_frame is None:
            return False, 0.0

        if not self.use_mediapipe or self.hands is None:
            return False, 0.0

        try:
            import cv2
            if hasattr(image_frame, 'size') and image_frame.size == 0:
                return False, 0.0
            # Convert BGR frame to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if not results.multi_hand_landmarks:
                return False, 0.0

            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                
                # Hand Landmark Indices:
                # Wrist: 0, Index tip: 8, Middle tip: 12, Ring tip: 16, Pinky tip: 20
                wrist = landmarks[0]
                index_tip = landmarks[8]
                middle_tip = landmarks[12]
                ring_tip = landmarks[16]
                pinky_tip = landmarks[20]

                # In image normalized coordinates, smaller Y is higher in the frame.
                # Open raised palm gesture: finger tips are above the wrist.
                fingers_raised = (
                    index_tip.y < wrist.y and
                    middle_tip.y < wrist.y and
                    ring_tip.y < wrist.y and
                    pinky_tip.y < wrist.y
                )

                if fingers_raised:
                    elevation_diff = wrist.y - middle_tip.y
                    confidence = round(float(min(max(elevation_diff * 3.0, 0.70), 0.95)), 2)
                    return True, confidence
        except Exception:
            pass

        return False, 0.0

    def process_frame(self, frame, camera_name="CAM-01"):
        """
        Processes a video frame, tracks SOS gesture persistence across frames,
        and generates a HIGH severity safety alert saved to SQLite upon confirmation.
        
        Args:
            frame: Image/Video frame matrix
            camera_name (str): Video stream / camera identifier
            
        Returns:
            bool: True if SOS alert triggered, False otherwise.
        """
        detected, confidence = self.detect_sos_in_crop(frame)

        if detected:
            self.consecutive_sos_frames += 1
        else:
            self.consecutive_sos_frames = 0

        if self.consecutive_sos_frames >= self.MIN_CONSECUTIVE_FRAMES:
            print("\n========================================")
            print("        SOS GESTURE DETECTED")
            print("========================================")
            print("Potential emergency gesture detected.")
            print("HIGH PRIORITY ALERT\n")

            # Generate HIGH severity safety alert (automatically saved to SQLite)
            generate_alert(
                alert_type="SOS Gesture",
                severity="HIGH",
                camera_name=camera_name,
                male_count=0,
                female_count=1,
                description="Potential emergency SOS distress gesture detected in video stream."
            )

            self.consecutive_sos_frames = 0
            return True

        return False
