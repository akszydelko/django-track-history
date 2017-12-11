from . import tracker


class TrackHistoryMiddleware(object):
    """
    This middleware sets user as a local thread variable, making it
    available to the model-level utilities to allow tracking of the
    authenticated user making a change.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tracker._thread_local.user = request.user
        response = self.get_response(request)
        del tracker._thread_local.user
        return response
