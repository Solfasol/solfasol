from django.urls import path
from .views import content_editor, image_upload, content_save, content_detail


urlpatterns = [
    path('yaz/', content_editor, name='pub_content_create'),
    path('yaz/<int:content_id>/', content_editor, name='pub_content_edit'),
    path('yaz/img/', image_upload, name='pub_content_upload_image'),
    path('yaz/save/', content_save, name='pub_content_save'),
]
