import time
import ipaddress
from config import Config

_last_scan_time = 0


def is_valid_subnet(subnet: str) -> bool:
    #Only allow scanning the configured local subnet
    try:
        requested = ipaddress.ip_network(subnet, strict=False)
        allowed = ipaddress.ip_network(Config.ALLOWED_SUBNET, strict=False)
        return requested.subnet_of(allowed) or requested == allowed
    except ValueError:
        return False


def can_scan_now() -> bool:
    #prevent scanning more than once every 30 seconds
    global _last_scan_time
    return (time.time() - _last_scan_time) >= Config.RATE_LIMIT


def scan_network(subnet: str = None) -> list:
    global _last_scan_time

    if subnet is None:
        subnet = Config.ALLOWED_SUBNET

    if not is_valid_subnet(subnet):
        raise ValueError(f"Subnet {subnet} is not allowed.")

    if not can_scan_now():
        wait = int(Config.RATE_LIMIT_SECONDS - (time.time() - _last_scan_time))
        raise RateLimitError(f"Please wait {wait}s before scanning again.")

    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments="-sn --host-timeout 10s")
    _last_scan_time = time.time()

    devices = []
    for host in nm.all_hosts():
        addresses = nm[host].get("addresses", {})
        vendor = nm[host].get("vendor", {})
        mac = addresses.get("mac", "N/A")
        devices.append({
            "ip": host,
            "hostname": nm[host].hostname() or "Unknown",
            "mac": mac,
            "vendor": vendor.get(mac, "Unknown"),
            "status": nm[host].state(),
            "scanned_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        })

    return sorted(devices, key=lambda d: list(map(int, d["ip"].split("."))))


class RateLimitError(Exception):
    pass