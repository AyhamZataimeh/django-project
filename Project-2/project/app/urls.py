from django.urls import path
from django.views.generic.base import RedirectView, View
from django.contrib.auth.decorators import permission_required
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('home/',views.HomePageView.as_view(),name='home'),
    path('',RedirectView.as_view(url='home')),
    path('accounts/login/',views.login_view,name='login'),
    path('accounts/logout/',views.logout_view,name='logout'),
    path('signup/',views.signin_view,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('usres/',views.Users.as_view(),name='users'),
    path('user/item',views.BookItemView.as_view(),name='user-item'),
    path('users/user',views.BookItemView.as_view(),name='users-user'),
    path('block/user/',views.BlockUserView.as_view(),name='block-user'),
    path('user/unbook/item',views.UnBookedItemView.as_view(),name='unbook_item'),
    path('list/admin',permission_required('user.is_admin')(views.AdminListView.as_view()),name='admin-list'),
    path('block-users/',permission_required('user.is_admin')(views.BlockListView.as_view()),name='block-users'),
    path('unblock-users/',views.UnblockUser.as_view(),name='unblock-user'),
    path('user/post/accept',views.AcceptedPosts.as_view(),name='accept_post'),
    path('user/accept/all',views.AcceptAllPosts.as_view(),name='accept_all'),
    path('user/post/reject',views.RejectedPosts.as_view(),name='reject_post'),
    path('home/<str:category>',views.sort_item,name='category'),
    path('user/item/<int:id>',views.booked_item_view,name='item-detail'),
    path('profile/<int:id>/',views.profile_edit,name='user-edit'),
    path('users/user/<int:pk>',views.UserDetail.as_view(),name='user'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)