from abc import ABC, abstractmethod
from cloudmesh.common2.compute import CloudmeshComputeABC
from cloudmesh.common.FlatDict import FlatDict

class CloudmeshComputeABC(ABC):

    @abstractmethod
    def authenticate(self):
        raise NotImplementedError("Subclasses must implement authenticate()")

    def load_config(self, filename=None, name=None):
        raise NotImplementedError("Subclasses must implement upload()")

    @abstractmethod
    def upload(self, local_path, remote_path):
        raise NotImplementedError("Subclasses must implement upload()")

    @abstractmethod
    def download(self, remote_path, local_path):
        raise NotImplementedError("Subclasses must implement download()")

    @abstractmethod
    def run(self, command):
        raise NotImplementedError("Subclasses must implement run()")

    @abstractmethod
    def status(self, job_id):
        raise NotImplementedError("Subclasses must implement status()")

    @abstractmethod
    def stderr(self, job_id):
        raise NotImplementedError("Subclasses must implement stderr()")

    @abstractmethod
    def stdout(self, job_id):
        raise NotImplementedError("Subclasses must implement stdout()")

    @abstractmethod
    def start(self, job_id):
        raise NotImplementedError("Subclasses must implement start()")

    @abstractmethod
    def stop(self, job_id):
        raise NotImplementedError("Subclasses must implement stop()")

    @abstractmethod
    def resume(self, job_id):
        raise NotImplementedError("Subclasses must implement resume()")


if __name__ == "__main__":
    # Example usage
    compute = GoogleColabCompute()

    compute.authenticate()
    compute.upload("local_file.txt", "remote_file.txt")
    compute.run("python script.py")
    # ... other method calls ...
