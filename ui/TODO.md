1. add loading status for 
    1. querying
    2. checking server status
    3. find the relationships
    
2. polish ui

3. Add function to split multiple queries
    1. if multiple queries are all executed, check the relationships at the end
    2. if multiple queries has error, check the relationship after the error for executed query
    3. if no queries are executed, not check relationships
    
4. add button to manually refresh relationship and properties

5. Connect consumer group and query_id, make it clickable, and show the consumer lags in real time
6. Try to apply something new in KSQLDB