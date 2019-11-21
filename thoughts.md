### Design thoughts
The app is designed to easily submit one query or multiple queries by copy and paste.

Multiple queries will be executed one by one which must be separated by **;**.

A SanKey diagram will be used to show the relationships between topics, streams, tables and queries. 
The nodes and links are clickable, which will output the properties dynamically as an interactive table.
You can choose to check the messages in the topic/stream/table with offset **'earliest'** or **'latest'**.
You can set limit number of consumption, default is 10. The column name will be parser based on the query statement.

