"""
Nutanix Prism VM Stats
"""

import requests
import urllib3
import json
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from requests.auth import HTTPBasicAuth


def main():
    """
    main entry point into the 'app'
    every function needs a Docstring in order to follow best
    practices
    """
    # load the script configuration
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)
    PC_IP = os.getenv("PC_IP")
    PC_PORT = os.getenv("PC_PORT")
    PC_USERNAME = os.getenv("PC_USERNAME")
    PC_PASSWORD = os.getenv("PC_PASSWORD")
    CLUSTER_IP = os.getenv("CLUSTER_IP")
    CLUSTER_PORT = os.getenv("CLUSTER_PORT")
    CLUSTER_USERNAME = os.getenv("CLUSTER_USERNAME")
    CLUSTER_PASSWORD = os.getenv("CLUSTER_PASSWORD")

    print(f"Cluster IP: {CLUSTER_IP}")
    print(f"Cluster Port: {CLUSTER_PORT}")
    print(f"Prism Central IP: {PC_IP}")
    print(f"Prism Central Port: {PC_PORT}")

    """
    disable insecure connection warnings
    please be advised and aware of the implications of doing this
    in a production environment!
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup a variable that can be used to store our JSON configuration
    raw_json = {}

    # grab and decode the category details from the included JSON file
    with open("./config.json", "r") as f:
        raw_json = json.loads(f.read())

    # setup the request that will get the VM list
    print("\nGathering VM list ...")
    endpoint = f"https://{PC_IP}:{PC_PORT}/api/nutanix/v3/vms/list"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # this request body instructs the v3 API to return the first available VM only
    request_body = {"kind": "vm", "length": 1}

    # submit the request that will gather the VM list
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(PC_USERNAME, PC_PASSWORD),
        )

        # check the results of the request
        if results.status_code == 200 or results.status_code == 201:
            print("Request successful, grabbing first VM UUID and name ...")

        # grab the VM name and UUID
        vm_name = results.json()["entities"][0]["status"]["name"]
        vm_uuid = results.json()["entities"][0]["metadata"]["uuid"]

        print(f"VM Name: {vm_name}")
        print(f"VM UUID: {vm_uuid}")

        # now that we have the VM name and UUID, we can proceed with gathering stats for that VM
        # this must be done using the v1 REST API, meaning a new request is required

        # setup the request that will get the VM stats
        print("\nGathering VM stats ...")
        if raw_json["config"]["required_metrics"] == "":
            endpoint = (
                f"https://{CLUSTER_IP}:{CLUSTER_PORT}/api/nutanix/v1/vms/{vm_uuid}"
            )
        else:
            metrics = raw_json["config"]["required_metrics"]
            endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/api/nutanix/v1/vms/{vm_uuid}/stats/?metrics={metrics}"
        request_headers = {"Content-Type": "application/json", "charset": "utf-8"}

        results = requests.get(
            endpoint,
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        print("# STATS #")

        # check to see if the user asked for a specific metric only
        # if so, the request above requested that specific metric only,
        # and will contain a different response than
        # if the user asked for ALL stats
        if raw_json["config"]["required_metrics"] == "":
            for stat in results.json()["stats"]:
                print(f"{stat}: {results.json()['stats'][stat]}")
            print("# USAGE STATS #")
            for usage_stat in results.json()["usageStats"]:
                print(f"{usage_stat}: {results.json()['usageStats'][usage_stat]}")
        else:
            for stat in results.json()["statsSpecificResponses"]:
                print(f"{stat['metric']}: {stat['values'][0]}")
    except Exception as error:
        print(f"An unhandled exception has occurred: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
