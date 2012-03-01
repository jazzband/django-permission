from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$', 
         'permission.admin.views.admin_move_ordered_model', 
         name="pages-admin-move"
    ),
)
