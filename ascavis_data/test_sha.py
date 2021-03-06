from sha import *

def test_simple_query():
    sha = SpitzerHeritageArchive(httplib2.Http(".cache"))
    observations = parse_table(sha.query_by_jpl(253))
    assert len(observations) == 19
    assert len(filter(is_spectrum, observations)) == 8


def test_spectrum():
    sha = SpitzerHeritageArchive(httplib2.Http(".cache"))
    observations = parse_table(sha.query_by_jpl(253))
    spectrum = parse_table(
        sha.download_spectrum(filter(is_spectrum, observations)[0])
    )
    assert len(spectrum) == 103
    for datum in spectrum:
        for attr in ["order", "wavelength", "flux_density", "error", "bit-flag"]:
            assert attr in datum
