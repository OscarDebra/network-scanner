import subprocess
import xml.etree.ElementTree as ET
import time
import ipaddress
from config import Config

_last_scan_time = 0


def is_valid_subnet(subnet: str) -> bool:
    try:
        requested = ipaddress.ip_network(subnet, strict=False)
        allowed = ipaddress.ip_network(Config.ALLOWED_SUBNET, strict=False)
        return requested.subnet_of(allowed) or requested == allowed
    except ValueError:
        return False


def can_scan_now() -> bool:
    global _last_scan_time
    return (time.time() - _last_scan_time) >= Config.RATE_LIMIT_SECONDS


def scan_network(subnet: str = None) -> list:
    global _last_scan_time

    if subnet is None:
        subnet = Config.ALLOWED_SUBNET

    if not is_valid_subnet(subnet):
        raise ValueError(f"Subnet {subnet} is not allowed.")

    if not can_scan_now():
        wait = int(Config.RATE_LIMIT_SECONDS - (time.time() - _last_scan_time))
        raise RateLimitError(f"Please wait {wait}s before scanning again.")

    result = subprocess.run(
        ["nmap", "-sn", "-T4", "--host-timeout", "5s", "-oX", "-", subnet],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"nmap error: {result.stderr}")

    _last_scan_time = time.time()
    return parse_nmap_xml(result.stdout)


def parse_nmap_xml(xml_output: str) -> list:
    root = ET.fromstring(xml_output)
    devices = []

    for host in root.findall("host"):
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue

        ip, mac, hostname, vendor = "Unknown", "N/A", "Unknown", "Unknown"

        for addr in host.findall("address"):
            if addr.get("addrtype") == "ipv4":
                ip = addr.get("addr", "Unknown")
            elif addr.get("addrtype") == "mac":
                mac = addr.get("addr", "N/A")
                vendor = addr.get("vendor", "Unknown")

        hostnames = host.find("hostnames")
        if hostnames is not None:
            first = hostnames.find("hostname")
            if first is not None:
                hostname = first.get("name", "Unknown")

        devices.append({
            "ip": ip,
            "hostname": hostname,
            "mac": mac,
            "vendor": vendor,
            "status": "up",
            "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        })

    return sorted(devices, key=lambda d: list(map(int, d["ip"].split("."))))


class RateLimitError(Exception):
    pass