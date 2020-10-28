import itertools
import re

from ec_tools.database.database_client import DatabaseClientInterface

PARENTHESES_PATTERN = re.compile(r'(\([^()]+\))')


def get_col_num(sql_pattern):
    return PARENTHESES_PATTERN.findall(sql_pattern)[0].count(',') + 1


def batch_execute(database_client: DatabaseClientInterface, sql_pattern: str, items: list):
    if not items:
        return None
    if not isinstance(items[0], (list, tuple)):
        items = [items]
    col_num = get_col_num(sql_pattern)
    assert col_num == len(items[0]), 'size of sql and data does not match! {} != {}'.format(
        col_num, len(items[0]))
    sql = sql_pattern.format(', '.join(['({})'.format(', '.join(['?'] * col_num))] * len(items)))
    args = list(itertools.chain(*items))
    return database_client.execute(sql, args)
