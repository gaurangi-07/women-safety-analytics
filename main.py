import sys

def display_menu():
    print("\n===============================================")
    print("          WOMEN SAFETY ANALYTICS")
    print("       AI Safety Monitoring System")
    print("===============================================")
    print("1. Analyze Video")
    print("2. Analyze Image")
    print("3. Live Camera")
    print("4. View Safety Alerts")
    print("5. Gender Statistics")
    print("6. Hotspot Analysis")
    print("7. Generate Report")
    print("8. Exit")
    print("===============================================")

def display_safety_alerts():
    """
    Fetches and displays recorded safety alerts from SQLite database
    in a clean, formatted table. Allows selecting an alert ID to inspect details.
    """
    from database import get_all_alerts
    alerts = get_all_alerts()

    if not alerts:
        print("\n[!] No safety alerts currently recorded in database.")
        return

    print("\n===============================================")
    print("              SAFETY ALERTS")
    print("===============================================")
    print(f"{'ID':<4} {'TYPE':<26} {'SEVERITY':<10} {'TIME':<8}")
    print("------------------------------------------------")

    alert_dict = {}
    for alert in alerts:
        aid = alert['id']
        alert_dict[aid] = alert
        
        atype = alert['alert_type']
        if len(atype) > 24:
            atype = atype[:21] + "..."
            
        severity = alert['severity']
        timestamp = alert['timestamp']
        time_str = timestamp.split(" ")[-1][:5] if " " in timestamp else timestamp[:5]

        print(f"{aid:<4} {atype:<26} {severity:<10} {time_str:<8}")

    print("===============================================")

    choice = input("\nEnter alert ID to view details (or press Enter to return): ").strip()
    if choice and choice.isdigit():
        target_id = int(choice)
        if target_id in alert_dict:
            a = alert_dict[target_id]
            print("\n========================================")
            print(f"        ALERT DETAILS (ID #{a['id']})")
            print("========================================")
            print(f"Alert Type : {a['alert_type']}")
            print(f"Severity   : {a['severity']}")
            print(f"Timestamp  : {a['timestamp']}")
            print(f"Location   : {a['location']}")
            print(f"People     : {a['female_count']} Female(s), {a['male_count']} Male(s)\n")
            print("Description:")
            print(f"{a['description']}")
            print("========================================\n")
        else:
            print(f"\n[X] Error: Alert ID #{target_id} not found in database.")

def display_gender_statistics():
    """
    Displays overall aggregate and latest scene gender statistics stored in SQLite database.
    """
    from database import get_aggregate_gender_stats, get_latest_gender_stat
    
    stats = get_aggregate_gender_stats()
    latest = get_latest_gender_stat()

    print("\n===============================================")
    print("             GENDER STATISTICS")
    print("===============================================")
    print(f"Total People Analyzed : {stats['total']}")
    print(f"Male                  : {stats['male']}")
    print(f"Female                : {stats['female']}\n")
    print(f"Male Percentage       : {stats['male_pct']:.2f}%")
    print(f"Female Percentage     : {stats['female_pct']:.2f}%")

    if latest:
        m_count = latest['male_count']
        f_count = latest['female_count']
        t_count = latest['total_count']
        m_pct = (m_count / t_count * 100.0) if t_count > 0 else 0.0
        f_pct = (f_count / t_count * 100.0) if t_count > 0 else 0.0

        print("\n-----------------------------------------------")
        print("          LATEST SCENE STATISTICS")
        print("-----------------------------------------------")
        print(f"Source                : {latest['source_name']}")
        print(f"Time                  : {latest['timestamp']}")
        print(f"Total People          : {t_count}")
        print(f"Male                  : {m_count} ({m_pct:.2f}%)")
        print(f"Female                : {f_count} ({f_pct:.2f}%)")

    print("===============================================\n")

def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            video_path = input("\nEnter video path: ").strip()
            if not video_path:
                print("\n[X] Error: Video path cannot be empty.")
            else:
                try:
                    from detection.person_detector import PersonDetector
                    detector = PersonDetector()
                    detector.detect_in_video(video_path)
                except ImportError as e:
                    print(f"\n[X] Missing required packages: {e}")
                    print("[!] Please run: pip install -r requirements.txt")
        elif choice == '2':
            image_path = input("\nEnter image path: ").strip()
            if not image_path:
                print("\n[X] Error: Image path cannot be empty.")
            else:
                try:
                    from detection.person_detector import PersonDetector
                    detector = PersonDetector()
                    detector.detect_in_image(image_path)
                except ImportError as e:
                    print(f"\n[X] Missing required packages: {e}")
                    print("[!] Please run: pip install -r requirements.txt")
        elif choice == '3':
            print("\n[!] Live Camera - Feature coming soon.")
        elif choice == '4':
            display_safety_alerts()
        elif choice == '5':
            display_gender_statistics()
        elif choice == '6':
            from analytics.hotspot_analysis import display_hotspots
            display_hotspots()
        elif choice == '7':
            print("\n[!] Generate Report - Feature coming soon.")
        elif choice == '8':
            print("\nExiting Women Safety Analytics system. Goodbye!")
            sys.exit(0)
        else:
            print("\n[X] Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
