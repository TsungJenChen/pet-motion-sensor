SQL_DICT = {
    'INSERT_LITTERBOX_RECORD': """
    
    INSERT INTO cat.toilet 
    (id, in_time, out_time, duration, pee_or_poop, litter_box_id, record_type, update_time, update_user_id, create_time, create_user_id)
    VALUES
    (DEFAULT, '{in_time}', '{out_time}', '{duration}', '1', '{litter_box_id}', '{record_type}', '{update_time}', '{update_user_id}', '{create_time}', '{create_user_id}')
    
    """
    ,
    'SELECT_TEST_RECORDS': """
    
    SELECT * FROM cat.toilet WHERE create_user_id = 'test'
        
    """
    ,
    'DELETE_TEST_RECORDS': """
    
    DELETE FROM cat.toilet
    WHERE create_user_id = 'test'
    
    """,
    'INSERT_HEARTBEAT_RECORD': """
    INSERT INTO cat.heartbeat 
    (id, time_stamp)
    VALUES
    (DEFAULT, '{time}')
    """







}