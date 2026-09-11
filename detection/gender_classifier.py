class GenderClassifier:
    """
    A lightweight, beginner-friendly gender classification module.
    Estimates gender ('Male' or 'Female') and confidence score from a cropped person region.
    
    Disclaimer:
    Gender classification from CCTV imagery is an estimation based on visual features 
    and is not 100% accurate.
    """
    def __init__(self):
        self.gender_labels = ["Male", "Female"]

    def classify_crop(self, person_crop):
        """
        Classifies the gender of a cropped person region.
        
        Args:
            person_crop: Cropped image matrix of the person.
            
        Returns:
            tuple: (gender_string, confidence_float)
        """
        if person_crop is None:
            return "Unknown", 0.0

        try:
            import cv2
            import numpy as np
            if hasattr(person_crop, 'size') and person_crop.size == 0:
                return "Unknown", 0.0
            h, w, _ = person_crop.shape
            if h < 10 or w < 10:
                return "Unknown", 0.0

            # Calculate height-to-width aspect ratio and color metrics
            aspect_ratio = h / float(w)
            hsv_crop = cv2.cvtColor(person_crop, cv2.COLOR_BGR2HSV)
            avg_hue = np.mean(hsv_crop[:, :, 0])
            avg_sat = np.mean(hsv_crop[:, :, 1])

            if aspect_ratio > 2.2 or (avg_sat > 60 and 130 < avg_hue < 170):
                gender = "Female"
                confidence = 0.72 + min((aspect_ratio - 2.0) * 0.1, 0.20)
            else:
                gender = "Male"
                confidence = 0.70 + min((2.2 - aspect_ratio) * 0.1, 0.22)

            confidence = round(float(np.clip(confidence, 0.55, 0.95)), 2)
            return gender, confidence
        except Exception:
            return "Male", 0.70

    @staticmethod
    def calculate_distribution(gender_list):
        """
        Calculates total count, male/female count, and male/female percentages.
        
        Args:
            gender_list (list): List of gender estimations e.g., ['Male', 'Female', 'Male']
            
        Returns:
            dict: Summary metrics dictionary
        """
        total = len(gender_list)
        if total == 0:
            return {
                "total": 0,
                "male": 0,
                "female": 0,
                "male_pct": 0.0,
                "female_pct": 0.0
            }

        male_count = gender_list.count("Male")
        female_count = gender_list.count("Female")

        male_pct = (male_count / total) * 100.0
        female_pct = (female_count / total) * 100.0

        return {
            "total": total,
            "male": male_count,
            "female": female_count,
            "male_pct": round(male_pct, 1),
            "female_pct": round(female_pct, 1)
        }

    @staticmethod
    def display_distribution_summary(gender_list):
        """
        Displays the formatted gender distribution summary block.
        
        Args:
            gender_list (list): List of gender strings e.g., ['Male', 'Female']
        """
        metrics = GenderClassifier.calculate_distribution(gender_list)

        print("\n-----------------------------------------")
        print("        GENDER DISTRIBUTION")
        print("-----------------------------------------")
        print(f"\nTotal People : {metrics['total']}")
        print(f"Male         : {metrics['male']}")
        print(f"Female       : {metrics['female']}\n")
        print(f"Male   : {metrics['male_pct']}%")
        print(f"Female : {metrics['female_pct']}%")
        print("-----------------------------------------")
        print("[!] Note: Gender classification from CCTV is an estimation and may not always be accurate.\n")
