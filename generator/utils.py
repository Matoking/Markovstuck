from django.conf import settings

import os.path


def save_chain(name, chain_json):
    """Save a Markov chain as a JSON file for later loading"""
    path = os.path.join(
        settings.BASE_DIR,
        "chains",
        "%s.json" % name)

    f = open(path, 'w')
    f.write(chain_json)
    f.close()

    return True
