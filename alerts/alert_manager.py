import datetime

class SafetyAlert:
    """
    Represents a single safety alert event in the Women Safety Analytics system.
    """
    def __init__(self, alert_type, severity="MEDIUM", camera_name="CAM-01", 
                 male_count=0, female_count=0, description=None, timestamp=None):
        self.alert_type = alert_type
        self.severity = severity.upper()
        self.camera_name = camera_name
        self.male_count = male_count
        self.female_count = female_count
        
        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp

        # Standard safety risk wording (Does NOT state a crime occurred)
        if description is None:
            self.description = "A potential safety risk pattern was detected."
        else:
            self.description = description

    def display(self):
        """Displays formatted safety alert banner in the terminal."""
        time_only = self.timestamp.split(" ")[-1] if " " in self.timestamp else self.timestamp

        print("\n========================================")
        print("        SAFETY ALERT")
        print("========================================")
        print(f"Alert Type : {self.alert_type}")
        print(f"Severity   : {self.severity}")
        print(f"Time       : {time_only}")
        print(f"Location   : {self.camera_name}\n")
        print("Description:")
        print(f"{self.description}")
        print("========================================\n")

    def to_dict(self):
        """Returns dictionary representation of the alert."""
        return {
            "alert_type": self.alert_type,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "camera_name": self.camera_name,
            "male_count": self.male_count,
            "female_count": self.female_count,
            "description": self.description
        }


class AlertManager:
    """
    Manages safety alert generation and alert history logging.
    """
    def __init__(self):
        self.alert_history = []

    def generate_alert(self, alert_type, severity="MEDIUM", camera_name="CAM-01", 
                       male_count=0, female_count=0, description=None):
        """
        Generates, displays, and stores a safety alert.
        
        Args:
            alert_type (str): e.g., 'Lone Woman at Night', 'Woman Surrounded by Men', 'SOS Gesture'
            severity (str): 'LOW', 'MEDIUM', 'HIGH'
            camera_name (str): Identifier e.g., 'CAM-01'
            male_count (int): Number of males present
            female_count (int): Number of females present
            description (str): Description of the potential risk
            
        Returns:
            SafetyAlert: The generated alert instance
        """
        # Ensure description states potential safety risk / anomaly (never crime certainty)
        if description is None:
            description = "A potential safety risk pattern was detected."

        alert = SafetyAlert(
            alert_type=alert_type,
            severity=severity,
            camera_name=camera_name,
            male_count=male_count,
            female_count=female_count,
            description=description
        )

        alert.display()
        self.alert_history.append(alert)

        # Save to local SQLite database
        try:
            from database import save_alert
            save_alert(
                alert_type=alert.alert_type,
                severity=alert.severity,
                timestamp=alert.timestamp,
                location=alert.camera_name,
                male_count=alert.male_count,
                female_count=alert.female_count,
                description=alert.description
            )
        except Exception as e:
            print(f"[!] Database Warning: Unable to log alert to SQLite: {e}")

        return alert

    def view_alerts(self):
        """Displays all recorded alerts in history."""
        if not self.alert_history:
            print("\n[!] No safety alerts recorded in current session.")
            return

        print(f"\n--- RECORDED SAFETY ALERTS ({len(self.alert_history)}) ---")
        for i, alert in enumerate(self.alert_history, start=1):
            print(f"\nAlert #{i}:")
            alert.display()


def generate_alert(alert_type, severity="MEDIUM", camera_name="CAM-01", 
                   male_count=0, female_count=0, description=None):
    """
    Standalone function to quickly generate a safety alert.
    """
    manager = AlertManager()
    return manager.generate_alert(
        alert_type=alert_type, 
        severity=severity, 
        camera_name=camera_name, 
        male_count=male_count, 
        female_count=female_count, 
        description=description
    )
