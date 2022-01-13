from django.urls import path
from django.views.generic.base import RedirectView, View
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[

    path('home/',views.HomePageView.as_view(),name='home'),
    path('',RedirectView.as_view(url='home')),
    path('accounts/login/',views.login_view,name='login'),
    path('accounts/logout/',views.logout_view,name='logout'),
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'),name='password-reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html' ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confrim.html' ),name='password_reset_confirm'),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html' )
    ,name='password_reset_complete'),
    
    path('signup/',views.signup_view,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('users/',views.Users.as_view(),name='users'),
    path('user/item',views.RequestBook.as_view(),name='user-item'),
    path('users/user',views.RequestBook.as_view(),name='users-user'),
    path('booked/item',views.UserBookedItem.as_view(),name='booked_item'),

    path('block/users/',views.BlockUserView.as_view(),name='block-users'),
    path('requsted/user',views.BookView.as_view(),name='requested-book'),
    path('book/user/accept',views.BookedUserAccept.as_view(),name='accept_book'),
    path('book/user/reject',views.BookedUserReject.as_view(),name='reject-book'),
    path('block/user/',views.BlockUserView.as_view(),name='block-user'),
    path('user/unbook/item',views.UnBookedItemView.as_view(),name='user_unbook_item'),
    path('unbook/item',views.UnBookedItemView.as_view(),name='unbook_item'),
    path('users/details/',permission_required('user.is_admin')(views.UsersDetails.as_view()),name='users-details'),
    path('list/admin',permission_required('user.is_admin')(views.AdminListView.as_view()),name='admin-list'),
    path('block-users/',permission_required('user.is_admin')(views.BlockListView.as_view()),name='block-users'),
    path('unblock-users/',views.UnblockUser.as_view(),name='unblock-user'),
    path('unblock-user/',views.UnblockUser.as_view(),name='unblock-users'),
    path('user/post/accept',views.AcceptedPosts.as_view(),name='accept_post'),
    path('user/accept/all',views.AcceptAllPosts.as_view(),name='accept_all'),
    path('user/reject/all',views.RejectAllPost.as_view(),name='accept_all'),
    path('user/post/reject',views.RejectedPosts.as_view(),name='reject_post'),
    path('home/<str:category>',views.sort_item,name='category'),
    path('user/item/<int:id>',views.booked_item_view,name='item-detail'),
    path('profile/<int:id>/',views.profile_edit,name='user-edit'),
    path('users/user/<int:pk>',views.UserDetail.as_view(),name='user'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)