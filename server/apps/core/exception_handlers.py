from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

_VALIDATION_ERROR_MESSAGE = 'Validation error'


def proposed_exception_handler(exc, ctx):  # noqa: C901
    """Exception handler with an expected response structure.

    @return: Response. Example: {"message":"str", "extra":"dict"}
    """
    if isinstance(exc, ValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    if isinstance(exc.detail, (list, dict)):
        response.data = {'detail': response.data}

    if isinstance(exc, exceptions.ValidationError):
        message = _VALIDATION_ERROR_MESSAGE
        extra = {'fields': response.data.pop('detail')}
    else:
        message = response.pop('detail')
        extra = {}

    response.data.update({'message': message, 'extra': extra})

    return response
