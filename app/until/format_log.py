def get_format_log(mes,user_id=None):
    if user_id is None:
        user_id="N/A"
    return f"[User_Id:{user_id}] {mes}"