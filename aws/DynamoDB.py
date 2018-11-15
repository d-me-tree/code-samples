# DynamoDB
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html

########################################################################################################################
# Core Components
# https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html
#
# TABLES
#   Similar to other database systems, DynamoDB stores data in tables. A table is a collection of data.
#
# ITEMS
#   Each table contains zero or more items. An item is a group of attributes that is uniquely identifiable
# among all of the other items. In a People table, each item represents a person. Items in DynamoDB are similar
# in many ways to rows.
#
# ATTRIBUTES
#   Each item is composed of one or more attributes. An attribute is a fundamental data element,
# something that does not need to be broken down any further.
########################################################################################################################

from pprint import pprint

import boto3


dynamodb = boto3.resource('dynamodb')


def create_table(table_name):
    """
    :param table_name: str
    :return: dynamodb.Table instance
    """
    # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.create_table
    params = {
        'TableName': table_name,

        # Columns
        'AttributeDefinitions': [
            {'AttributeName': 'MyPrimaryKey', 'AttributeType': 'S'},
        ],

        # Indexing
        'KeySchema': [
            {'AttributeName': 'MyPrimaryKey', 'KeyType': 'HASH'}
        ],

        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    dynamodb.create_table(**params)

    # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Waiter.TableExists
    waiter = dynamodb.meta.client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)


def delete_table(table_name):
    dynamodb.Table(table_name).delete()

    # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Waiter.TableNotExists
    waiter = dynamodb.meta.client.get_waiter('table_not_exists')
    waiter.wait(TableName=table_name)


def create_or_update_item(table_name, item):
    """
    Creates a new item, or replaces an old item with a new item.

    :param table_name: str
    :param item: dict
    :return: dict, {'ResponseMetadata': {...}}
    """
    # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item
    table = dynamodb.Table(table_name)
    return table.put_item(Item=item)


def get_item(table_name, item):
    """
    :param table_name: str
    :param item: dict
    :return: dict, {'Item': {...}, 'ResponseMetadata': {...}}
    """
    # http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.get_item
    table = dynamodb.Table(table_name)
    return table.get_item(Key=item)


def main():
    # List available methods and attributes
    print([prop for prop in dir(dynamodb) if not prop.startswith('_')])

    # List DynamoDB tables
    print([table.name for table in dynamodb.tables.all()])

    # print(create_table('test_table_DD'))
    # print([table.name for table in dynamodb.tables.all()])
    #
    # new_item = {
    #     'MyPrimaryKey': 'some-value',
    #     'NewAttribute': 123
    # }
    # pprint(create_or_update_item('test_table_DD', item=new_item))
    #
    # pprint(get_item('test_table_DD', item={'MyPrimaryKey': 'some-value'}))
    #
    # pprint(delete_table('test_table_DD'))
    # print([table.name for table in dynamodb.tables.all()])


if __name__ == '__main__':
    main()
