import dash_table


def without_keys(d, *keys):
    return dict(filter(lambda key_value: key_value[0] not in keys, d.items()))


# Remove duplicate elements in a list and key the order of element.
def find_unique(sequence):
    seen = set()
    unique_list = []
    if isinstance(sequence[0], str):
        for x in sequence:
            if x == 'REGISTERED':
                unique_list.append(x)
            else:
                if not (x in seen or seen.add(x)):
                    unique_list.append(x)
    elif isinstance(sequence[0], list):
        tuple_list = [tuple(x) for x in sequence]
        for x in tuple_list:
            if not (x in seen or seen.add(x)):
                unique_list.append(x)
    return unique_list


def generate_datatable(dataframe, table_id):
    return dash_table.DataTable(
        id='stream_table',
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict('records'))
