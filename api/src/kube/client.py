import kubernetes


class KubeClient:
    def __init__(self):
        kubernetes.config.load_incluster_config()
        self.client = kubernetes.client.ApiClient()

    def create_from_dict(self, value):
        kubernetes.utils.create_from_dict(self.client, value)