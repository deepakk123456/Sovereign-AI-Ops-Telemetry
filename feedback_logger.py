import sqlite3
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "llm_observability_core.db")

class LLMOpsDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.initialize_tables()

    def initialize_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    prompt TEXT,
                    status TEXT,
                    violation_type TEXT,
                    severity_score REAL,
                    latency_ms REAL,
                    hallucination_index REAL,
                    cost_usd REAL,
                    jailbreak_prob REAL,
                    cache_hit_flag INTEGER
                )
            """)
            
            # Dynamic Migration Matrix to append columns if schema cache exists
            try:
                self.conn.execute("ALTER TABLE audit_logs ADD COLUMN jailbreak_prob REAL")
                self.conn.execute("ALTER TABLE audit_logs ADD COLUMN cache_hit_flag INTEGER")
            except sqlite3.OperationalError:
                pass

    def commit_transaction(self, prompt: str, status: str, violation: str, severity: float, lat: float, hallucination: float, cost: float, jailbreak: float, cache_hit: int):
        with self.conn:
            self.conn.execute("""
                INSERT INTO audit_logs (timestamp, prompt, status, violation_type, severity_score, latency_ms, hallucination_index, cost_usd, jailbreak_prob, cache_hit_flag)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (time.time(), prompt, status, violation, severity, lat, hallucination, cost, jailbreak, cache_hit))

    def fetch_analytical_aggregates(self, limit: int = 35):
        cursor = self.conn.cursor()
        cursor.execute("SELECT timestamp, status, violation_type, severity_score, latency_ms, hallucination_index, cost_usd, jailbreak_prob, cache_hit_flag FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()