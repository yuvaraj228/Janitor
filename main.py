from package.tags.list_untagged_instances import list_untagged_instances
from package.tags.list_untagged_emr_clusters import list_untagged_emr_clusters
from package.tags.list_untagged_buckets import list_untagged_buckets
from package.tags.list_untagged_dynamo_tables import list_untagged_dynamo_tables
from package.clusterMonitoring.janitor_monitor import emr_status, ec2_list_running_instances, get_ec2_metrics
import urllib3
http = urllib3.PoolManager()
import json

def slack_notification(msg, prefix=''):
    url = "https://hooks.slack.com/services/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"
    msg = {
        "channel": "#hackathon-janitor",
        "username": "janitor_bot",
        "text": prefix + msg,
        "icon_emoji": ":janitor:"
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)
    return resp

def slack_msg_conversion(inp, prefix=''):
    if 'list' in str(type(inp)):
        for i in inp:
            slack_notification(i,prefix)
    else:
        slack_notification(inp)
def run():
    # Listing the Poorly tagged resources and sending notification to Slack
    slack_msg_conversion(list_untagged_instances(), 'Untagged EC2 Instances : ')
    slack_msg_conversion(list_untagged_emr_clusters(), 'Untagged EMR Clusters : ')
    slack_msg_conversion(list_untagged_buckets(), 'Untagged S3 Buckets : ')
    slack_msg_conversion(list_untagged_dynamo_tables(), 'Untagged DynamoDB Tables : ')

    # Finding Idle resources and sending a slack notification out
    slack_msg_conversion(emr_status(), 'Idle EMR Cluster - ')
    list_instances = ec2_list_running_instances()
    slack_msg_conversion(get_ec2_metrics(list_instances), 'Idle EC2 Instance with CPU Utilization % : ')


if __name__ == "__main__":
# def lambda_handler(event, context):
    run()
