import os

from flask import json, Response, url_for


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


def video_url_for(func: str, **kwargs):
    url = os.environ.get('URL', 'http://api:5000')
    return f"{url}{url_for(func, **kwargs)}"
