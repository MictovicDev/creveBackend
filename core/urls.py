from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), #you can use to login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api', views.DocumentApi.as_view(), name="endpoints" ),
    path('auth/', views.CreateUserView.as_view(), name='client_signup'),
    # path('auth/creative/', views.TalentView.as_view(), name='talent_signup'),
    path('auth/activation/', views.ActivateAccount.as_view(), name='activateaccount'),
    path('questions/', views.QuestionListCreateView.as_view(), name='question-create'),
    path('questions/<str:pk>/', views.QuestionUpdateDel.as_view(), name='question-list'),
    path('userprofile/', views.ClientProfileGetView.as_view(), name="usersprofile"),
    path('user/<str:pk>/', views.ClientUpdateGetDeleteView.as_view(), name="clientupdate"),
    path('userprofile/<str:pk>/', views.ClientProfileGetUpdateView.as_view(), name="userprofileupdate"),
    path('creativeprofile/', views.TalentProfileGetView.as_view(), name="creativeprofile"),
    path('tcreativeprofile/', views.UnAuthTalentProfileGetView.as_view(), name="tcreativeprofile"),
    path('creativeprofile/<str:pk>/', views.TalentProfileGetUpdateView.as_view(), name="creativeprofile"),
    path('skills/', views.SkillsListCreateView.as_view(), name="create-skill"),
    path('skills/<str:pk>/', views.SkillUpdateDel.as_view(), name='skillupdate'),
    path('reviews/<str:pk>/', views.ReviewCreateView.as_view(), name="create_review"),
    path('bookcreatives/<str:pk>/', views.BookCreativeView.as_view(), name="book_creative"),
    path('books/', views.BookView.as_view(), name="books"),
    path('reviews/', views.ListReview.as_view(), name='reviews'),
    path('waitlist/', views.WaitListView.as_view(), name='waitlist'),
    path('gallery/', views.GalleryListCreateView.as_view(), name="create-gallery"),
    path('gallery/<str:pk>/', views.GalleryUpdateDel.as_view(), name= "delete-gallery"),
    path('otp/', views.UpdateOtpSecretView.as_view(), name='otp')

]
