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
            print("\n[!] Analyze Video - Feature coming soon.")
        elif choice == '2':
            print("\n[!] Analyze Image - Feature coming soon.")
        elif choice == '3':
            print("\n[!] Live Camera - Feature coming soon.")
        elif choice == '4':
            print("\n[!] View Safety Alerts - Feature coming soon.")
        elif choice == '5':
            print("\n[!] Gender Statistics - Feature coming soon.")
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
