# This Helper file makes API calls
import os
from dotenv import load_dotenv
from sodapy import Socrata
import pandas as pd
load_dotenv()


def do_callout(identifier: str, select: str, where: str) -> pd.DataFrame:
    return pd.DataFrame.from_dict(do_callout_return_raw(identifier, select, where))


def do_callout_return_raw(identifier: str, select: str, where: str):
    socrata_domain = 'data.transportation.gov'
    socrata_dataset_identifier = identifier
    socrata_token = os.environ.get('APP_PUBLIC')
    client = Socrata(socrata_domain, socrata_token)

    return client.get(socrata_dataset_identifier, select=select, where=where)
