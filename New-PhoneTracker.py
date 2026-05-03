import time
import random
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def lookup_name(number):
    """
    Queries a real API to find the name associated with a phone number.
    (Replace the URL and headers with the actual endpoint of your chosen provider)
    """
    API_KEY = "your_actual_api_key_here"
    url = f"https://api.example-lookup-service.com/v1/lookup?phone={number}&apikey={API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Adjust the key path based on the API provider's JSON structure
            return data.get("name", "Name not found in registry")
        else:
            return "API Error (Invalid response)"
    except requests.exceptions.RequestException:
        return "Connection failed (API unavailable)"

def start_phone_tracer(target):
    print("\n[+] phoneTracer v2.2 - OSINT")
    print(f"[*] Target: {target}")
    print("[*] Initiating trace...\n")

    try:
        for step in ["Parsing number", "Fetching region", "Checking carrier", "Looking up name", "Finalizing"]:
            print(f"[*] {step}...")
            time.sleep(random.uniform(0.3, 0.8))

        parsed_number = phonenumbers.parse(target, None)

        if not phonenumbers.is_valid_number(parsed_number):
            print("[!] Invalid phone number.")
            return

        location = geocoder.description_for_number(parsed_number, "en")
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        # Real lookup execution
        name = lookup_name(target)

        print("\n[+] ===== Trace Results =====")
        print(f"[+] Location   : {location if location else 'Unknown'}")
        print(f"[+] Carrier    : {sim_carrier if sim_carrier else 'Unknown'}")
        print(f"[+] Time Zones : {', '.join(time_zones) if time_zones else 'Unknown'}")
        print(f"[+] Owner Name : {name}")
        print("[+] Status     : Number is valid")
        print("[+] =========================\n")

    except phonenumbers.NumberParseException:
        print("[!] Error: Could not parse the phone number. Check format.")
    except Exception as e:
        print(f"[!] Unexpected error: {e}")

    print("[+] Trace complete.\n")


if __name__ == "__main__":
    try:
        user_input = input("Enter phone number (with country code, e.g., +14155552671): ")
        start_phone_tracer(user_input)
    except KeyboardInterrupt:
        print("\n[!] Trace interrupted by user.")