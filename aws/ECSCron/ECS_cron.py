########################################################################################################################
# ECS Scheduled Tasks aka Cron
#
# Cron rule, e.g. every_3_hours, has 1 or more tasks (aka targets in AWS-speak).
#
# Documentation:
#   https://docs.aws.amazon.com/AmazonECS/latest/developerguide/scheduled_tasks_cli_tutorial.html
#   https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
########################################################################################################################

import json
from pprint import pprint

import boto3
import yaml
from prettytable import PrettyTable


########################################################################################################################
# Cron Rules
########################################################################################################################


def list_cron_rules():
    """
    :return: list of {
        'Arn': 'arn:aws:events:eu-west-1:149681194111:rule/every_3_hours',
        'Name': 'every_3_hours',
        'ScheduleExpression': 'cron(0 0/3 * * ? *)',
        'State': 'ENABLED'
    }
    """
    events = boto3.client('events')
    return events.list_rules()['Rules']


def remove_cron_rule(rule_name):
    """
    Deletes `rule_name`, e.g. 'every_3_hours', and associated tasks from AWS.

    :param rule_name: str
    """
    events = boto3.client('events')

    associated_tasks = events.list_targets_by_rule(Rule=rule_name)['Targets']

    target_ids = [t['Id'] for t in associated_tasks]
    if target_ids:
        events.remove_targets(Rule=rule_name, Ids=target_ids)

    events.delete_rule(Name=rule_name)


########################################################################################################################
# Cron Tasks
########################################################################################################################

def list_cron_tasks():
    """
    Lists deployed cron tasks.
    """
    events = boto3.client('events')

    tbl = PrettyTable()
    tbl.field_names = ['rule_name', 'cluster', 'task_name', 'task_definition', 'command']
    tbl.align['rule_name'] = 'l'

    for rule in events.list_rules()['Rules']:
        rule_name = rule['Name']
        for target in events.list_targets_by_rule(Rule=rule_name)['Targets']:
            cluster = target['Arn'].split('/')[-1]
            task_name = target['Id']
            task_definition = target['EcsParameters']['TaskDefinitionArn'].split('/')[-1]
            command = json.loads(target.get('Input', '{}')).get('containerOverrides', [{}])[0].get('command')

            tbl.add_row([rule_name, cluster, task_name, task_definition, command])

    print(tbl)


def remove_deployed_cron_task(task_name):
    """
    "Undeploy" task_name.
    """
    events = boto3.client('events')
    for rule in events.list_rules()['Rules']:
        rule_name = rule['Name']
        for task in events.list_targets_by_rule(Rule=rule_name)['Targets']:
            if task['Id'] == task_name:
                events.remove_targets(Rule=rule_name, Ids=[task_name])
                return


def _clusters():
    """
    Returns a map of "Cluster Name --> Cluster ARN" (Amazon Resource Name).

    :return: {'cluster_name': 'cluster_arn'}
    """
    ecs = boto3.client('ecs')
    return {arn.split('/')[-1]: arn for arn in ecs.list_clusters()['clusterArns']}


def aws_describe_task_definition(task_name):
    ecs = boto3.client('ecs')
    return ecs.describe_task_definition(taskDefinition=task_name)['taskDefinition']


def assign_task_to_cron_rule(rule_name, task):
    """
    Adds `task` under `rule_name`.

    :param rule_name: str, e.g. `every_3_hours`
    :param task: dict, defined in `cron.yaml`
    """
    targets = []

    task_definition = task['task_definition']

    # Container overrides
    command = task.get('command')
    environment = task.get('environment')

    clusters = _clusters()

    # Copy task across clusters
    for cluster in task.get('clusters', []):
        target = {
            'Id': '{task_name}-{cluster}'.format(task_name=task['name'], cluster=cluster),
            'EcsParameters': {
                'TaskDefinitionArn': 'arn:aws:ecs:eu-west-1:149681194111:task-definition/{}'.format(task_definition)
            },
            'Arn': clusters[cluster]['arn'],
            'RoleArn': 'arn:aws:iam::149681194111:role/ecsEventsRole',
        }

        if command or environment:
            container_name = aws_describe_task_definition(task_definition)['containerDefinitions'][0]['name']
            overrides = {
                'name': container_name
            }

            if command:
                overrides['command'] = command
            if environment:
                overrides['environment'] = environment

            target['Input'] = json.dumps({'containerOverrides': [overrides]})

        targets.append(target)

    if targets:
        events = boto3.client('events')
        events.put_targets(Rule=rule_name, Targets=targets)


def deploy_cron(task_name, cluster):
    """
    Deploy an individual cron task.
    """
    with open('./cron.yaml', 'r') as f:
        cron_rules = yaml.safe_load(f)

    events = boto3.client('events')
    rules_in_aws = {rule['Name'] for rule in events.list_rules()['Rules']}

    # It is possible for the same task to be defined under multiple rules:
    # e.g. "run task_A every_10_minutes and every_3_hours".
    # Therefore, check every rule for matching task.
    for rule in cron_rules:
        rule_name = rule['rule_name']

        for task in rule['tasks']:
            if task_name == task['name']:

                if rule_name not in rules_in_aws:
                    events.put_rule(Name=rule_name, ScheduleExpression=rule['schedule'])
                    rules_in_aws.add(rule_name)

                if cluster is not None:
                    task['clusters'] = [cluster]

                assign_task_to_cron_rule(rule_name, task)
                continue


if __name__ == '__main__':
    pprint(list_cron_rules())
