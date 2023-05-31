import boto3
from .tag_commons import has_required_tags


def list_untagged_dynamo_tables():
    session = boto3.Session(profile_name='hack', region_name='us-west-2')
    # client = session.client('s3')
    AWS_REGION = session.region_name
    AWS_ACCOUNT_ID = session.client("sts").get_caller_identity()["Account"]

    dynamodb = session.client("dynamodb")

    table_names = dynamodb.list_tables()["TableNames"]
    flagged_tables = []

    for table_name in table_names:
        resource_arn = (
            f"arn:aws:dynamodb:{AWS_REGION}:{AWS_ACCOUNT_ID}:table/{table_name}"
        )
        response = dynamodb.list_tags_of_resource(ResourceArn=resource_arn)
        tags = response.get("Tags", [])

        if not has_required_tags(tags):
            flagged_tables.append(table_name)

    print("Flagged tables:", flagged_tables)
    return flagged_tables


if __name__ == "__main__":
    list_untagged_dynamo_tables()
