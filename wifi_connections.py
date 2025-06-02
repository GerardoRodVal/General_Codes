import nmap

def scan_ports(ip):
    nmap_path = [r"C:\Program Files (x86)\Nmap\nmap.exe", ]
    nm = nmap.PortScanner(nmap_search_path=nmap_path)
    nm.scan(ip, '1-65535')  # Escanea todos los puertos
    for host in nm.all_hosts():
        print(f'Scan report for {host}')
        for proto in nm[host].all_protocols():
            print(f'Protocol : {proto}')
            lport = nm[host][proto].keys()
            for port in lport:
                print(f'Port : {port}\tState : {nm[host][proto][port]["state"]}')

ip_address = "187.190.132.25"
scan_ports(ip_address)
