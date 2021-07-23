import yaml

REPO_URL_PATTERN = "ros2-gbp"

def parse_yaml_to_dictionary(filepath):
    "Opens the given YAML file path and parses it into a dictionary"
    with open(filepath) as f:
        data = yaml.safe_load(f)
        return data

def get_release_url(repo_dict):
    if "release" not in repo_dict:
        return None
    return repo_dict["release"]["url"]

def get_release_url_for_repo_in_dict(repo, d):
    return get_release_url(d["repositoryes"][repo])

def compare(yaml_a, yaml_b):
    "Here, yaml_a will usually be 'galactic' and yaml_b will be 'rolling'."

    # Let's first parse the two YAML files into two Python dictionaries.
    dict_a = parse_yaml_to_dictionary(yaml_a)
    dict_b = parse_yaml_to_dictionary(yaml_b)

    # A
    # This is the first condition that we are trying to meet.
    repos_with_ros_2_in_a = set()
    for r in dict_a["repositories"]:
        release_url = get_release_url(dict_a["repositories"][r])
        # Check if the release URL for this repo DOES have the pattern.
        # We do a None check because a repo may not have a release URL at all
        if release_url is not None and REPO_URL_PATTERN in release_url:
            repos_with_ros_2_in_a.add(r)

    # B
    # This is the second condition that we are trying to meet.
    repos_with_non_ros_2_in_b = set()
    for r in dict_b["repositories"]:
        release_url = get_release_url(dict_b["repositories"][r])
        # Check if the release URL for this repo DOES NOT have the pattern.
        # We do a None check because a repo may not have a release URL at all
        if release_url is not None and REPO_URL_PATTERN not in release_url:
            repos_with_non_ros_2_in_b.add(r)

    print("Repos from '" + yaml_a + "' with '" + REPO_URL_PATTERN + "'")
    print(repos_with_ros_2_in_a)

    print("")

    print("Repos from '" + yaml_b + "' WITHOUT '" + REPO_URL_PATTERN + "'")
    print(repos_with_non_ros_2_in_b)

    repos_of_interest = repos_with_ros_2_in_a.intersection(repos_with_non_ros_2_in_b)
    print("")
    print("Intersection:")
    print(repos_of_interest)

if __name__ == "__main__":
    compare("galactic.yaml", "rolling.yaml")