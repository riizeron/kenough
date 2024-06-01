import logging

from src.dataclasses.creds import BBCred

logger = logging.getLogger(__name__)


def read_creds(creds: dict[str, str]) -> dict[str, str]:
    creds_dict: dict[str, str] = dict()
    for key, path_to_cred in creds.items():
        with open(path_to_cred) as f:
            creds_dict[key] = f.read().strip()

    return creds_dict


def get_tokens(creds_config: dict[str, str]) -> dict[str, BBCred]:

    bb_creds: dict[str, BBCred] = dict()

    usernames: dict[str, str] = dict()
    tokens: dict[str, str] = dict()
    username_prefix = "username-"
    token_prefix = "token-"

    for key, cred in read_creds(creds_config).items():
        if key.startswith(username_prefix):
            usernames[key.removeprefix(username_prefix)] = cred
        elif key.startswith(token_prefix):
            tokens[key.removeprefix(token_prefix)] = cred

    for key in usernames:
        bb_creds[key] = BBCred(username=usernames[key], token=tokens[key])

    logger.info(f"CREDS INJECTED: {bb_creds.keys()}")

    return bb_creds
