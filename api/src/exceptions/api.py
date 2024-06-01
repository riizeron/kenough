from fastapi import HTTPException

from src.api.models.source import Repo

class ModelValidationException(Exception):
    status_code = 400

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}. {self.message}"


class ArtifactNetworkException(Exception):
    status_code = 500


class ArtifactAccessDeniedException(Exception):
    status_code = 403


class ArtifactNotFoundException(Exception):
    status_code = 404


class RepositoryAccessDeniedException(ArtifactAccessDeniedException):
    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    def __str__(self):
        return f"{type(self).__name__}. Unable to access repository: {self.repo_url}"


class RepositoryNotFoundException(ArtifactNotFoundException):
    def __init__(self, repo_url: str):
        self.repo_url = repo_url

    def __str__(self):
        return f"{type(self).__name__}. Repository {self.repo_url} was not found"


class RefNotFoundException(ArtifactNotFoundException):
    def __init__(self, repo_url, repo_ref):
        self.repo_url = repo_url
        self.repo_ref = repo_ref

    def __str__(self):
        return f"{type(self).__name__}. Ref {self.repo_ref} was not found in repo {self.repo_url}"


class RepositoryNetworkException(ArtifactNetworkException):
    def __init__(self, repo_url):
        self.repo_url = repo_url

    def __str__(self):
        return f"{type(self).__name__}. No Network access to repository {self.repo_url}"


class ScannersException(Exception):
    status_code = 501


class ImpossibleScannerException(ScannersException):
    def __init__(self, scanners: list[str], artifact):
        self.scanners = scanners
        self.artifact = artifact

    def __str__(self):
        return f"{type(self).__name__}. Scanners: {self.scanners} is not applicable for artifact: {self.artifact}"


class ApplicableScannersNotFoundException(ScannersException):
    def __init__(self, artifact):
        self.artifact = artifact

    def __str__(self):
        return f"{type(self).__name__}. Not found applicable scanners for artifact: {self.artifact}"


class AnalyzerException(Exception):
    status_code = 500


# TODO: NEED HANDLERS
class RepoAnalyzerException(AnalyzerException):
    def __init__(self, repo: Repo):
        self.repo = repo

    def __str__(self):
        return f"{type(self).__name__}. Unable to analyze repo: {self.repo}"


class DistribAnalyzerException(AnalyzerException):
    def __init__(self, distrib_url: str):
        self.distrib_url = distrib_url

    def __str__(self):
        return f"{type(self).__name__}. Unable to analyze distrib: {self.distrib_url}"


class SbomAnalyzerException(AnalyzerException):
    def __init__(self, sha256: str):
        self.sha256 = sha256

    def __str__(self):
        return f"{type(self).__name__}. Unable to analyze sbom: {self.sha256}"


class UrlAccessException(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 403

    def __str__(self):
        return f"UrlAccessException. {self.message}"


class BadAddress(Exception):
    def __init__(self, message):
        self.message = message


class FileException(Exception):
    def __init__(self, message):
        self.message = message


class LaunchTaskException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"LaunchTaskException. {self.message}"


class RuinScanException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RuinScanException. {self.message}"


class WrongClient(Exception):
    def __init__(self, subject_name: str, **kwargs):
        self.kwargs = kwargs
        self.subject_name = subject_name
        self.status_code = 403

    def __str__(self):
        return "WrongClient. Forbidden request for report"


