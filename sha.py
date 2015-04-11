"""
Spitzer Heritage Archive queries

"""

import httplib2
import StringIO


DATA_SERVICE_URL = "http://sha.ipac.caltech.edu/applications/Spitzer/SHA/servlet/DataService"
DATASET = "ivo://irsa.ipac/spitzer.level2"


def parse_asteroid_obs(content):
    lines = content.split("\n")
    k, entries = 0, []
    for entry in lines[0].split("|")[1:]:
        entries.append([entry.strip(), k, len(entry) + 1 + k])
        k += len(entry) + 1
    return [
        {name: line[a:b].strip() for name, a, b in entries}
        for line in lines[4:]
    ]


def is_spectrum(observation):
    return (
        observation["filetype"] == "Table"
        and (
            "Spectrum" in observation["ptcomment"] or
            "spectrum" in observation["ptcomment"]
        )
    )


class SpitzerHeritageArchive(object):

    def __init__(self, http_backend):
        self.http_backend = http_backend

    def query_by_jpl(self, jpl_number):
        # Convert JPL number to NAIF ID
        naif_id = 2000000 + jpl_number
        # Query the SHA data service
        data_query = (DATA_SERVICE_URL + "?NAIFID={}&VERB=3&DATASET=" + DATASET
            ).format(naif_id)
        return self.http_backend.request(data_query, "GET")
