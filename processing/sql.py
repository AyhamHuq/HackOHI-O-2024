class sql:
    db_name = '../data/data.db'
    table_name = 'data'

    _attribute_names = [
        'Observation_no',
        'Date',
        'Point_name',
        'Qualifier_text',
        'Risk_notes',
        'Risk_follow_up'
    ]
    _primary_key = _attribute_names[0], _attribute_names[2]

    create_sql = f'''CREATE TABLE IF NOT EXISTS {table_name} (
        {_attribute_names[0]} INT,
        {_attribute_names[1]} DATETIME,
        {_attribute_names[2]} TEXT,
        {_attribute_names[3]} TEXT,
        {_attribute_names[4]} TEXT,
        {_attribute_names[5]} TEXT,
        PRIMARY KEY ({_primary_key[0]}, {_primary_key[1]})
    );'''

    add_scores = f'''ALTER TABLE {_table_name}
                    ADD COLUMN IF NOT EXISTS low TEXT,
                    ADD COLUMN IF NOT EXISTS medium TEXT,
                    ADD COLUMN IF NOT EXISTS high TEXT;
                    '''
    
    insert_sql = f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)'

    update_low = f'''UPDATE {_table_name}
    SET low = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''
    
    update_med = f'''UPDATE {_table_name}
    SET med = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''
    
    update_high = f'''UPDATE {_table_name}
    SET high = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''

    delete_sql = f'DELETE FROM {table_name}'

    retrieve_sql = f'SELECT * FROM {table_name}'