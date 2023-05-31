import boto3
import urllib3
import json
from datetime import datetime, timedelta
http = urllib3.PoolManager()
boto3 = boto3.session.Session(profile_name='hack')
emr = boto3.client('emr')

emr_hr_1 = []
emr_hr_2 = []
emr_hr_3 = []

def emr_status():

    page_iterator = emr.get_paginator('list_clusters').paginate(
        ClusterStates=['RUNNING','WAITING','STARTING','BOOTSTRAPPING']
    )
    emr_list = []

    for page in page_iterator:
        if page['Clusters']:
            for item in page['Clusters']:

                if item['NormalizedInstanceHours']>=0:
                    emr_list.append(item['Id'])
                    # response = slack_notification(item['Name']+" is "+item['Status']['State']+". This cluster is running for "+str(item['NormalizedInstanceHours']))
                # else:
                #     return 'Success'
    return emr_list

def ec2_list_running_instances():
    print('EC2 Instance monitoring')
    ec2_client = boto3.client('ec2')

    # Get the instance status
    response = ec2_client.describe_instances()
    running_instances=[]
    for j in response['Reservations']:
        for i in j['Instances']:
            if i['State']['Name'] == 'running':
                running_instances.append(i['InstanceId'])
    return running_instances

def get_ec2_metrics(running_instances):
    cw_client = boto3.client('cloudwatch')
    # Get the CPU utilization of the instance for the last two minutes
    now = datetime.utcnow()
    idle_instances = []
    for i in running_instances:
        response = cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'cpu_utilization',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [
                                {
                                    'Name': 'InstanceId',
                                    'Value': i
                                },
                            ]
                        },
                        'Period': 60,
                        'Stat': 'Average',
                        'Unit': 'Percent'
                    },
                    'ReturnData': True
                },
            ],
            StartTime=now - timedelta(hours=3),
            EndTime=now
        )
        # Check if the CPU utilization is below a certain threshold (e.g. 5%) for the last two minutes
        cpu_percent_list = response['MetricDataResults'][0]['Values']
        avg_cpu_utlz = sum(cpu_percent_list)/len(cpu_percent_list)
        if avg_cpu_utlz and avg_cpu_utlz < 5:
            idle_instances.append(i+' - '+str(avg_cpu_utlz)+'%')
        else:
            print(f"The instance is not idle - {i} - {avg_cpu_utlz} %")
    return idle_instances

# def lambda_handler(event, context):

# EMR Cluster monitoring and alerting
#  ****
# idle_emr=emr_status()
#
# # EC2 Instance Monitoring and alerting
# list_instances = ec2_list_running_instances()
# idle_ec2 = get_ec2_metrics(list_instances)
#
# if 'list' in str(type(idle_ec2)):
#     for i in idle_ec2:
#         slack_notification(i, 'Idle EC2 Instance with CPU Utilization % : ')
# else:
#     slack_notification(idle_ec2, 'Idle EC2 Instance with CPU Utilization % : ')
