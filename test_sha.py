from sha import *

def test_simple_query():
    sha = SpitzerHeritageArchive(httplib2.Http(".cache"))
    _, content = sha.query_by_jpl(253)
    observations = parse_asteroid_obs(content)
    assert len(observations) == 19
    assert len(filter(is_spectrum, observations)) == 8
