# Basic-Port-Scanner

- Scans the given IP address for open ports, using 80 active threads at a time. Should take around 3 minutes for a full scan.

#Usage

- `python3 scanner.py ip_address ports`
- e.g. 	`scanner.py 10.10.10.10 all`
- e.g. 	`scanner.py 10.10.10.10 1-1024`
- port ranges are inclusive, and have to be between 1-65536