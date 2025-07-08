import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
import ssl
import socket
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)


def banner():
    print('\n')
    print(Fore.LIGHTGREEN_EX + '         ████████╗██████╗  █████╗  ██████╗███████╗')
    print(Fore.LIGHTGREEN_EX + '         ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝')
    print(Fore.LIGHTGREEN_EX + '██╗   ██╗   ██║   ██████╔╝███████║██║     █████╗  ')
    print(Fore.LIGHTGREEN_EX + '██║   ██║   ██║   ██╔══██╗██╔══██║██║     ██╔══╝  ')
    print(Fore.LIGHTGREEN_EX + '╚██████╔╝   ██║   ██║  ██║██║  ██║╚██████╗███████╗')
    print(Fore.LIGHTGREEN_EX + ' ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝')
    print(Fore.CYAN + "🔗 Advanced URL Redirect Checker 🔗" + Fore.LIGHTGREEN_EX + Style.BRIGHT + '    By Abinav')
    print('\n')
    
def help():
    about = '''\nThis project is a terminal-based tool that checks how a given website URL behaves when accessed. It helps users understand if the website redirects to other locations, how many redirections occur, and what the final destination is. The tool also verifies whether the final URL uses HTTPS and whether it has a valid SSL certificate, which ensures a secure connection. In addition, it displays key technical details like the time it takes to respond. Users can check a single URL or process multiple URLs from a file in batch mode. This tool is especially useful for developers, testers, and network administrators who want to verify website behavior, security, and performance in a quick and readable way.\n'''
    print(about)
    print(Fore.LIGHTYELLOW_EX+"\nREQUIREMENTS:")
    print(Fore.LIGHTYELLOW_EX+" - Python3")
    print(Fore.LIGHTYELLOW_EX+" - Install required libraries:")
    print(Fore.LIGHTYELLOW_EX+"     pip install colorama")
    print(Fore.LIGHTYELLOW_EX+"     pip install requests")
    print(Fore.LIGHTYELLOW_EX+' - Run the tool: uTrace.py')
    print(Fore.LIGHTRED_EX+'\nCoded by: ABINAV\n')
    
def parse_url(url):
    parsed = urlparse(url)
    return {
        "scheme":parsed.scheme,
        "netloc":parsed.netloc,
        "path":parsed.path,
        "query":parsed.query
    }
    
def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expires = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                return {
                    "valid": True,
                    "issuer": cert.get("issuer"),
                    "expires": expires.strftime("%Y-%m-%d")
                }
    except Exception:
        return {"valid": False}
    
def check_redirects(url):
    try:
        response = requests.get(url,allow_redirects=True,timeout=10)
        history = response.history
        
        print(Fore.CYAN + f"\nURL: {url}")
        
        url_info = parse_url(response.url)
        print(f"📎 Domain: {url_info['netloc']}")
        print(f"🔗 Scheme: {url_info['scheme']}")
        print(f"📁 Path: {url_info['path']}")
        print(Fore.CYAN + f"🔍 Final URL: {response.url}")
        
        is_https = response.url.startswith("https://")
        print("🔒 HTTPS: " + (Fore.GREEN + "Yes" if is_https else Fore.RED + "No"))
        
        #SSL check
        ssl_status = check_ssl(url_info["netloc"])
        if ssl_status["valid"]:
            print(Fore.GREEN + f"🛡️ SSL Certificate valid (expires {ssl_status['expires']})")
        else:
            print(Fore.RED + "⚠️ SSL Certificate not valid or not available")

        if history:
            print(f"\n🔁 Redirected {len(history)} times:")
            for i, resp in enumerate(history):
                print(Fore.YELLOW + f" {i+1}. {resp.status_code} → {resp.url} ({resp.elapsed.total_seconds()}s)")
        else:
            print(Fore.GREEN + "\n✅ No redirection occurred.")

        print(Fore.MAGENTA + f"\n⏱️ Final response time: {response.elapsed.total_seconds()}s")
        print("\n")
        
    except RequestException as e:
        print(Fore.RED+f"\n❌ Request failed: {e}")

# def batch_mode(file_path):
#     print("\n📦 Batch mode: Reading URLs from file...\n")
#     with open(file_path, 'r') as f:
#         urls = [line.strip() for line in f.readlines() if line.strip()]
        
#     for url in urls:
#         check_redirects(url)

def batch_mode(file_path):
    print("\n📦 Batch mode: Reading URLs from file...\n")
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"❌ File not found: {file_path}")
        return
    except Exception as e:
        print(Fore.RED + f"❌ Failed to read file: {e}")
        return

    for url in urls:
        result = check_redirects(url)
        print("------------------------------")

    print(Fore.GREEN + "\n✅ Batch checking complete.")


def main():
    banner()
    print(Fore.LIGHTGREEN_EX+'['+Fore.RESET+'1'+Fore.LIGHTGREEN_EX+']' +Fore.CYAN+' --Check a single URL')
    print(Fore.LIGHTGREEN_EX+'['+Fore.RESET+'2'+Fore.LIGHTGREEN_EX+']' +Fore.CYAN+' --Check a batch of URLs from a file')
    print(Fore.LIGHTGREEN_EX+'['+Fore.RESET+'3'+Fore.LIGHTGREEN_EX+']' +Fore.CYAN+' --help')
    #print("[2] Check a single URL")
    #print("[3] Check a batch of URLs from a file\n")
    choice = input('\n'+ Fore.LIGHTGREEN_EX +'Select an option (1/2/3) : '+Fore.RESET).strip()
    if choice == '1':
        url = input("\nEnter a URL : ").strip()
        check_redirects(url)
    elif choice == '2':
        file_path = input("Enter path to file with URLs: ").strip()
        batch_mode(file_path)
    elif choice == '3':
        help()

if __name__ == "__main__":
    main()