from django.urls import path
from .views import content_editor, image_upload, content_save, view_content


urlpatterns = [
    path('yaz/', content_editor, name='pub_content_create'),
    path('yaz/<int:id>/', content_editor, name='pub_content_edit'),
    path('yaz/img/', image_upload, name='pub_content_upload_image'),
    path('yaz/save/', content_save, name='pub_content_save'),

    path('<slug:publication_slug>/<slug:content_slug>/', view_content, name='pub_content_detail'),
]
