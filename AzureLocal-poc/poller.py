from helpers.auth import get_auth_headers
from helpers.checkDeprovisions import check_deprovisions
from urllib.parse import urlparse
import json
import requests
from config.database import get_connection
import uuid
from datetime import datetime, UTC

from helpers.checkJobs import check_jobs

def run_poller():

    get_jobs = check_jobs()
    get_deprovisions = check_deprovisions()
    print("Poller Cycle Completed!")


if __name__ == "__main__":
    run_poller()