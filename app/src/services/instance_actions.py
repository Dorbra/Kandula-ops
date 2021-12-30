from boto3 import client


class InstanceActions:
    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instance_state(self, instance_id):
        response = ""
        try:
            response = self.ec2_client.describe_instance_status(
                InstanceIds=[str(instance_id)], IncludeAllInstances=True)
            response_state = response['InstanceStatuses'][0]['InstanceState']['Code']
        except Exception as e:
            print(e)
            response_state = 0

        return response_state

    def start_instance(self, instance_id):
        is_instance_started = False
        response = ""

        response = self.ec2_client.start_instances(
            InstanceIds=[str(instance_id)])
        response_state = response['StartingInstances'][0]['SurrentState']['Code']

        if (response_state == 0):
            is_instance_started = True
            return is_instance_started

        else:
            return is_instance_started

    def stop_instance(self, instance_id):
        is_instance_stopped = False
        instance_status = self.get_instance_state(instance_id)

        # code 16 means 'running'
        if(instance_status == 16):
            response = self.ec2_client.stop_instances(
                InstanceIds=[str(instance_id)])
            response_state = response['StoppingInstances'][0]['CurrentState']['Code']
            if (response_state == 64):
                is_instance_stopped = True
                print("STOPPING. Status: {} instanceId: {}".format(
                    response_state, instance_id))

            else:
                is_instance_stopped = False
                print("ERROR. Status: {} instanceId: {}".format(
                    response_state, instance_id))

            return is_instance_stopped

        else:
            return is_instance_stopped

    def terminate_instance(self, instance_id):
        is_instance_terminated = False
        response = self.ec2_client.terminate_instances(
            InstanceIds=[str(instance_id)])
        response_status = response['TerminatingInstances'][0]['CurrentState']['Code']

        if (response_status == 32):  # 'shutting down'
            is_instance_terminated = True
        else:
            is_instance_terminated = False

        return is_instance_terminated

    def action_selector(self, instance_action):
        return {
            'start': self.start_instance,
            'stop': self.stop_instance,
            'terminate': self.terminate_instance
        }.get(instance_action, lambda x: self.action_not_found(instance_action))

    @ staticmethod
    def action_not_found(instance_action):
        raise RuntimeError(
            "Unknown instance action selected: {}".format(instance_action))
