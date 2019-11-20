from sklearn import preprocessing


class Label:
    def __init__(self, relationship_list=None, stream_list=None, table_list=None):
        self.stream_list = stream_list
        self.table_list = table_list
        self.le = preprocessing.LabelEncoder()
        unique_list = list(set([element for relationship in relationship_list for element in relationship]))
        self.le.fit(unique_list)
        self.label = self.le.classes_
        self.relationship_list = relationship_list
        self.relationship_enc_list = []
        self.source_list = []
        self.target_list = []

        self.transform()
        self.label_color = self.label_node_color()

    def transform(self):
        for relationship in self.relationship_list:
            relationship_enc = self.le.transform(relationship)
            self.source_list.append(relationship_enc[0])
            self.target_list.append(relationship_enc[1])
            self.relationship_enc_list.append(relationship_enc)

    def label_node_color(self):
        stream_color = ['blue']
        table_color = ['red']
        topic_color = ['black']
        label_color = []
        for label in self.label:
            if label in self.stream_list:
                label_color += stream_color
            elif label in self.table_list:
                label_color += table_color
            else:
                label_color += topic_color

        return label_color

    def label_link_color(self, link_list):
        csas_color = ['aqua']
        ctas_color = ['orange']
        insertquery_color = ['plum']
        registered_color = ['grey']
        link_color = []
        for link in link_list:
            link_type = link.split('_')[0].upper()
            if link_type == 'CSAS':
                link_color += csas_color
            elif link_type == 'CTAS':
                link_color += ctas_color
            elif link_type == 'INSERTQUERY':
                link_color += insertquery_color
            elif link_type == 'REGISTERED':
                link_color += registered_color
            else:
                link_color += 'grey'
        return link_color

    def label_link_value(self):
        target_list = [relationship[1] for relationship in self.relationship_list]
        link_value_list = []

        for relationship in self.relationship_list:
            source = relationship[0]
            target = relationship[1]
            if source not in self.stream_list and source not in self.table_list:
                link_value_list += [1]
            elif target not in self.stream_list and target not in self.table_list:
                link_value_list += [1]
            else:
                if target in target_list:
                    link_value_list += [1.0/target_list.count(target)]
        return link_value_list

