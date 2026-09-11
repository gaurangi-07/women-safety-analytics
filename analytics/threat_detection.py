import datetime
import math
from alerts.alert_manager import generate_alert

class ThreatDetector:
    """
    Analytics module for evaluating safety risk patterns.
    
    Contains rule-based logic to detect situational risk patterns
    such as 'Lone Woman at Night' and 'Woman Surrounded by Men'.
    
    Disclaimer:
    These rules identify potential safety risk patterns for monitoring
    and do NOT declare that a crime has definitely occurred.
    """
    def __init__(self, night_start=20, night_end=6, isolation_distance=250, 
                 surround_distance=250, nearby_male_threshold=3, min_consecutive_frames=3):
        """
        Configurable rules for safety analysis.
        
        Args:
            night_start (int): Hour marking start of night (default: 20 = 8 PM)
            night_end (int): Hour marking end of night (default: 6 = 6 AM)
            isolation_distance (int): Distance in pixels to determine spatial isolation
            surround_distance (int): Distance in pixels to determine proximity of males
            nearby_male_threshold (int): Minimum males nearby to trigger surrounded alert (default: 3)
            min_consecutive_frames (int): Required consecutive positive frames before alert
        """
        # Lone woman rule settings
        self.NIGHT_START = night_start
        self.NIGHT_END = night_end
        self.ISOLATION_DISTANCE = isolation_distance

        # Woman surrounded rule settings
        self.SURROUND_DISTANCE = surround_distance
        self.NEARBY_MALE_THRESHOLD = nearby_male_threshold

        self.MIN_CONSECUTIVE_FRAMES = min_consecutive_frames

        # Counters to track consecutive frames matching criteria
        self.lone_woman_frame_counter = 0
        self.surrounded_frame_counter = 0

    def is_night_time(self, current_hour=None):
        """
        Rule 1: Check whether the current time falls during night hours (8 PM - 6 AM).
        """
        if current_hour is None:
            current_hour = datetime.datetime.now().hour

        if self.NIGHT_START > self.NIGHT_END:
            return current_hour >= self.NIGHT_START or current_hour < self.NIGHT_END
        else:
            return self.NIGHT_START <= current_hour < self.NIGHT_END

    def calculate_center_distance(self, box1, box2):
        """
        Calculates Euclidean distance between the center points of two bounding boxes.
        
        Mathematics Explanation for 2nd-Year CS Students:
        1. Find Center of Bounding Box 1:
           cx1 = (x1 + x2) / 2
           cy1 = (y1 + y2) / 2
        2. Find Center of Bounding Box 2:
           cx2 = (x1 + x2) / 2
           cy2 = (y1 + y2) / 2
        3. Calculate 2D Euclidean Distance (Pythagorean Theorem):
           distance = sqrt((cx1 - cx2)^2 + (cy1 - cy2)^2)
        """
        cx1 = (box1[0] + box1[2]) / 2.0
        cy1 = (box1[1] + box1[3]) / 2.0
        cx2 = (box2[0] + box2[2]) / 2.0
        cy2 = (box2[1] + box2[3]) / 2.0
        return math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

    def check_lone_woman_at_night(self, frame_detections, current_hour=None, camera_name="CAM-01"):
        """
        Rule Evaluation: Lone Woman at Night
        
        Triggers a MEDIUM severity alert if an isolated female is detected during night hours.
        """
        if not self.is_night_time(current_hour):
            self.lone_woman_frame_counter = 0
            return False

        females = [d for d in frame_detections if d.get('gender') == 'Female']
        if not females:
            self.lone_woman_frame_counter = 0
            return False

        is_isolated = False
        for female in females:
            f_box = female.get('box', (0, 0, 0, 0))
            nearby_people = [
                p for p in frame_detections 
                if p != female and self.calculate_center_distance(f_box, p.get('box', (0, 0, 0, 0))) < self.ISOLATION_DISTANCE
            ]
            if len(nearby_people) == 0:
                is_isolated = True
                break

        if is_isolated:
            self.lone_woman_frame_counter += 1
        else:
            self.lone_woman_frame_counter = 0

        if self.lone_woman_frame_counter >= self.MIN_CONSECUTIVE_FRAMES:
            males_count = sum(1 for d in frame_detections if d.get('gender') == 'Male')
            females_count = len(females)

            generate_alert(
                alert_type="Lone Woman at Night",
                severity="MEDIUM",
                camera_name=camera_name,
                male_count=males_count,
                female_count=females_count,
                description="Potential Safety Risk: Lone Woman at Night pattern detected during night hours."
            )
            self.lone_woman_frame_counter = 0
            return True

        return False

    def check_woman_surrounded_by_men(self, frame_detections, camera_name="CAM-01"):
        """
        Rule Evaluation: Woman Surrounded by Men
        
        Logic:
        1. Identify female and male detections in the frame.
        2. Compute center coordinates of bounding boxes.
        3. Count males within SURROUND_DISTANCE (e.g. 250px) of each female.
        4. If nearby males >= NEARBY_MALE_THRESHOLD (default: 3), trigger HIGH severity alert.
        
        Args:
            frame_detections (list): List of detected person dicts
            camera_name (str): Video stream / camera identifier
            
        Returns:
            bool: True if a safety alert was triggered, False otherwise.
        """
        females = [d for d in frame_detections if d.get('gender') == 'Female']
        males = [d for d in frame_detections if d.get('gender') == 'Male']

        if not females or len(males) < self.NEARBY_MALE_THRESHOLD:
            self.surrounded_frame_counter = 0
            return False

        is_surrounded = False

        for female in females:
            f_box = female.get('box', (0, 0, 0, 0))

            # Find all male detections within SURROUND_DISTANCE of this female
            nearby_males = [
                m for m in males
                if self.calculate_center_distance(f_box, m.get('box', (0, 0, 0, 0))) < self.SURROUND_DISTANCE
            ]

            if len(nearby_males) >= self.NEARBY_MALE_THRESHOLD:
                is_surrounded = True
                break

        if is_surrounded:
            self.surrounded_frame_counter += 1
        else:
            self.surrounded_frame_counter = 0

        # Trigger HIGH severity safety alert after consecutive frames threshold
        if self.surrounded_frame_counter >= self.MIN_CONSECUTIVE_FRAMES:
            generate_alert(
                alert_type="Woman Surrounded by Men",
                severity="HIGH",
                camera_name=camera_name,
                male_count=len(males),
                female_count=len(females),
                description="Potential Safety Risk: Woman surrounded by multiple males detected in monitored area."
            )
            self.surrounded_frame_counter = 0
            return True

        return False
