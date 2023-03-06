from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from server.apps.core.exceptions import ApplicationError

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

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            context = {'message': exc.message, 'extra': exc.extra}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {'detail': response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data['message'] = _VALIDATION_ERROR_MESSAGE
        response.data['extra'] = {'fields': response.data['detail']}
    else:
        response.data['message'] = response.data['detail']
        response.data['extra'] = {}

    del response.data['detail']  # noqa: WPS420

    return response
