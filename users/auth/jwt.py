def get_user_info(user):
    return {
        'id': user.id,
        'username': user.username,
        'phone': user.phone,
        'email': user.email
    } 