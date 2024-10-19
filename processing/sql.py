class sql:
    db_name = '../data/data.db'
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

    add_scores = f'''ALTER TABLE {_table_name}
                    ADD COLUMN IF NOT EXISTS low TEXT,
                    ADD COLUMN IF NOT EXISTS medium TEXT,
                    ADD COLUMN IF NOT EXISTS high TEXT;
                    '''
    
    insert_sql = f'INSERT INTO {_table_name} VALUES (?, ?, ?, ?, ?, ?)'

    update_low = f'''UPDATE {_table_name}
    SET low = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''
    
    update_med = f'''UPDATE {_table_name}
    SET med = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''
    
    update_high = f'''UPDATE {_table_name}
    SET high = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''

    delete_sql = f'DELETE FROM {_table_name}'