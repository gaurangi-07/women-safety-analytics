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
            from alerts import generate_alert
            print("\n[+] Displaying sample safety alert system demonstration...")
            generate_alert(
                alert_type="Lone Woman at Night",
                severity="MEDIUM",
                camera_name="CAM-01",
                male_count=0,
                female_count=1,
                description="A potential safety risk pattern was detected."
            )
        elif choice == '5':
            file_path = input("\nEnter image or video path for Gender Statistics: ").strip()
            if not file_path:
                print("\n[X] Error: File path cannot be empty.")
            else:
                try:
                    from detection.person_detector import PersonDetector
                    detector = PersonDetector()
                    if file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        detector.detect_in_video(file_path)
                    else:
                        detector.detect_in_image(file_path)
                except ImportError as e:
                    print(f"\n[X] Missing required packages: {e}")
                    print("[!] Please run: pip install -r requirements.txt")
        elif choice == '6':
            print("\n[!] Hotspot Analysis - Feature coming soon.")
        elif choice == '7':
            print("\n[!] Generate Report - Feature coming soon.")
        elif choice == '8':
            print("\nExiting Women Safety Analytics system. Goodbye!")
            sys.exit(0)
        else:
            print("\n[X] Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
