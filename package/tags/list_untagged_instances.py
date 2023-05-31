import boto3
from .tag_commons import has_required_tags


def list_untagged_instances():
    session = boto3.session.Session(profile_name='hack')
    client = session.client('ec2')

    # TODO: add filters
    response = client.describe_instances()

    instances = response["Reservations"][0]["Instances"]

    flagged_instances = []

    for instance in instances:
        instance_id = instance["InstanceId"]
        tags = instance["Tags"]

        if not has_required_tags(tags):
            flagged_instances.append(instance_id)

    print("Flagged instances:", flagged_instances)
    return flagged_instances


if __name__ == "__main__":
    list_untagged_instances()
