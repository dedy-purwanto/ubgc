from django.contrib.sites.models import Site

def common(request):
    current_site = Site.objects.get_current()
    return {
            'SITE_NAME': current_site.name,
            }
