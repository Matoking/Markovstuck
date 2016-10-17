from django.conf import settings

import os


def save_chain(name, chain_json):
    """Save a Markov chain as a JSON file for later loading"""
    chain_dir = os.path.join(settings.BASE_DIR, "chains")

    # Create the chain directory if it doesn't exist
    if not os.path.isdir(chain_dir):
        os.makedirs(chain_dir)

    path = os.path.join(
        settings.BASE_DIR,
        "chains",
        "%s.json" % name)

    f = open(path, 'w')
    f.write(chain_json)
    f.close()

    return True
