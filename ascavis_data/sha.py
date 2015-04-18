"""
Spitzer Heritage Archive queries

Usage:

First you have to query all observations for a given JPL number. You can then
download the spectrum for each observation.

>>> from ascavis_data import sha
>>> spitzer = sha.SpitzerHeritageArchive(httplib2.Http(".cache"))
>>> observations = sha.parse_table(spitzer.query_by_jpl(253))
>>> spectra = map(
...     lambda obs: sha.parse_table(spitzer.download_spectrum(obs)),
...     filter(sha.is_spectrum, observations)
... )

"""

import httplib2


DATA_SERVICE_URL = "http://sha.ipac.caltech.edu/applications/Spitzer/SHA/servlet/DataService"
DATASET = "ivo://irsa.ipac/spitzer.level2"


def parse_table(content):
    lines = content.split("\n")
    headers_line = 0
    while lines[headers_line][0] != "|":
        headers_line += 1
    k, entries = 0, []
    for entry in lines[headers_line].split("|")[1:]:
        if entry != "":
            entries.append([entry.strip(), k, len(entry) + 1 + k])
        k += len(entry) + 1
    return [
        {name: line[a:b].strip() for name, a, b in entries}
        for line in lines[headers_line + 4:]
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
        _header, content = self.http_backend.request(data_query, "GET")
        return content

    def download_spectrum(self, observation):
        _header, content = self.http_backend.request(observation["accessUrl"], "GET")
        return content
