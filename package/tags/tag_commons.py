def has_required_tags(tags_array):
    tag_compliance = {
        "Name": False,
        "Environment": False,
        "Product": False,
        "Team": False,
    }

    for tag in tags_array:
        tag_key = tag["Key"]
        if tag_key in tag_compliance:
            tag_compliance[tag_key] = True

    return all(tag_compliance.values())
