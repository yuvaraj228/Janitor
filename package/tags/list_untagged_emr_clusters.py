import boto3
from .tag_commons import has_required_tags


def list_untagged_emr_clusters():
    session = boto3.session.Session(profile_name='hack')
    client = session.client("emr")

    response = client.list_clusters(
        ClusterStates=[
            "STARTING",
            "BOOTSTRAPPING",
            "RUNNING",
            "WAITING",
        ]
    )

    clusters = response["Clusters"]

    flagged_clusters = []

    for cluster in clusters:
        cluster_id = cluster['Id']
        cluster_info = client.describe_cluster(ClusterId=cluster_id)['Cluster']
        tags = cluster_info['Tags']

        tag_compliance = {"Environment": False, "Product": False, "Team": False}

        for tag in tags:
            tag_key = tag['Key']
            if tag_key in tag_compliance:
                tag_compliance[tag_key] = True

        if not any(tag_compliance.values()):
            flagged_clusters.append(cluster_id)

    return flagged_clusters


if __name__ == "__main__":
    list_untagged_emr_clusters()
