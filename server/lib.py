import nmap
import argparse
from datetime import datetime
import ipaddress
from typing import List, Dict
import json

# Global variable to store host information
hosts: List[Dict] = []

def fast_network_scan(network: str) -> None:
    """
    Perform a fast ping sweep of the network and store results in global hosts variable
    
    Args:
        network (str): Network address in CIDR notation (e.g., '192.168.1.0/24')
    """
    try:
        # Validate network address format
        ipaddress.ip_network(network)
        
        # Initialize scanner
        scanner = nmap.PortScanner()
        
        print(f"[*] Starting fast network scan of {network} at {datetime.now()}")
        print("[*] Performing ping sweep...")
        
        # -sn: Ping scan
        # -n: No DNS resolution
        # -T4: Aggressive timing template
        scanner.scan(hosts=network, arguments='-sn -n -T4')
        
        # Clear global hosts list before new scan
        global hosts
        hosts.clear()
        
        # Initialize host entries
        for host in scanner.all_hosts():
            print("host: ", host)
            if scanner[host].state() == 'up':
                host_entry = {
                    'ip': host,
                    'name': scanner[host].hostname() or 'unknown',
                    'mac': scanner[host]['addresses']['mac'] or 'unknown',
                    'scan_time': datetime.now().isoformat(),
                    'services': [],
                }
                hosts.append(host_entry)
                
        # Print results
        print(f"\n[+] Scan completed at {datetime.now()}")
        print(f"[+] Found {len(hosts)} active hosts")
        
        for host in hosts:
            print(f"Host: {host['ip']} ({host['hostname']})")
                
    except Exception as e:
        print(f"[!] An error occurred during network scan: {str(e)}")

def run_vuln_scan(target: str, ports: str = None) -> None:
    """
    Run vulnerability scan against specified target and update global hosts array
    
    Args:
        target (str): Target IP or hostname
        ports (str): Port specification (default: common ports)
    """
    try:
        # Initialize scanner
        scanner = nmap.PortScanner()
        
        # Convert localhost to IP if needed
        if target.lower() in ['localhost', 'local']:
            target = '127.0.0.1'
            
        # Build scan arguments
        arguments = '-sV --script vuln'
        if ports:
            arguments += f' -p{ports}'
            
        print(f"[*] Starting vulnerability scan of {target} at {datetime.now()}")
        print("[*] This may take several minutes...")
        
        # Run the scan
        scanner.scan(target, arguments=arguments)
        
        # Find the host entry in our global hosts list
        global hosts
        host_index = next((index for index, host in enumerate(hosts) if host['ip'] == target), None)
        
        if host_index is None:
            print(f"[!] Host {target} not found in scanned hosts list")
            return
        
        # Update scan information
        if target in scanner.all_hosts():
            host_data = scanner[target]
            
            # Create new services list for this scan
            new_services = []
            
            # Collect port and vulnerability information
            for proto in host_data.all_protocols():
                for port in host_data[proto].keys():
                    port_data = host_data[proto][port]
                    
                    # Store vulnerability information from port scripts
                    if 'script' in port_data:
                        for script_name, output in port_data['script'].items():
                            vuln_info = {
                                'port': port,
                                'state': port_data.get('state', 'unknown'),
                                'name': port_data.get('name', 'unknown'),
                                'version': port_data.get('version', 'unknown'),
                                'script_name': script_name,
                                'output': output,
                                'ifVulnerable': output.find('EXPLOIT') != -1
                            }
                            new_services.append(vuln_info)
            
            # Update the host entry with new services
            print(new_services)
            hosts[host_index]['services'] = new_services
            print(hosts)
            hosts[host_index]['scan_time'] = datetime.now().isoformat()
            
            # Print summary
            print(f"\n[+] Vulnerability scan completed for {target}")
            print(f"[+] Found {len(new_services)} services with potential vulnerabilities")
            
        else:
            print(f"[!] No scan data found for host {target}")
            
    except Exception as e:
        print(f"[!] An error occurred during vulnerability scan: {str(e)}")

def save_results(filename: str) -> None:
    """
    Save the current scan results to a JSON file
    
    Args:
        filename (str): Name of the file to save results to
    """
    try:
        with open(filename, 'w') as f:
            json.dump(hosts, f, indent=4)
        print(f"[+] Results saved to {filename}")
    except Exception as e:
        print(f"[!] Error saving results: {str(e)}")

def load_results(filename: str) -> None:
    """
    Load scan results from a JSON file
    
    Args:
        filename (str): Name of the file to load results from
    """
    try:
        global hosts
        with open(filename, 'r') as f:
            hosts = json.load(f)
        print(f"[+] Loaded {len(hosts)} hosts from {filename}")
    except Exception as e:
        print(f"[!] Error loading results: {str(e)}")

def get_hosts() -> List[Dict]:
    """
    Get the current list of hosts
    
    Returns:
        List[Dict]: List of host dictionaries
    """
    return hosts
