from src.git.git_http import GitHttpClient

from src.utils.creds import get_tokens

from src.configs.config import bb_creds

git_http_client = GitHttpClient(bb_tokens=get_tokens(bb_creds))
