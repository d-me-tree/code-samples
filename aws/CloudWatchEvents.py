# CloudWatchEvents
# http://boto3.readthedocs.io/en/latest/reference/services/events.html

from pprint import pprint

import boto3

events = boto3.client('events')


def main():
    # List rules
    print([r['Name'] for r in events.list_rules()['Rules']])

    # List tasks associated with rule
    pprint(events.list_targets_by_rule(Rule='every_3_hours')['Targets'])


if __name__ == '__main__':
    main()
