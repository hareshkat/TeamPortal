from django.urls import path
from .views import home, team_member, team_contri, team_contribution, useful_link, gallery, gallery_show_imgs

urlpatterns = [
    path('', home),
    path('home', home, name='home'),
    path('team/members', team_member, name='team_member'),
    path('team/contribution', team_contri, name='team_contri'),
    path('useful_link', useful_link, name='usefullink'),
    path('team/contribution/<int:m>/<int:y>', team_contribution, name='team_contribution'),
    path('gallery/<int:y>', gallery, name='gallery'),
    path('gallery/<int:y>/imgs/<str:title>/<int:img_id>', gallery_show_imgs, name='gallery_imgs')
]
