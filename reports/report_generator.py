import os
import datetime
from database.database import get_all_alerts, get_aggregate_gender_stats
from analytics.hotspot_analysis import HotspotAnalyzer

class ReportGenerator:
    """
    Module for generating plain text safety summary reports.
    Saves generated reports to data/reports/safety_report.txt.
    """
    def __init__(self, output_path="data/reports/safety_report.txt"):
        self.output_path = output_path

    def generate_report(self):
        """
        Gathers system analytics (alerts, demographics, hotspots)
        and writes a structured text report to file.
        """
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        alerts = get_all_alerts()
        total_alerts = len(alerts)
        
        high_alerts = sum(1 for a in alerts if a.get('severity') == 'HIGH')
        medium_alerts = sum(1 for a in alerts if a.get('severity') == 'MEDIUM')
        low_alerts = sum(1 for a in alerts if a.get('severity') == 'LOW')
        
        # Demographics statistics
        g_stats = get_aggregate_gender_stats()
        
        # Hotspots analysis
        analyzer = HotspotAnalyzer()
        hotspots, top_hotspot = analyzer.analyze_hotspots()
        top_hotspot_str = f"{top_hotspot} ({hotspots[0]['total']} total alerts)" if (hotspots and top_hotspot) else "N/A"
        
        # Most common alert type
        alert_types = {}
        for a in alerts:
            atype = a.get('alert_type', 'Unknown')
            alert_types[atype] = alert_types.get(atype, 0) + 1
        
        most_common_type = max(alert_types, key=alert_types.get) if alert_types else "N/A"
        
        timestamp_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_lines = [
            "=================================================",
            "          WOMEN SAFETY ANALYTICS REPORT          ",
            "=================================================",
            f"Generated On: {timestamp_now}\n",
            "-------------------------------------------------",
            "1. ALERT SUMMARY",
            "-------------------------------------------------",
            f"Total Safety Alerts Recorded : {total_alerts}",
            f"  - High Severity Alerts     : {high_alerts}",
            f"  - Medium Severity Alerts   : {medium_alerts}",
            f"  - Low Severity Alerts      : {low_alerts}\n",
            "-------------------------------------------------",
            "2. DEMOGRAPHICS & GENDER STATISTICS",
            "-------------------------------------------------",
            f"Total People Analyzed        : {g_stats['total']}",
            f"Male Count                   : {g_stats['male']} ({g_stats['male_pct']:.2f}%)",
            f"Female Count                 : {g_stats['female']} ({g_stats['female_pct']:.2f}%)\n",
            "-------------------------------------------------",
            "3. LOCATION & HOTSPOT ANALYSIS",
            "-------------------------------------------------",
            f"Top Safety Hotspot           : {top_hotspot_str}",
            f"Most Common Alert Type       : {most_common_type}\n",
            "-------------------------------------------------",
            "4. RECENT SAFETY ALERTS",
            "-------------------------------------------------"
        ]

        if not alerts:
            report_lines.append("No safety alerts currently logged.\n")
        else:
            recent_alerts = alerts[:10]
            for a in recent_alerts:
                report_lines.append(
                    f"[{a['timestamp']}] ID #{a['id']} | Type: {a['alert_type']} | Severity: {a['severity']} | Location: {a['location']}"
                )
            report_lines.append("")

        report_lines.append("=================================================")
        report_lines.append("                END OF REPORT                    ")
        report_lines.append("=================================================")

        report_content = "\n".join(report_lines)

        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"\nReport generated successfully:\n{self.output_path}\n")
        return self.output_path


def generate_safety_report():
    generator = ReportGenerator()
    return generator.generate_report()
