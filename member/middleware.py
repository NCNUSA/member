import time

from django.utils.deprecation import MiddlewareMixin


class MultipleProxyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        f = open("./web.log", "a")
        print(
            request.META["REMOTE_ADDR"],
            time.asctime(),
            request.META["REQUEST_METHOD"],
            request.META["PATH_INFO"],
            request.META["SERVER_PROTOCOL"],
            request.META["HTTP_USER_AGENT"],
            file=f,
        )
        f.close()
