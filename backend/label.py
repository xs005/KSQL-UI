from sklearn import preprocessing


class Label:
    def __init__(self, relationship_list=None):
        self.le = preprocessing.LabelEncoder()
        unique_list = list(set([element for relationship in relationship_list for element in relationship]))
        self.le.fit(unique_list)
        self.label = self.le.classes_
        self.relationship_list = relationship_list
        self.relationship_enc_list = []
        self.source_list = []
        self.target_list = []

        self.transform()

    def transform(self):
        for relationship in self.relationship_list:
            relationship_enc = self.le.transform(relationship)
            self.source_list.append(relationship_enc[0])
            self.target_list.append(relationship_enc[1])
            self.relationship_enc_list.append(relationship_enc)
