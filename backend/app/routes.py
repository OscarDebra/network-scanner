from flask import Blueprint, jsonify, request
from config import Config
from app.scanner import scan_network, RateLimitError
from app.models import save_scan, get_scan_history

bp = Blueprint("main", __name__)


@bp.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@bp.route("/api/scan", methods=["GET"])
def scan():
    subnet = request.args.get("subnet", None)
    try:
        devices = scan_network(subnet)
        save_scan(Config.ALLOWED_SUBNET, devices)
        return jsonify({
            "success": True,
            "count": len(devices),
            "devices": devices
        })
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except RateLimitError as e:
        return jsonify({"success": False, "error": str(e)}), 429
    except Exception as e:
        return jsonify({"success": False, "error": "Scan failed", "detail": str(e)}), 500


#Look up a specific IP
@bp.route("/api/devices/<ip>")
def device_detail(ip):
    try:
        devices = scan_network()
        match = next((d for d in devices if d["ip"] == ip), None)
        if match:
            return jsonify(match)
        return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route("/api/history")
def history():
    return jsonify(get_scan_history())

@bp.route("/api/devices")
def devices():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM devices WHERE scan_id = (SELECT MAX(id) FROM scans)"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])