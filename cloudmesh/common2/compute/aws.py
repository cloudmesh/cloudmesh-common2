import boto3
from cloudmesh.common.FlatDict import FlatDict

class AWSCompute(CloudmeshComputeABC):

    def __init__(self,
                 access_key=None,
                 secret_key=None,
                 region=None,
                 instance_id=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.instance_id = instance_id

    def load_config(self, filename=None, name="aws"):
        self.config = FlatDict()
        self.load_config(filename=filename)
        self.access_key = self.config[f"{name}.access_key"]
        self.secret_key = self.config[f"{name}.secret_key"]

    def authenticate(self):
        self.ec2_client = boto3.client(
            'ec2',
            region_name=self.region,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )

    def upload(self, local_path, remote_path):
        # Implement file upload to AWS instance
        pass

    def download(self, remote_path, local_path):
        # Implement file download from AWS instance
        pass

    def run(self, command):
        # Implement running a command on AWS instance
        pass



    def start(self):
        self.ec2.start_instances(InstanceIds=[self.instance_id])
        print(f"Started instance {self.instance_id}")

    def stop(self):
        self.ec2.stop_instances(InstanceIds=[self.instance_id])
        print(f"Stopped instance {self.instance_id}")

if __name__ == "__main__":
    # Example usage for AWSCompute
    region = "us-east-1"
    access_key = "your_access_key"
    secret_key = "your_secret_key"
    instance_id = "your_instance_id"

    compute = AWSCompute(region, access_key, secret_key, instance_id)

    compute.authenticate()
    compute.start_instance()
    compute.upload("local_file.txt", "remote_file.txt")
    compute.run("ls -l")
    compute.stop_instance()
