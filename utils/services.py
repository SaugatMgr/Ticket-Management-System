# This file contains utility functions and services for the application.
from rest_framework.exceptions import NotAcceptable


def generate_error(message, code=None):
    """
    Generates a standardized error response.

    Args:
        message (str): The error message to include in the response.
        code (str, optional): An optional error code.

    Returns:
        dict: A dictionary representing the error response.
    """
    error = {"message": message}
    if code:
        error["code"] = code
    return {"error": error}


def get_instance_by_attr(model, attr_name, attr_value):
    """
    Retrieves the instance of a model according to the provided attribute name and value

    Args:
        model (django.db.models.Model): represents from which model class the instance will be retrieved
        attr_name (str): attribute name of the instance
        attr_value : value of the attribute

    Returns:
        instance of model if exists otherwise error
    """
    try:
        instance = model.objects.get(**{attr_name: attr_value})
        return instance
    except model.DoesNotExist:
        raise NotAcceptable(
            generate_error(
                message=f"model {model.__name__} with {attr_name} {attr_value} does not exist."
            )
        )
