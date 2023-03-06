class ApplicationError(Exception):
    """Core application error."""

    def __init__(self, message, extra=None):
        """Initial block.

        @param message: message for exception context
        @param extra: extra data.
        """
        super().__init__(message)

        self.message = message
        self.extra = extra or {}
