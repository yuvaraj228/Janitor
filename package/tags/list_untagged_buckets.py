import boto3
from time import time
from .tag_commons import has_required_tags


def list_buckets(client):
    response = client.list_buckets()
    buckets = response["Buckets"]
    return list(map(lambda bucket: bucket["Name"], buckets))


def get_bucket_tags(client, bucket_name):
    try:
        response = client.get_bucket_tagging(Bucket=bucket_name)
        tag_set = response["TagSet"]
        return tag_set
    except:
        return []


def list_untagged_buckets():
    session = boto3.Session(profile_name='hack')
    client = session.client('s3')

    t = time()
    bucket_names = list_buckets(client)
    # print(
    #     f"[debug] Took {(time() - t) * 1000:.2f} ms to list buckets; found {len(bucket_names)}"
    # )

    flagged_buckets = []

    for bucket_name in bucket_names:
        t = time()
        tags = get_bucket_tags(client, bucket_name)
        # print(
        #     f'[debug] Took {(time() - t) * 1000:.2f} ms to get bucket "{bucket_name}" tags'
        # )

        if not has_required_tags(tags):
            flagged_buckets.append(bucket_name)

    print("Flagged buckets:", flagged_buckets)
    return flagged_buckets


if __name__ == "__main__":
    list_untagged_buckets()
