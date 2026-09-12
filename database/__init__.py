# Database package initialization
from .database import (
    initialize_database,
    save_alert,
    get_all_alerts,
    get_alert_count,
    get_alerts_by_location,
    save_gender_stat,
    get_aggregate_gender_stats,
    get_latest_gender_stat
)

__all__ = [
    "initialize_database",
    "save_alert",
    "get_all_alerts",
    "get_alert_count",
    "get_alerts_by_location",
    "save_gender_stat",
    "get_aggregate_gender_stats",
    "get_latest_gender_stat"
]
