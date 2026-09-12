from database.database import get_all_alerts

class HotspotAnalyzer:
    """
    Module for analyzing historical safety alert hotspots grouped by camera location.
    Queries recorded alerts from SQLite and groups incidents to identify high-risk zones.
    """
    def __init__(self):
        pass

    def analyze_hotspots(self):
        """
        Groups recorded safety alerts by location and computes total/high/medium/low risk counts.
        
        Returns:
            tuple: (sorted_hotspot_list, highest_location_name)
        """
        alerts = get_all_alerts()
        if not alerts:
            return [], None

        location_stats = {}

        for alert in alerts:
            loc = alert.get('location', 'Unknown')
            severity = str(alert.get('severity', 'MEDIUM')).upper()

            if loc not in location_stats:
                location_stats[loc] = {
                    "location": loc,
                    "total": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }

            location_stats[loc]["total"] += 1
            if severity == "HIGH":
                location_stats[loc]["high"] += 1
            elif severity == "LOW":
                location_stats[loc]["low"] += 1
            else:
                location_stats[loc]["medium"] += 1

        # Sort locations by total alerts in descending order
        sorted_locations = sorted(
            location_stats.values(), 
            key=lambda x: x["total"], 
            reverse=True
        )

        highest_location = sorted_locations[0]["location"] if sorted_locations else None
        return sorted_locations, highest_location

    def display_hotspot_report(self):
        """
        Displays the formatted Safety Hotspots report table in the terminal.
        """
        sorted_locations, highest_location = self.analyze_hotspots()

        print("\n===============================================")
        print("              SAFETY HOTSPOTS")
        print("===============================================")

        if not sorted_locations:
            print("\n[!] No historical safety alert data found in database.")
            print("===============================================\n")
            return

        print(f"{'Location':<12} {'Total':<9} {'High':<9} {'Medium':<9} {'Low':<6}")
        print("-----------------------------------------------")

        for item in sorted_locations:
            print(f"{item['location']:<12} {item['total']:<9} {item['high']:<9} {item['medium']:<9} {item['low']:<6}")

        print("\n-----------------------------------------------")
        print("Highest Alert Location:")
        highest_stat = sorted_locations[0]
        print(f"-> {highest_location} ({highest_stat['total']} Total Alerts)")
        print("===============================================\n")


def display_hotspots():
    """
    Helper function to trigger hotspot analysis display.
    """
    analyzer = HotspotAnalyzer()
    analyzer.display_hotspot_report()
