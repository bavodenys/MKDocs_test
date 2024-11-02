import requests
import sys
import os

GITHUB_REPO = 'bavodenys/MKDocs_test'  # Replace with your repository name
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
RELEASE_TAG = sys.argv[1].strip('refs/tags/')  # Get the tag name

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_milestone_by_title(title):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/milestones'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    milestones = response.json()
    for milestone in milestones:
        if milestone['title'] == title:
            return milestone['number']
    return None

def get_issues_for_milestone(milestone_number):
    url = f'https://api.github.com/repos/{GITHUB_REPO}/issues'
    params = {
        'state': 'closed',
        'milestone': milestone_number
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def generate_release_notes(issues, release_tag):
    filename = f'docs/releases/{release_tag}.md'
    with open(filename, 'w') as f:
        f.write(f'# Release {release_tag}\n\n## Resolved Issues\n')
        if issues:
            for issue in issues:
                f.write(f"- {issue['title']} (#{issue['number']}) by @{issue['user']['login']}\n")
        else:
            f.write('No issues resolved in this release.\n')
    print(f'Release notes generated at {filename}')

milestone_number = get_milestone_by_title(RELEASE_TAG)
if milestone_number:
    issues = get_issues_for_milestone(milestone_number)
    generate_release_notes(issues, RELEASE_TAG)
else:
    print(f'Milestone {RELEASE_TAG} not found')
