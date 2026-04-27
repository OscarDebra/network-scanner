import sqlite3
import time
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn

def init_db():
    #Create tables if they don't exist. Call this on app startup.
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS scans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at  TEXT NOT NULL,
            finished_at TEXT,
            subnet      TEXT NOT NULL,
            device_count INTEGER DEFAULT 0,
            triggered_by TEXT DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS devices (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id    INTEGER NOT NULL,
            ip         TEXT NOT NULL,
            mac        TEXT,
            hostname   TEXT,
            vendor     TEXT,
            status     TEXT,
            FOREIGN KEY (scan_id) REFERENCES scans(id)
        );

        CREATE TABLE IF NOT EXISTS known_devices (
            mac         TEXT PRIMARY KEY,
            label       TEXT,
            is_trusted  INTEGER DEFAULT 1,
            first_seen  TEXT,
            last_seen   TEXT
        );
    """)
    conn.commit()
    conn.close()


def save_scan(subnet, devices):
    """Persist a completed scan and its devices. Returns the scan_id."""
    conn = get_db()
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    cur = conn.execute(
        "INSERT INTO scans (started_at, finished_at, subnet, device_count) VALUES (?,?,?,?)",
        (now, now, subnet, len(devices))
    )
    scan_id = cur.lastrowid
    for d in devices:
        conn.execute(
            "INSERT INTO devices (scan_id, ip, mac, hostname, vendor, status) VALUES (?,?,?,?,?,?)",
            (scan_id, d["ip"], d["mac"], d["hostname"], d["vendor"], d["status"])
        )
        if d["mac"] and d["mac"] != "N/A":
            conn.execute("""
                INSERT INTO known_devices (mac, first_seen, last_seen)
                VALUES (?, ?, ?)
                ON CONFLICT(mac) DO UPDATE SET last_seen=excluded.last_seen
            """, (d["mac"], now, now))
    conn.commit()
    conn.close()
    return scan_id


def get_scan_history(limit=10):
    """Return the last N scans with device counts."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM scans ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_unknown_devices():
    """Return devices seen in the latest scan that aren't marked trusted."""
    conn = get_db()
    rows = conn.execute("""
        SELECT d.ip, d.mac, d.hostname, d.vendor
        FROM devices d
        JOIN scans s ON d.scan_id = s.id
        LEFT JOIN known_devices k ON d.mac = k.mac
        WHERE s.id = (SELECT MAX(id) FROM scans)
        AND (k.is_trusted IS NULL OR k.is_trusted = 0)
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]