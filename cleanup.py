import json
import boto3
import os
from botocore.exceptions import ClientError

def cleanup_resources():
    """Read resources.json and clean up AWS resources."""
    try:
        with open("resources.json", "r") as file:
            resources = json.load(file)

        ec2_client = boto3.client("ec2", region_name="us-east-1")

        # Terminate instances
        instances = resources.get("instances", [])
        if instances:
            try:
                ec2_client.terminate_instances(InstanceIds=instances)
                print(f"Termination of instances {instances} initiated.")
                waiter = ec2_client.get_waiter("instance_terminated")
                waiter.wait(InstanceIds=instances)
                print("Instances terminated.")
            except ClientError as e:
                print(f"Error terminating instances: {e}")

        # Delete security groups
        for group_id in resources.get("security_groups", []):
            try:
                ec2_client.delete_security_group(GroupId=group_id)
                print(f"Security group {group_id} deleted.")
            except ClientError as e:
                print(f"Error deleting security group {group_id}: {e}")

        # Delete key pair
        key_name = resources.get("key_name")
        key_path = resources.get("key_path")
        if key_name:
            try:
                ec2_client.delete_key_pair(KeyName=key_name)
                print(f"Key pair {key_name} deleted.")
            except ClientError as e:
                print(f"Error deleting key pair {key_name}: {e}")

        if key_path and os.path.exists(key_path):
            try:
                os.remove(key_path)
                print(f"Key file {key_path} deleted.")
            except OSError as e:
                print(f"Error deleting key file {key_path}: {e}")

    except FileNotFoundError:
        print("resources.json not found. Nothing to clean up.")
    except KeyError as e:
        print(f"Missing key in resources.json: {e}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_resources()
