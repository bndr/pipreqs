"""
Environment variables can be used as a first choice
$ set CA_BUNDLE="certificates.pem"     # for win OS
$ export CA_BUNDLE="certificates.pem"  # for nix OS

If environment variables are not found then a second attempt
will be made by loading the values from a .env.test file in
the same directory

See ./env.test.example for details.
"""

import importlib
import os
from pathlib import Path

CA_BUNDLE = os.environ.get("CA_BUNDLE")

if CA_BUNDLE is None and importlib.find_loader("dotenv"):
    # optional loading of values from .env.test file
    import dotenv

    env_test_path = Path(os.path.dirname(__file__) + "/.env.test")
    config = dotenv.dotenv_values(env_test_path)

    if config is not None:
        CA_BUNDLE = config["CA_BUNDLE"]
elif CA_BUNDLE is not None:
    CA_BUNDLE = str(Path(CA_BUNDLE))
