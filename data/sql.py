class sql:
    db_name = 'data.db'
    _table_name = 'data'
    _primary_key = 'Observation_no', 'Point_name'

    create_sql = f'''CREATE TABLE IF NOT EXISTS {_table_name} (
        {_primary_key[0]} INT,
        Date DATETIME,
        {_primary_key[1]} TEXT,
        Qualifier_text TEXT,
        Risk_notes TEXT,
        Risk_follow_up TEXT,
        PRIMARY KEY ({_primary_key[0]}, {_primary_key[1]})
    );'''
    
    insert_sql = f'INSERT INTO {_table_name} VALUES (?, ?, ?, ?, ?, ?)'

    delete_sql = f'DELETE FROM {_table_name}'