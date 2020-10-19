# Jex - JSON/YAML interactive explorer

## Why?
- In a world that JSON/YAML config files take over the world and JQ is
not your taste, use the language you already know to explore the data.
Whether it is Python/Hylang or ES6 on your favorite web browser developer tool.

- Fighting the bad practice of using online JSON pretifier/formatter, which is
prone to leak credentials contained in JSON/YAML (e.g K8S secret output).

## Install

`pip install jex`

## Features
- Supports input JSON/YAML.

### Explorers
Supports exploring via
- Python interpreter
- Hylang interpreter `hy`
- Interactive Ruby Shell `irb`
- Node `node`
- Web browser

## Usage
- Just pipe the jex after the command that outputs JSON/YAML.
```
$ curl -ssL https://api.github.com/users/hvnsweeting/repos | jex
```

- Use `jex -w` to open data on your browser, open web console and access the data via `data`.

![Firefox](firefox.png)

![Firefox DOM](dom.png)

- Use `jex -i` to open simple python interpreter - in same process - useful on
no GUI environment.

- Use `jex` would open a new window for interactive exploring the data via name `data` in Python interactive interpreter:
This pre-import `pprint`, all functions in `itertools`, `functools`, `operator` stdlib.
Provide `--repl LANG` to invoke other language interpreters.

```python
========== WELCOME TO JEX ==========
Access the data via name data
data is a list, with length 30, first elem of type <class 'dict'>
>>> data[0].keys()
dict_keys(['id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url', 'description', 'fork', 'url', 'forks_url', 'keys_url', 'collaborators_url', 'teams_url', 'hooks_url', 'issue_events_url', 'events_url', 'assignees_url', 'branches_url', 'tags_url', 'blobs_url', 'git_tags_url', 'git_refs_url', 'trees_url', 'statuses_url', 'languages_url', 'stargazers_url', 'contributors_url', 'subscribers_url', 'subscription_url', 'commits_url', 'git_commits_url', 'comments_url', 'issue_comment_url', 'contents_url', 'compare_url', 'merges_url', 'archive_url', 'downloads_url', 'issues_url', 'pulls_url', 'milestones_url', 'notifications_url', 'labels_url', 'releases_url', 'deployments_url', 'created_at', 'updated_at', 'pushed_at', 'git_url', 'ssh_url', 'clone_url', 'svn_url', 'homepage', 'size', 'stargazers_count', 'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki', 'has_pages', 'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 'license', 'forks', 'open_issues', 'watchers', 'default_branch'])
>>> pprint([(i['name'], i['html_url']) for i in data])
[('adventofcode', 'https://github.com/hvnsweeting/adventofcode'),
 ('airflow_docker', 'https://github.com/hvnsweeting/airflow_docker'),
 ('albatross', 'https://github.com/hvnsweeting/albatross'),
 ('alloy_ci', 'https://github.com/hvnsweeting/alloy_ci'),
 ('amnesia', 'https://github.com/hvnsweeting/amnesia'),
...
```

```yaml
$ echo 'apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80' | jex
```

```python
========== WELCOME TO JEX ==========
Access the data via name data
data is a dict, with keys: ['apiVersion', 'kind', 'metadata', 'spec']
>>> pprint(data['spec'])
{'replicas': 3,
 'selector': {'matchLabels': {'app': 'nginx'}},
 'template': {'metadata': {'labels': {'app': 'nginx'}},
              'spec': {'containers': [{'image': 'nginx:1.14.2',
                                       'name': 'nginx',
                                       'ports': [{'containerPort': 80}]}]}}}

```

## TODO
- Support Jid.

# Authors
- Viet Hung Nguyen <hvn@familug.org>
