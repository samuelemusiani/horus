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
            if scanner[host].state() == 'up':
                host_entry = {
                    'ip': host,
                    'hostname': scanner[host].hostname() or 'unknown',
                    'state': 'up',
                    'scan_time': datetime.now().isoformat(),
                    'vulnerabilities': [],
                    'open_ports': [],
                    'vuln_scan_completed': False,
                    'host_scripts': []
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
        host_entry = next((host for host in hosts if host['ip'] == target), None)
        
        if not host_entry:
            print(f"[!] Host {target} not found in scanned hosts list")
            return
        
        # Update scan information
        if target in scanner.all_hosts():
            host_data = scanner[target]
            
            # Reset vulnerability and port lists
            host_entry['vulnerabilities'] = []
            host_entry['open_ports'] = []
            host_entry['vuln_scan_completed'] = True
            host_entry['last_vuln_scan'] = datetime.now().isoformat()
            
            # Collect port and vulnerability information
            for proto in host_data.all_protocols():
                for port in host_data[proto].keys():
                    port_data = host_data[proto][port]
                    
                    # Store port information
                    port_info = {
                        'port': port,
                        'protocol': proto,
                        'state': port_data.get('state', 'unknown'),
                        'service': port_data.get('name', 'unknown'),
                        'version': port_data.get('version', 'unknown')
                    }
                    host_entry['open_ports'].append(port_info)
                    
                    # Store vulnerability information from port scripts
                    if 'script' in port_data:
                        for script_name, output in port_data['script'].items():
                            vuln_info = {
                                'type': 'port_script',
                                'port': port,
                                'script_name': script_name,
                                'output': output
                            }
                            host_entry['vulnerabilities'].append(vuln_info)
            
            # Store host script results
            if hasattr(scanner[target], 'hostscript'):
                for script_result in scanner[target].hostscript():
                    host_script = {
                        'id': script_result['id'],
                        'output': script_result['output']
                    }
                    host_entry['host_scripts'].append(host_script)
            
            # Print summary
            print(f"\n[+] Vulnerability scan completed for {target}")
            print(f"[+] Found {len(host_entry['vulnerabilities'])} vulnerability indicators")
            print(f"[+] Found {len(host_entry['open_ports'])} open ports")
            
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Network Scanner and Vulnerability Assessment')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Network scan parser
    network_parser = subparsers.add_parser('network', help='Perform fast network scan')
    network_parser.add_argument('network', help='Network address (e.g., 192.168.1.0/24)')
    
    # Vulnerability scan parser
    vuln_parser = subparsers.add_parser('vuln', help='Perform vulnerability scan')
    vuln_parser.add_argument('target', help='Target IP or hostname')
    vuln_parser.add_argument('-p', '--ports', help='Port specification (default: common ports)')
    
    # Save results parser
    save_parser = subparsers.add_parser('save', help='Save results to file')
    save_parser.add_argument('filename', help='File to save results to')
    
    # Load results parser
    load_parser = subparsers.add_parser('load', help='Load results from file')
    load_parser.add_argument('filename', help='File to load results from')
    
    args = parser.parse_args()
    
    if args.command == 'network':
        fast_network_scan(args.network)
    elif args.command == 'vuln':
        run_vuln_scan(args.target, args.ports)
    elif args.command == 'save':
        save_results(args.filename)
    elif args.command == 'load':
        load_results(args.filename)
    else:
        parser.print_help()
