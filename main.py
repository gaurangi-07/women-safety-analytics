"""
main.py – Women Safety Analytics
Entry point for the terminal application.
Uses the Rich library for professional terminal formatting.
"""

import sys
import os

# ─────────────────────────────────────────────────────────────────────────────
#  Ensure project root is on sys.path so all package imports resolve correctly
#  regardless of which directory the user runs the script from.
# ─────────────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()

# ─────────────────────────────────────────────────────────────────────────────
#  Severity colour helper
# ─────────────────────────────────────────────────────────────────────────────
SEVERITY_STYLES = {
    "HIGH":   "bold red",
    "MEDIUM": "bold yellow",
    "LOW":    "bold green",
}

def severity_style(sev: str) -> str:
    return SEVERITY_STYLES.get(str(sev).upper(), "white")


# ─────────────────────────────────────────────────────────────────────────────
#  Menu
# ─────────────────────────────────────────────────────────────────────────────
def display_menu():
    console.print()
    console.print(Panel.fit(
        "[bold white]WOMEN SAFETY ANALYTICS[/bold white]\n[dim italic]AI Safety Monitoring System[/dim italic]",
        border_style="red",
        padding=(0, 4),
    ))

    menu_items = [
        ("[bold cyan]1.[/bold cyan]", "Analyze Video"),
        ("[bold cyan]2.[/bold cyan]", "Analyze Image"),
        ("[bold cyan]3.[/bold cyan]", "Live Camera"),
        ("[bold cyan]4.[/bold cyan]", "View Safety Alerts"),
        ("[bold cyan]5.[/bold cyan]", "Gender Statistics"),
        ("[bold cyan]6.[/bold cyan]", "Hotspot Analysis"),
        ("[bold cyan]7.[/bold cyan]", "Generate Report"),
        ("[bold red]8.[/bold red]",   "Exit"),
    ]
    menu_text = "\n".join(f"  {num} {label}" for num, label in menu_items)
    console.print(Panel(menu_text, border_style="dim white", title="[bold]Menu[/bold]", padding=(0, 2)))


# ─────────────────────────────────────────────────────────────────────────────
#  Option 1 – Analyze Video
# ─────────────────────────────────────────────────────────────────────────────
def analyze_video():
    video_path = console.input("\n[bold cyan]Enter video path:[/bold cyan] ").strip()

    if not video_path:
        console.print("[red]Error: No path entered.[/red]")
        return

    if not os.path.exists(video_path):
        console.print(f"[red]File not found: {video_path}[/red]")
        return

    try:
        from detection.person_detector import PersonDetector
        console.print("[dim]Loading model and processing video. Press 'q' in the video window to stop early.[/dim]")
        with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing video frames..."), transient=False) as progress:
            task = progress.add_task("[cyan]Processing...", total=None)
            detector = PersonDetector()
            detector.detect_in_video(video_path)
            progress.update(task, completed=True)

    except ImportError as e:
        console.print(f"[red]Missing package: {e}[/red]")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
    except Exception as e:
        console.print(f"[red]Video analysis error: {e}[/red]")


# ─────────────────────────────────────────────────────────────────────────────
#  Option 2 – Analyze Image
# ─────────────────────────────────────────────────────────────────────────────
def analyze_image():
    image_path = console.input("\n[bold cyan]Enter image path:[/bold cyan] ").strip()

    if not image_path:
        console.print("[red]Error: No path entered.[/red]")
        return

    if not os.path.exists(image_path):
        console.print(f"[red]File not found: {image_path}[/red]")
        return

    try:
        from detection.person_detector import PersonDetector
        with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing image..."), transient=True) as progress:
            progress.add_task("", total=None)
            detector = PersonDetector()
            detector.detect_in_image(image_path)

    except ImportError as e:
        console.print(f"[red]Missing package: {e}[/red]")
        console.print("[yellow]Run: pip install -r requirements.txt[/yellow]")
    except Exception as e:
        console.print(f"[red]Image analysis error: {e}[/red]")


