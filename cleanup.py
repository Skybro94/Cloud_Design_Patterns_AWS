from typing import List
import os

def cleanup_resources(instances: List[str], security_groups: List[str], key_name: str, ssh_key_path: str, ec2_client):
    """Cleanup all AWS resources."""
    try:
        # Terminate instances
        ec2_client.terminate_instances(InstanceIds=instances)
        print(f"Termination of instances {instances} initiated.")

        # Wait for instances to terminate
        waiter = ec2_client.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=instances)
        print("Instances terminated.")

        # Delete security groups
        for group_id in security_groups:
            try:
                ec2_client.delete_security_group(GroupId=group_id)
                print(f"Deleted security group: {group_id}")
            except Exception as sg_error:
                print(f"Error deleting security group {group_id}: {sg_error}")

        # Delete key pair
        try:
            ec2_client.delete_key_pair(KeyName=key_name)
            os.remove(ssh_key_path)
            print("Deleted key pair and local key file.")
        except Exception as key_error:
            print(f"Error deleting key pair or key file: {key_error}")

    except Exception as e:
        print(f"Error during cleanup: {e}")
