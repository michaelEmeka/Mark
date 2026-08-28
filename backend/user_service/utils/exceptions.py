# utils/exceptions.py
from rest_framework.views import exception_handler as drf_exception_handler

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        response.data = {
            "error": {
                "code": exc.__class__.__name__.upper(),
                "message": "Please correct the errors below." 
                    if isinstance(response.data, dict) else str(response.data),
                "fields": response.data if isinstance(response.data, dict) else None,
            }
        }

    return response