# Description: 
# This script is a Python-based tool that analyzes a forensic image of a Windows machine to identify potential cyber attacks and create a profile of the attacker.

# What it does: 
# The script mounts the forensic image, extracts metadata from files, scans for malware, and looks up file hashes on various threat intelligence platforms. 
# It also searches for identity indicators in the file system and creates a comprehensive report of the attacker's profile.

# How it works:
# The script mounts the forensic image using Autopsy.
# It extracts metadata from files, including PE files, and scans for malware using VirusTotal, OTX, Malwarebytes, and Hybrid Analysis.
# It looks up file hashes on various threat intelligence platforms to gather more information about the malware.
# It searches for identity indicators in the file system, such as email addresses, usernames, and passwords.
# The script creates a comprehensive report of the attacker's profile, including malware, IP addresses, domains, usernames, and identity indicators.
# The report is generated in a text file labeled "ForensicScanResults.txt".

# NOTICE 
# This script is in active development and will see many changes, additives, and errors.

# Developed By
# Adam Rivers of Hello Security LLC

import os
import json
import requests
from pyew import Autopsy
import hashlib
import re
from collections import defaultdict

# Set up Autopsy
autopsy = Autopsy()

# Set up API keys
vt_api_key = "YOUR_VIRUSTOTAL_API_KEY"
otx_api_key = "YOUR_OTX_API_KEY"
malwarebytes_api_key = "YOUR_MALWAREBYTES_API_KEY"
hybrid_analysis_api_key = "YOUR_HYBRID_ANALYSIS_API_KEY"
# Add more API keys as needed

# Define the functions to interact with each service
def vt_scan(file_path):
    params = {"apikey": vt_api_key, "file": file_path}
    response = requests.post("https://www.virustotal.com/vtapi/v2/file/scan", params=params)
    return response.json()

def otx_lookup(hash):
    params = {"apikey": otx_api_key, "hash": hash}
    response = requests.get("https://otx.alienvault.com/api/v1/indicators/file/" + hash, params=params)
    return response.json()

def malwarebytes_lookup(hash):
    params = {"apikey": malwarebytes_api_key, "hash": hash}
    response = requests.get("https://api.malwarebytes.com/v1/lookup/" + hash, params=params)
    return response.json()

def hybrid_analysis_lookup(hash):
    params = {"apikey": hybrid_analysis_api_key, "hash": hash}
    response = requests.get("https://www.hybrid-analysis.com/api/v2/lookup/" + hash, params=params)
    return response.json()

def analyze_pe_file(file_path):
    # Use pyew to extract PE file metadata
    pe_file = autopsy.get_pe_file(file_path)
    file_info = pe_file.get_file_info()
    return file_info

def extract_strings(file_path):
    # Use pyew to extract strings from the file
    strings = autopsy.extract_strings(file_path)
    return strings

def calculate_entropy(file_path):
    # Calculate the entropy of the file
    with open(file_path, "rb") as f:
        data = f.read()
    entropy = hashlib.sha256(data).hexdigest()
    return entropy

def search_for_identity_indicators(file_system):
    # Search for identity indicators in the file system
    identity_indicators = []
    for file in file_system.get_files():
        file_path = file.get_path()
        if file.get_type() == "TEXT":
            with open(file_path, "r") as f:
                content = f.read()
                if re.search(r"\b(email|username|password|name|address|phone)\b", content):
                    identity_indicators.append({"type": "text_file", "value": content})
    return identity_indicators

def create_attacker_profile(evidence):
    # Create a profile of the attacker based on the evidence
    profile = defaultdict(list)
    for item in evidence:
        if item["type"] == "malware":
            profile["malware"].append(item["name"])
        elif item["type"] == "ip_address":
            profile["ip_addresses"].append(item["value"])
        elif item["type"] == "domain":
            profile["domains"].append(item["value"])
        elif item["type"] == "username":
            profile["usernames"].append(item["value"])
        elif item["type"] == "command":
            profile["commands"].append(item["value"])
        elif item["type"] == "identity_indicator":
            profile["identity_indicators"].append(item["value"])
    return profile

def generate_report(profile, report_file):
    # Generate a report based on the attacker profile
    with open(report_file, "w") as f:
        f.write("Attacker Profile:\n")
        f.write("==============\n")
        for key, value in profile.items():
            f.write(f"{key.capitalize()}: {', '.join(value)}\n")
        f.write("\n")

# Define the main function to process the forensic image
def process_forensic_image(image_path):
    # Mount the forensic image using Autopsy
    autopsy.mount_image(image_path)

    # Get the file system metadata
    file_system = autopsy.get_file_system()

    # Initialize the evidence list
    evidence = []

    # Iterate through the files and directories
    for file in file_system.get_files():
        # Get the file path and hash
        file_path = file.get_path()
        file_hash = file.get_md5()

        # Check if the file is a PE file (Windows executable)
        if file.get_type() == "PE":
            # Analyze the PE file
            file_info = analyze_pe_file(file_path)
            evidence.append({"type": "pe_file", "name": file_info["name"], "version": file_info["version"]})

            # Extract strings from the file
            strings = extract_strings(file_path)
            for string in strings:
                evidence.append({"type": "string", "value": string})

            # Calculate the entropy of the file
            entropy = calculate_entropy(file_path)
            evidence.append({"type": "entropy", "value": entropy})

            # Scan the file with VirusTotal
            vt_response = vt_scan(file_path)
            if vt_response["response_code"] == 1:
                evidence.append({"type": "malware", "name": vt_response["scans"]["positives"]})

            # Lookup the file hash on OTX
            otx_response = otx_lookup(file_hash)
            if otx_response["status"] == "success":
                evidence.append({"type": "otx", "value": otx_response["pulse_info"]})

            # Lookup the file hash on Malwarebytes
            mb_response = malwarebytes_lookup(file_hash)
            if mb_response["status"] == "success":
                evidence.append({"type": "malwarebytes", "value": mb_response["detection"]})

            # Lookup the file hash on Hybrid Analysis
            ha_response = hybrid_analysis_lookup(file_hash)
            if ha_response["status"] == "success":
                evidence.append({"type": "hybrid_analysis", "value": ha_response["verdict"]})

    # Search for identity indicators in the file system
    identity_indicators = search_for_identity_indicators(file_system)
    for indicator in identity_indicators:
        evidence.append({"type": "identity_indicator", "value": indicator["value"]})

    # Unmount the forensic image
    autopsy.unmount_image()

    # Create a profile of the attacker based on the evidence
    attacker_profile = create_attacker_profile(evidence)

    # Generate a report based on the attacker profile
    report_file = "ForensicScanResults.txt"
    generate_report(attacker_profile, report_file)

    # Print the report
    print("Report generated:", report_file)

# Example usage
image_path = "/path/to/forensic/image.E01"
process_forensic_image(image_path)
