from boto3 import client

SAMPLE_INSTANCE_DATA = {
    'Instances': [
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-53d13a927070628de', 'Type': 'a1.2xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-13T19:27:52.000Z', 'State': 'running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Jenkins Master'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-23a13a927070342ee', 'Type': 't2.medium',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Stopped',
         'StateReason': 'Client.UserInitiatedShutdown: User initiated shutdown', 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Consul Node'}]
         },
        {'Cloud': 'aws', 'Region': 'us-east-1', 'Id': 'i-77z13a9270708asd', 'Type': 't2.xlarge',
         'ImageId': 'ami-03cf127a',
         'LaunchTime': '2020-10-18T21:27:49.000Z', 'State': 'Running',
         'StateReason': None, 'SubnetId': 'subnet-3c940491', 'VpcId': 'vpc-9256ce43',
         'MacAddress': '1b:2b:3c:4d:5e:6f', 'NetworkInterfaceId': 'eni-bf3adbb2',
         'PrivateDnsName': 'ip-172-31-16-58.ec2.internal', 'PrivateIpAddress': '172.31.16.58',
         'PublicDnsName': 'ec2-54-214-201-8.compute-1.amazonaws.com', 'PublicIpAddress': '54.214.201.8',
         'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs',
         'SecurityGroups': [{'GroupName': 'default', 'GroupId': 'sg-9bb1127286248719d'}],
         'Tags': [{'Key': 'Name', 'Value': 'Grafana'}]
         }
    ]
}


def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']


def get_public_ip_reason(instance):
    if "PublicIpAddress" in instance:
        return instance['PublicIpAddress']


class InstanceData:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instances(self):
        my_instances = self.ec2_client.describe_instances()

        instances_data = []
        instance_data_dict_list = []

        for instance in my_instances['Reservations']:
            for data in instance['Instances']:
                instances_data.append(data)

        for instance in instances_data:
            try:
                if instance['State']['Name'] != "terminated" or instance['State']['Name'] != "shutting-down":
                    instance_data_dict = {}
                    instance_data_dict['Cloud'] = 'aws'
                    instance_data_dict['Region'] = self.ec2_client.meta.region_name
                    instance_data_dict['Id'] = instance['InstanceId']
                    instance_data_dict['Type'] = instance['InstanceType']
                    instance_data_dict['ImageId'] = instance['ImageId']
                    instance_data_dict['LaunchTime'] = instance['LaunchTime']
                    instance_data_dict['State'] = instance['State']['Name']
                    instance_data_dict['StateReason'] = get_state_reason( instance)
                    instance_data_dict['SubnetId'] = instance['SubnetId']
                    instance_data_dict['VpcId'] = instance['VpcId']
                    instance_data_dict['MacAddress'] = instance['NetworkInterfaces'][0]['MacAddress']
                    instance_data_dict['NetworkInterfaceId'] = instance['NetworkInterfaces'][0]['NetworkInterfaceId']
                    instance_data_dict['PrivateDnsName'] = instance['PrivateDnsName']
                    instance_data_dict['PrivateIpAddress'] = instance['PrivateIpAddress']
                    instance_data_dict['PublicDnsName'] = instance['PublicDnsName']
                    instance_data_dict['PublicIpAddress'] = get_public_ip_reason(instance)
                    instance_data_dict['RootDeviceName'] = instance['RootDeviceName']
                    instance_data_dict['RootDeviceType'] = instance['RootDeviceType']
                    instance_data_dict['SecurityGroups'] = instance['SecurityGroups']
                    instance_data_dict['Tags'] = instance['Tags']

                    instance_data_dict_list.append(instance_data_dict)
                    print(instance_data_dict_list[0])
            except Exception:
                raise

        return {'Instances': instance_data_dict_list}
