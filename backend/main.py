import nmap

def scan_network(network="192.168.1.0/24"):
    nm = nmap.PortScanner()
    nm.scan(hosts=network, arguments="-sn")  # -sn = ping scan, no ports
    devices = []
    for host in nm.all_hosts():
        devices.append({
            "ip": host,
            "hostname": nm[host].hostname(),
            "mac": nm[host]["addresses"].get("mac", "N/A"),
            "vendor": nm[host]["vendor"].get(nm[host]["addresses"].get("mac",""), "Unknown"),
            "status": nm[host].state()
        })
    return devices