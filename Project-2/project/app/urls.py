from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from django.conf.urls.static import static
from django.conf import settings
RedirectView
urlpatterns=[

    path('home/',views.home_page_view,name='home'),
    path('',RedirectView.as_view(url='home')),
    path('accounts/login/',views.login_view,name='login'),
    path('accounts/logout/',views.logout_view,name='logout'),
    path('signup/',views.signin_view,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('user/item',views.BookItemView.as_view(),name='user-item'),
    path('user/unbook/item',views.UnBookedItemView.as_view(),name='unbook_item'),
    path('list/admin',views.AdminListView.as_view(),name='admin-list'),
    path('user/post/accept',views.AcceptedPosts.as_view(),name='accept-post'),
    path('user/post/reject',views.RejectedPosts.as_view(),name='reject-post'),
    path('user/item/<int:id>',views.booked_item_view,name='item-detail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)