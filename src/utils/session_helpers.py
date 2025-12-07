def get_sessions_in_hour_range(collection, user_id, start_hour: int, end_hour: int):
    all_sessions = list(collection.find({"userId": str(user_id)}))
    filtered = []
    for s in all_sessions:
        hour = s["date"].hour
        if start_hour <= end_hour:
            if start_hour <= hour < end_hour:
                filtered.append(s)
        else:
            if hour >= start_hour or hour < end_hour:
                filtered.append(s)
    return filtered