from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        # Если запрос к домену С www - редиректим на версию БЕЗ www
        if host == 'www.natalis-domini.ru':
            new_url = f"https://natalis-domini.ru{request.path}"
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)