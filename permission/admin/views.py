from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from . import PermissionRoleAdmin
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):
    if direction == "up":
        PermissionRoleAdmin.move_up(model_type_id, model_id)
    else:
        PermissionRoleAdmin.move_down(model_type_id, model_id)

    ModelClass = ContentType.objects.get(id=model_type_id).model_class()

    app_label = ModelClass._meta.app_label
    model_name = ModelClass.__name__.lower()

    redirect_url = request.META.get('HTTP_REFERER')
    if redirect_url is None:
        redirect_url = "/admin/%s/%s/" % (app_label, model_name)

    return HttpResponseRedirect(redirect_url)
