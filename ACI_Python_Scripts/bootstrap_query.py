# Import the required libraries
import requests
import json
import getpass
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def authenticate(apic_ip_hostname, username, password):
    """
    Authenticate to the APIC and return the authentication token
    """
    url = f"https://{apic_ip_hostname}/api/aaaLogin.json"
    headers = {"Content-Type": "application/json"}
    payload = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": password
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False, timeout=10)
        response.raise_for_status()
        token = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
        return token
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Incorrect username or password.")
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectTimeout:
        print(f"Connection to {apic_ip_hostname} timed out. The APIC might be unreachable.")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except KeyError:
        print("Authentication failed: Invalid credentials or response format.")
    return None

def make_api_call(apic_ip_hostname, token):
    """
    Make the API call to the APIC to query the bootstrap information
    """
    url = f"https://{apic_ip_hostname}/api/workflows/v1/cluster/bootstrap"
    cookies = {"APIC-cookie": token}
    
    try:
        response = requests.get(url, cookies=cookies, verify=False, timeout=10)
        response.raise_for_status()
        print(json.dumps(response.json(), indent=4))
    except requests.exceptions.HTTPError as http_err:
        print(f"API call failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")

def main():
    """
    Main function to authenticate to the APIC and make the API call
    """
    while True:
        apic_ip_hostname = input("Enter APIC IP or URL: ").strip()
        if not apic_ip_hostname:
            print("APIC IP or URL cannot be empty. Please try again.")
            continue

        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue

        password = getpass.getpass("Enter password: ").strip()
        if not password:
            print("Password cannot be empty. Please try again.")
            continue

        token = authenticate(apic_ip_hostname, username, password)
        if token:
            while True:
                make_api_call(apic_ip_hostname, token)
                
                while True:
                    another_call = input("Do you want to make the same API call to the same APIC? (y/n): ").strip().lower()
                    if another_call == "y":
                        break
                    elif another_call == "n":
                        break
                    else:
                        print("Only y or n is accepted as input.")
                        continue
                if another_call == "n":
                    break

        while True:
            another_apic = input("Do you want to make the same API call to a different APIC? (y/n): ").strip().lower()
            if another_apic == "y":
                break
            elif another_apic == "n":
                return
            else:
                print("Only y or n is accepted as input.")

if __name__ == "__main__":
    main()
