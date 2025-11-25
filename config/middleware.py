from django.http import HttpResponsePermanentRedirect


class WwwRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()

        # Если запрос к домену БЕЗ www - редиректим на версию С www
        if host == 'natalis-domini.ru':
            new_url = f"https://www.natalis-domini.ru{request.path}"
            return HttpResponsePermanentRedirect(new_url)

        return self.get_response(request)