import importlib
import os

CA_BUNDLE = os.environ.get("CA_BUNDLE")

if CA_BUNDLE is None and importlib.find_loader("dotenv"):
    # optional loading of values from .env.test file
    from pathlib import Path

    import dotenv

    env_test_path = Path(os.path.dirname(__file__) + "/.env.test")
    config = dotenv.dotenv_values(env_test_path)

    if config is not None:
        CA_BUNDLE = config["CA_BUNDLE"]
