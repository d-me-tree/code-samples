# ECS
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html

from pprint import pprint

import boto3

ecs = boto3.client('ecs')


def describe_task_definition(task_family):
    """
    returned dict keys: [
        'containerDefinitions',
        'family',
        'placementConstraints',
        'requiresAttributes',
        'revision',
        'status',
        'taskDefinitionArn',
        'volumes'
    ]

    :param task_family: str
    :return: dict
    """
    return ecs.describe_task_definition(taskDefinition=task_family)['taskDefinition']


def create_new_task_revision(task_family, tag=None, deregister=True):
    """
    Creates new task revision. The previous task revision is copied and, optionally, modified (container tag updated).

    :param task_family: str
    :param tag: str
    :param deregister: bool. Delete previous task revision after successfully creating a new one. Default: True.
    """
    # Get the latest task revision from AWS
    task_definition = describe_task_definition(task_family)

    # NOTE: At the moment, we use 1 container per task definition. This may change in the future.
    container_definitions = task_definition['containerDefinitions'][0]

    if tag:
        container_definitions['image'] = container_definitions['image'].split(':')[0] + f':{tag}'

    # Create new task revision
    response = ecs.register_task_definition(family=task_family, containerDefinitions=[container_definitions])

    if deregister and response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
        task_revision = task_definition.get('revision', 1)
        ecs.deregister_task_definition(taskDefinition=f'{task_family}:{task_revision}')


def main():
    # List cluster ARNs (Amazon Resource Names)
    pprint(ecs.list_clusters()['clusterArns'])

    # List ACTIVE task definition family names
    print(ecs.list_task_definition_families(status='ACTIVE')['families'])


if __name__ == '__main__':
    main()
