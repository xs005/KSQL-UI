import numpy as np


def find_query_source(query):
    query_element_list = np.array(query.split(' '))
    # Find FROM and the name after FROM
    query_sources = []
    for j in np.where(np.logical_or(query_element_list == 'FROM', query_element_list == 'JOIN'))[0]:
        query_sources.append(query_element_list[j + 1].split(';')[0])

    return query_sources


def find_action(query):
    KSQL_ACTION = ['CREATE', 'DROP', 'TERMINATE', 'JOIN', 'INSERT', 'SELECT', 'FROM']


def find_entity(query):
    ENTITY = ['TABLE', 'STREAM']

    #TODO: Use a SQL parser to do this, and add STREAM as TABLE in the parser.
