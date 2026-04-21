# Network Scanner

This is a fullstack network scanner. The backend is a python flask script that scans for devices on the local network with nmap. The backend is connected to an SQlite database. The frontend is made with react. All this is made to run on a small raspberry-pi 3+

## Physical architecture

The raspberry pi 3+ has a 64gb thumb drive plugged into it, which is its storage and also contains its OS.

## Decisions

# Why Python Flask

Flask is quite lightweight, which can be important when running on a weak computer. Fastapi would be better for handling many requests, but that won't ever happen. Flask also has relatively easy integration with nmap, easier than fastapi as far as i could see.

# Why React

I have developed before in react, so i'm decently familiar. I picked it for the ease of use with react being component-based and live-updating. It's also lighter, and closer to standard HTML than frameworks like angular, which makes it easier to adopt based on my previous experience.