from functools import wraps
from flask import session, redirect, url_for

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login'))  # ≈сли не админ Ч перенаправление на страницу входа
        return f(*args, **kwargs)  # »наче Ч выполнить защищЄнную функцию
    return decorated_function

