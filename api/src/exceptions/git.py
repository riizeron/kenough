class RepoCloneException(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return f"{type(self).__name__}. Unable to clone repo {self.url}"


class RefNotFoundError(Exception):
    def __init__(self, url, ref):
        self.url = url
        self.ref = ref

    def __str__(self):
        return f"{type(self).__name__}. Ref {self.ref} not found in repo {self.url}"