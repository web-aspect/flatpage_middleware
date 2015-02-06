from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.models import FlatPage
from django.http import Http404
from django.conf import settings


class FlatpageFallbackMiddleware(object):
	def process_request(self, request):
		try:
            request.flatpage = FlatPage.objects.get(url=request.path_info)
		except:
            request.flatpage = None

	def process_response(self, request, response):
		if response.status_code != 404:
			return response
		try:
			return flatpage(request, request.path_info)
		except Http404:
            return response
		except:
			if settings.DEBUG:
                raise
			return response