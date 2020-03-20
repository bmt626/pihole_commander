###########################################
# Script to control pihole server
# By: Brandon Taylor
###########################################

# Disable pihole - http://pi.hole/admin/api.php?disable&auth=PWHASH
# Disable pihole for 5 minutes - http://pi.hole/admin/api.php?disable=300&auth=PWHASH
# Enable pihole - http://pi.hole/admin/api.php?enable&auth=PWHASH

import argparse
import json
import requests

# Take password hash from your install located in /etc/pihole/setupVars.conf - WEBPASSWORD
PWHASH = "REPLACE_THIS_WITH_YOUR_WEBPASSWORD"
url_base = "http://pi.hole/admin/api.php?"
url_auth = "&auth="
base_response = "Your pihole has been "

# Take result of the url get request parse the json that is returned to get the result status - either enabled or disabled
def parseResponse(url_response):
    parsed = json.loads(url_response)
    return parsed.get("status")

def pihole(command, time=None):
    if time != None:
        value = parseResponse(requests.get(
            url_base + command + "=" + str(time) + url_auth + PWHASH).content)
    else:
        value = parseResponse(requests.get(url_base + command + url_auth + PWHASH).content)
    print(base_response + value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='An app to control your pihole')
    parser.add_argument("-s", choices=["enable","disable"], required=True, type=str, help="-s is the status you want either enable or disable")
    parser.add_argument("-t",type=int, help="-t the time in minutes you want to disable your pihole for")
    
    args = parser.parse_args()
    if args.s == "enable":
        pihole(args.s)
    elif args.s =="disable":
        if args.t == None:
            pihole(args.s)
        else:
            time = int(args.t) * 60
            pihole(args.s, time=time)
