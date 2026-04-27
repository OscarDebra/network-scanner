# Network Scanner

This is a fullstack network scanner. The backend is a python flask script that scans for devices on the local network with nmap. The backend is connected to an SQlite database. The frontend is made with react. All this is made to run on a small raspberry-pi 3+

## Physical architecture

The raspberry pi 3+ has a 64gb thumb drive plugged into it, which is its storage and also contains its OS. The Raspberry Pi is connected via Wifi to the local network.

## Limitations

- Hostnames are unresolvable on networks that don't expose reverse DNS (like Elvebakken-IM and BakkaIM) for devices using MAC address randomization (modern iOS, Android, Windows)
- nmap requires root/sudo privileges to read MAC addresses
- Docker network_mode: host is Linux-only; on macOS the backend must 
  run natively for accurate scanning

## Security

- The API rate-limits scan requests to prevent abuse
- Subnet validation ensures only the configured local network can be scanned
- MAC addresses and IP data are personal data under GDPR — scan history 
  is stored locally and never transmitted externally
- The tool should only be used on networks you own or have permission to scan. 
  Unauthorized network scanning is illegal under Norwegian law (straffeloven § 207)

## Decisions

### Why Python Flask

Flask is quite lightweight, which can be important when running on a weak computer. Fastapi would be better for handling many requests, but that won't ever happen. Flask also has relatively easy integration with nmap, easier than fastapi as far as i could see.

### Why React

I have developed before in react, so i'm decently familiar. I picked it for the ease of use with react being component-based and live-updating. It's also lighter, and closer to standard HTML than frameworks like angular, which makes it easier to adopt based on my previous experience.

### Why SQLite

SQLite is pretty lightweight. A full database like PostgreSQL would be unnecessary for a single-user tool with infrequent writes.

