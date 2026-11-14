from django.urls import path
from . import views


urlpatterns = [

    # Главные страницы
    path('', views.home, name='home'),
    path('showcase/', views.showcase, name='showcase'),

    # Регистрация и авторизация
    path('auth/', views.auth, name='auth'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout_view, name='logout'),

    # Фильмы
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movie/', views.movie_by_get, name='movie_by_get'),

    # Профиль
    path('profile/', views.profile, name='profile'),

    # Личный список просмотра
    path(
        'watchlater/add/<int:movie_id>/',
        views.watchlater_add,
        name='watchlater_add'
    ),

    path(
        'watchlater/edit/<int:item_id>/',
        views.watchlater_edit,
        name='watchlater_edit'
    ),

    path(
        'watchlater/delete/<int:item_id>/',
        views.watchlater_delete,
        name='watchlater_delete'
    ),
]