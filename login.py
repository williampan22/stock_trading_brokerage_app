from functools import wraps 
from flask import Flask, render_template, redirect, request, session

# require user to log in 
def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return function(*args, **kwargs)
    return decorated_function