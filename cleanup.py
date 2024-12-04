from main import EC2Manager
import os

def cleanup_resources(ec2_manager: EC2Manager):
    """Cleanup all AWS resources."""
    try:
        # Terminate instances
        instances = [inst.instance.id for inst in ec2_manager.instances]
        ec2_manager.ec2_client.terminate_instances(InstanceIds=instances)
        print(f"Termination of instances {instances} initiated.")

        # Wait for instances to terminate
        waiter = ec2_manager.ec2_client.get_waiter("instance_terminated")
        waiter.wait(InstanceIds=instances)
        print("Instances terminated.")

        # Delete security groups
        for group_id in [
            ec2_manager.cluster_security_group_id,
            ec2_manager.proxy_security_group_id,
            ec2_manager.trusted_host_security_group_id,
            ec2_manager.gatekeeper_security_group_id,
        ]:
            try:
                ec2_manager.ec2_client.delete_security_group(GroupId=group_id)
                print(f"Deleted security group: {group_id}")
            except Exception as sg_error:
                print(f"Error deleting security group {group_id}: {sg_error}")

        # Delete key pair
        try:
            ec2_manager.ec2_client.delete_key_pair(KeyName=ec2_manager.key_name)
            os.remove(ec2_manager.ssh_key_path)
            print("Deleted key pair and local key file.")
        except Exception as key_error:
            print(f"Error deleting key pair or key file: {key_error}")

    except Exception as e:
        print(f"Error during cleanup: {e}")
