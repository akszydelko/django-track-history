from .tracker import TrackHelper


class TrackHelperRequestMiddleware(object):
    """
    This middleware sets user as a local thread variable, making it
    available to the model-level utilities to allow tracking of the
    authenticated user making a change.
    """

    def process_request(self, request):
        TrackHelper.thread.user = request.user
