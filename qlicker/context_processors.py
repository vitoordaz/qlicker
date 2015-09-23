from django.conf import settings


def site(request):
    """This context processor enrich template context with a site info."""
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    name = site.name
    domain = site.domain if not settings.DEBUG else 'qlicker.co'
    return {'SITE': {'name': name, 'domain': domain}}