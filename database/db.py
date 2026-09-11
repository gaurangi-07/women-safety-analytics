"""
Database helper module for Women Safety Analytics.
Uses Python's standard built-in `sqlite3` module (no external pip package required).
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "safety_analytics.db")

def get_connection():
    """Returns a connection to the local SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Placeholder for database schema initialization.
    Tables (alerts, hotspots, statistics) will be defined here in future steps.
    """
    pass