# ─────────────────────────────────────────────────────────────────────────────
#  Option 3 – Live Camera
# ─────────────────────────────────────────────────────────────────────────────
def live_camera():
    try:
        import cv2
    except ImportError:
        console.print("[red]OpenCV not installed. Run: pip install opencv-python[/red]")
        return

    console.print("[dim]Opening default camera (index 0). Press 'q' in the window to stop.[/dim]")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        console.print("[red]Camera could not be opened. Check if it is connected and not in use.[/red]")
        return

    try:
        from detection.person_detector import PersonDetector
        detector = PersonDetector()
    except Exception as e:
        console.print(f"[red]Model loading failed: {e}[/red]")
        cap.release()
        return

    console.print("[green]Camera opened. Streaming...[/green]")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                console.print("[red]Camera feed lost.[/red]")
                break

            results = detector.model(frame, verbose=False)
            frame_boxes = []

            for result in results:
                for box_data in result.boxes:
                    cls_id = int(box_data.cls[0])
                    if cls_id == detector.person_class_id:
                        x1, y1, x2, y2 = map(int, box_data.xyxy[0])
                        crop = frame[max(0, y1):min(frame.shape[0], y2),
                                     max(0, x1):min(frame.shape[1], x2)]
                        gender, g_conf = detector.gender_classifier.classify_crop(crop)
                        frame_boxes.append({
                            "box": (x1, y1, x2, y2),
                            "confidence": float(box_data.conf[0]),
                            "gender": gender,
                            "gender_confidence": g_conf,
                        })
                        color = (180, 105, 255) if gender == "Female" else (255, 191, 0)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        label = f"{gender} ({int(g_conf * 100)}%)"
                        cv2.putText(frame, label, (x1, max(y1 - 10, 20)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            cv2.putText(frame, f"People: {len(frame_boxes)}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            # Threat and SOS detection
            detector.threat_detector.check_lone_woman_at_night(frame_boxes, camera_name="LIVE-CAM")
            detector.threat_detector.check_woman_surrounded_by_men(frame_boxes, camera_name="LIVE-CAM")
            detector.gesture_detector.process_frame(frame, camera_name="LIVE-CAM")

            cv2.imshow("Women Safety Analytics – Live Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        console.print(f"[red]Camera streaming error: {e}[/red]")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        console.print("[dim]Camera session ended.[/dim]")


# ─────────────────────────────────────────────────────────────────────────────
#  Option 4 – View Safety Alerts
# ─────────────────────────────────────────────────────────────────────────────
def display_safety_alerts():
    try:
        from database import get_all_alerts
        alerts = get_all_alerts()
    except Exception as e:
        console.print(f"[red]Database error: {e}[/red]")
        return

    if not alerts:
        console.print(Panel(
            "[yellow]No safety alerts recorded yet.\nRun a video or image analysis first.[/yellow]",
            title="Safety Alerts", border_style="yellow"))
        return

    table = Table(
        title="[bold]SAFETY ALERTS[/bold]",
        box=box.ROUNDED,
        border_style="red",
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("ID",       style="dim",  width=5,  justify="right")
    table.add_column("Type",     min_width=28)
    table.add_column("Severity", justify="center", width=10)
    table.add_column("Location", width=14)
    table.add_column("Time",     width=8)

    alert_dict = {}
    for alert in alerts:
        aid = alert['id']
        alert_dict[aid] = alert
        sev = str(alert.get('severity', '')).upper()
        sev_text = Text(sev, style=severity_style(sev))
        ts = alert['timestamp']
        time_str = ts.split(" ")[-1][:5] if " " in ts else ts[:5]
        table.add_row(str(aid), alert['alert_type'], sev_text,
                      alert.get('location', 'N/A'), time_str)

    console.print(table)

    choice = console.input("\n[dim]Enter alert ID for details (or press Enter to go back):[/dim] ").strip()
    if not choice:
        return

    if not choice.isdigit():
        console.print("[red]Please enter a valid numeric alert ID.[/red]")
        return

    target_id = int(choice)
    if target_id not in alert_dict:
        console.print(f"[red]Alert ID #{target_id} not found.[/red]")
        return

    a = alert_dict[target_id]
    sev = str(a.get('severity', '')).upper()
    detail = (
        f"[bold]Alert Type :[/bold] {a['alert_type']}\n"
        f"[bold]Severity   :[/bold] [{severity_style(sev)}]{sev}[/{severity_style(sev)}]\n"
        f"[bold]Timestamp  :[/bold] {a['timestamp']}\n"
        f"[bold]Location   :[/bold] {a['location']}\n"
        f"[bold]People     :[/bold] {a['female_count']} Female(s), {a['male_count']} Male(s)\n\n"
        f"[bold]Description:[/bold]\n{a['description']}"
    )
    console.print(Panel(detail, title=f"[bold]Alert Details  #[bold]{a['id']}[/bold]",
                        border_style=severity_style(sev), padding=(1, 2)))


# ─────────────────────────────────────────────────────────────────────────────
#  Option 5 – Gender Statistics
# ─────────────────────────────────────────────────────────────────────────────
def display_gender_statistics():
    try:
        from database import get_aggregate_gender_stats, get_latest_gender_stat
    except Exception as e:
        console.print(f"[red]Database error: {e}[/red]")
        return

    with Progress(SpinnerColumn(), TextColumn("[cyan]Loading gender statistics..."), transient=True) as p:
        p.add_task("", total=None)
        stats  = get_aggregate_gender_stats()
        latest = get_latest_gender_stat()

    if stats['total'] == 0:
        console.print(Panel(
            "[yellow]No gender data yet.\nAnalyze a video or image first.[/yellow]",
            title="Gender Statistics", border_style="yellow"))
        return

    table = Table(
        title="[bold]GENDER STATISTICS[/bold]",
        box=box.ROUNDED, border_style="magenta", header_style="bold cyan",
    )
    table.add_column("Metric", style="bold", min_width=28)
    table.add_column("Value",  justify="right", min_width=14)

    table.add_row("Total People Analyzed", str(stats['total']))
    table.add_row("Male",                  f"[cyan]{stats['male']}[/cyan]")
    table.add_row("Female",                f"[magenta]{stats['female']}[/magenta]")
    table.add_row("Male Percentage",       f"[cyan]{stats['male_pct']:.2f}%[/cyan]")
    table.add_row("Female Percentage",     f"[magenta]{stats['female_pct']:.2f}%[/magenta]")
    console.print(table)

    if latest:
        m = latest['male_count']
        f = latest['female_count']
        t = latest['total_count']
        m_pct = (m / t * 100) if t > 0 else 0.0
        f_pct = (f / t * 100) if t > 0 else 0.0

        lt = Table(title="[bold]LATEST SCENE[/bold]",
                   box=box.SIMPLE_HEAVY, border_style="dim", header_style="bold yellow")
        lt.add_column("Metric", style="bold", min_width=22)
        lt.add_column("Value",  justify="right", min_width=16)
        lt.add_row("Source",       latest['source_name'])
        lt.add_row("Time",         latest['timestamp'])
        lt.add_row("Total People", str(t))
        lt.add_row("Male",         f"[cyan]{m} ({m_pct:.2f}%)[/cyan]")
        lt.add_row("Female",       f"[magenta]{f} ({f_pct:.2f}%)[/magenta]")
        console.print(lt)


# ─────────────────────────────────────────────────────────────────────────────
#  Option 6 – Hotspot Analysis
# ─────────────────────────────────────────────────────────────────────────────
def display_hotspot_analysis():
    try:
        from analytics.hotspot_analysis import HotspotAnalyzer
    except Exception as e:
        console.print(f"[red]Import error: {e}[/red]")
        return

    with Progress(SpinnerColumn(), TextColumn("[cyan]Analyzing hotspots..."), transient=True) as p:
        p.add_task("", total=None)
        analyzer = HotspotAnalyzer()
        sorted_locations, highest_location = analyzer.analyze_hotspots()

    if not sorted_locations:
        console.print(Panel(
            "[yellow]No alert data found.\nAlerts are saved automatically during video/image analysis.[/yellow]",
            title="Safety Hotspots", border_style="yellow"))
        return

    table = Table(
        title="[bold]SAFETY HOTSPOTS[/bold]",
        box=box.ROUNDED, border_style="red", header_style="bold white on dark_red",
        show_lines=True,
    )
    table.add_column("Location", min_width=14)
    table.add_column("Total",  justify="right", width=8)
    table.add_column("High",   justify="right", width=8)
    table.add_column("Medium", justify="right", width=8)
    table.add_column("Low",    justify="right", width=8)

    for i, item in enumerate(sorted_locations):
        row_style = "bold" if i == 0 else ""
        table.add_row(
            Text(item['location'], style=row_style),
            Text(str(item['total']), style=row_style),
            Text(str(item['high']),   style="bold red"    if item['high']   > 0 else "dim"),
            Text(str(item['medium']), style="bold yellow" if item['medium'] > 0 else "dim"),
            Text(str(item['low']),    style="bold green"  if item['low']    > 0 else "dim"),
        )
    console.print(table)

    if highest_location:
        top = sorted_locations[0]
        console.print(Panel(
            f"[bold red]🔴 {highest_location}[/bold red]  —  "
            f"[bold]{top['total']}[/bold] Total Alerts  |  "
            f"[red]{top['high']} High[/red]  |  "
            f"[yellow]{top['medium']} Medium[/yellow]  |  "
            f"[green]{top['low']} Low[/green]",
            title="[bold]Highest Alert Location[/bold]",
            border_style="red", padding=(0, 2),
        ))


# ─────────────────────────────────────────────────────────────────────────────
#  Option 7 – Generate Report
# ─────────────────────────────────────────────────────────────────────────────
def generate_report():
    try:
        from reports.report_generator import generate_safety_report
    except Exception as e:
        console.print(f"[red]Import error: {e}[/red]")
        return

    try:
        with Progress(SpinnerColumn(), TextColumn("[cyan]Generating report..."), transient=True) as p:
            p.add_task("", total=None)
            output_path = generate_safety_report()

        console.print(Panel(
            f"[bold green]✔  Report generated successfully[/bold green]\n\n"
            f"[dim]Saved to:[/dim] [cyan]{output_path}[/cyan]",
            title="[bold]Report Generator[/bold]",
            border_style="green", padding=(1, 2),
        ))
    except Exception as e:
        console.print(f"[red]Report generation failed: {e}[/red]")


# ─────────────────────────────────────────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────────────────────────────────────────
def main():
    console.clear()
    console.print(Panel.fit(
        "[bold white]Starting Women Safety Analytics...[/bold white]",
        border_style="dim red", padding=(0, 2),
    ))

    while True:
        try:
            display_menu()
            choice = console.input("\n[bold white]Enter your choice (1-8):[/bold white] ").strip()
        except KeyboardInterrupt:
            console.print("\n\n[bold yellow]Interrupted. Exiting...[/bold yellow]")
            sys.exit(0)

        if choice == '1':
            analyze_video()
        elif choice == '2':
            analyze_image()
        elif choice == '3':
            live_camera()
        elif choice == '4':
            display_safety_alerts()
        elif choice == '5':
            display_gender_statistics()
        elif choice == '6':
            display_hotspot_analysis()
        elif choice == '7':
            generate_report()
        elif choice == '8':
            console.print(Panel(
                "[bold green]Goodbye! Stay safe.[/bold green]",
                border_style="green", padding=(0, 4),
            ))
            sys.exit(0)
        else:
            console.print("[red]Please enter a valid option between 1 and 8.[/red]")


if __name__ == "__main__":
    main()
