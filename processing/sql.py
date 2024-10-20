import sqlite3

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

    result_names = [
        'low',
        'medium',
        'high',
        'ppe',
        'documentation',
        'equipment',
        'traffic',
        'fire',
        'electrical',
        'fall'
    ]

    create_sql = f'''CREATE TABLE IF NOT EXISTS {table_name} (
        {_attribute_names[0]} INT,
        {_attribute_names[1]} DATETIME,
        {_attribute_names[2]} TEXT,
        {_attribute_names[3]} TEXT,
        {_attribute_names[4]} TEXT,
        {_attribute_names[5]} TEXT,
        PRIMARY KEY ({_primary_key[0]}, {_primary_key[1]})
    );'''

    def add_column(cursor: sqlite3.Cursor, attr_name: str, type: str) -> str: 
        cursor.execute(f"PRAGMA table_info({sql.table_name});")
        columns = [row[1] for row in cursor.fetchall()]
    
        if attr_name not in columns:
            cursor.execute(f"ALTER TABLE {sql.table_name} ADD COLUMN {attr_name} {type};")

    insert_sql = f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?);'

    def update_column(attr_name: str) -> str:
        return f'''UPDATE {sql.table_name}
        SET {attr_name} = ?
        WHERE {sql._primary_key[0]} = ? AND {sql._primary_key[1]} = ?;'''
    
    delete_sql = f'DROP TABLE {table_name};'

    retrieve_sql = f'''SELECT
        {_attribute_names[0]}, 
        {_attribute_names[2]}, 
        {_attribute_names[3]}, 
        {_attribute_names[4]}, 
        {_attribute_names[5]} 
    FROM {table_name}
    ORDER BY {_attribute_names[0]} ASC;'''

    retrieve_for_duplicates_sql = f'''SELECT
        {_primary_key[0]}, 
        {_primary_key[1]},
        low, 
        medium, 
        high
    FROM {table_name}
    ORDER BY {_primary_key[0]} ASC;'''

    update_risk_sql = f'''UPDATE {table_name}
    SET low = ?, medium = ?, high = ?
    WHERE {_primary_key[0]} = ? AND {_primary_key[1]} = ?;'''

    retrieve_results_sql = f'''SELECT
        {', '.join(result_names)},
        {_primary_key[0]}, 
        {_primary_key[1]}
    FROM {table_name}
    ORDER BY {_attribute_names[0]} ASC;'''
