from django.core.exceptions import PermissionDenied


class UserIsAuthorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
