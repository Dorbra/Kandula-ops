import boto3

client = boto3.client("ec2")
reservations = client.describe_instances(Filters=[
    {"Name": "instance-state-name", "Values": ["running"], }
]).get("Reservations")

for reservation in reservations:
    for instance in reservation["Instances"]:
        instance_state = instance["State"]['Name']
        instance_id = instance["InstanceId"]
        instance_name = instance["Tags"][0]['Value']
        instance_type = instance["InstanceType"]
        public_ip = instance["PublicIpAddress"]
        private_ip = instance["PrivateIpAddress"]
        print(
            f"{instance_state}, {instance_name}, {instance_id}, {instance_type}, {public_ip}, {private_ip}")


def get_machine_time():
    return 1602824750094  # No need to implement at the moment


def check_aws_connection():
    # TODO: implement real call to aws describe instances. If successful, return true. otherwise return False
    try:
        if(instance_state == 'running'):
            is_available = True
        else:
            is_available = False
    except:
        is_available = False
    finally:
        print("\nFINALLY is_available = {}".format(is_available))
    return is_available


def check_db_connection():
    # TODO: implement real select query to db. If successful, return true. otherwise return False
    try:
        # UPDATE TO CHECK DBs subnet/group connection
        if(reservations):
            is_available = True
        else:
            is_available = False
    except:
        is_available = False
    finally:
        print("\nFINALLY is_available = {}".format(is_available))
    return is_available


def is_app_healthy(healthchecks):
    return all([check["Value"] for check in healthchecks])


def get_app_health():
    health_checks = [
        {"Name": "machine-time", "Value": get_machine_time()},
        {"Name": "aws-connection", "Value": check_aws_connection()},
        {"Name": "db-connection", "Value": check_db_connection()},
    ]

    return health_checks, is_app_healthy(health_checks)


check_aws_connection()
