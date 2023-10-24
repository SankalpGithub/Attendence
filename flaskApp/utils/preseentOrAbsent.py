def find_user_id(user_id, present, absent):
    found_in_array1 = any(item['userId'] == user_id for item in present)
    found_in_array2 = any(item['userId'] == user_id for item in absent)

    if found_in_array1:
        return True
    elif found_in_array2:
        return False
    else:
        return "User ID is not present in either array."

