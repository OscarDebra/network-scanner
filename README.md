# Network Scanner

## Architecture

This is a fullstack network scanner. The backend is a python flask script that scans for devices on the local network with nmap. The backend is connected to an SQlite database. The frontend is made with react. All this is made to run on a small raspberry-pi 3+, but can be run on most things with more processing power. Backend and frontend both have their own docker container file. At root is a docker compose to run the project.

## Physical architecture

The raspberry pi 3+ has a 64gb thumb drive plugged into it, which is its storage and also contains its OS. The Raspberry Pi is connected via Wifi to the local network.

## Setup for a different network

To run this tool on a different network, update the `ALLOWED_SUBNET`
variable in `config.py` to match your local subnet:

```python
ALLOWED_SUBNET = "192.168.1.0/24"  # typical home network
ALLOWED_SUBNET = "10.0.0.0/24"     # typical office network
ALLOWED_SUBNET = "172.31.0.0/23"   # this deployment
```

To find your subnet, run the following command:

Mac/Linux:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Windows:
```bash
ipconfig
```

The output will show your IP address and netmask, from which you can
determine your subnet. For example, an IP of `192.168.1.45` with
netmask `255.255.255.0` means your subnet is `192.168.1.0/24`.

## Limitations

- Hostnames are unresolvable on networks that don't expose reverse DNS (like Elvebakken-IM and BakkaIM) for devices using MAC address randomization (modern iOS, Android, Windows)
- nmap requires root/sudo privileges to read MAC addresses
- Docker network_mode: host is Linux-only; on macOS the backend must run natively for accurate scanning
- Database cannot store who triggered scans, the string "user" is hardcoded instead of requiring a login
- Database is not persistent, stopping the backend container will wipe the whole database
- The API does not accept user-supplied subnet parameters. The subnet is hardcoded in `config.py` and validated in `scanner.py` via `is_valid_subnet()`, this is deliberate because it prevents the tool from scanning subnets that are not validated by the operator. to change the subnet to your own, change the ALLOWED_SUBNET variable in config.py, make sure you have permission to scan on that network first.

## Security

- The API rate-limits scan requests to prevent abuse
- Subnet validation ensures only the configured local network can be scanned
- MAC addresses and IP data are personal data under GDPR — scan history 
  is stored locally and never transmitted externally
- The tool should only be used on networks you have permission to scan.

## Decisions

### Why Python Flask

Flask is quite lightweight, which can be important when running on a weak computer. Fastapi would be better for handling many requests, but that won't ever happen. Flask also has relatively easy integration with nmap, easier than fastapi as far as i could see.

### Why React

I have developed before in react, so i'm decently familiar. I picked it for the ease of use with react being component-based and live-updating. It's also lighter, and closer to standard HTML than frameworks like angular, which makes it easier to adopt based on my previous experience.

### Why SQLite

SQLite is pretty lightweight. A full database like PostgreSQL would be unnecessary for a single-user tool with infrequent writes.

