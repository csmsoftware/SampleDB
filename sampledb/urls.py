"""sampledb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from sampledbapp import views,ajax_views

urlpatterns = [

    url(r'^django-rq/', include('django_rq.urls')),

    url(r'^admin/', admin.site.urls),


    url(r'^$',views.index, name='index'),

    url(r'^login',views.login_user, name='login'),

    url(r'^logout',views.logout_user, name='logout'),

    url(r'^home',views.home, name='home'),

    url(r'^edit-project',views.edit_project, name='edit project'),
    #   url(r'^save-project',views.save_project, name='save project'),

    url(r'^view-projects',views.view_projects, name='view projects'),

    url(r'^view-samples',views.view_samples, name='view samples'),

    url(r'^sample-staging',views.sample_staging, name='sample staging'),

    url(r'^view-tasks',views.view_tasks, name='view tasks'),

    url(r'^pending-commits',views.pending_commits, name='pending commits'),

    url(r'^view-commit',views.view_commit, name='view commit'),

    url(r'^view-files',views.view_files, name='view files'),

    url(r'^sample-search',views.sample_search, name='sample search'),

    url(r'^download-file',views.download_file, name='download file'),

    url(r'^ajax/save-project',ajax_views.save_project, name='save project'),

    url(r'^ajax/get-samples',ajax_views.get_samples, name='get samples'),

    url(r'^ajax/submit-edit-samples',ajax_views.submit_edit_samples, name='submit edit samples'),

    url(r'^ajax/commit-staging-samples',ajax_views.commit_staging_samples, name='commit staging samples'),

    url(r'^ajax/recommit-staging-samples',ajax_views.recommit_staging_samples, name='recommit staging samples'),

    url(r'^ajax/delete-staging-object',ajax_views.delete_staging_object, name='delete staging samples'),

    url(r'^ajax/get-user-jobs',ajax_views.get_user_jobs, name='get user jobs'),

    url(r'^ajax/get-pending-commits',ajax_views.get_pending_commits, name='get pending commits'),

    url(r'^ajax/clear-all-non-completed-staging-tasks',ajax_views.clear_all_non_completed_staging_tasks, name='get pending commits'),

    url(r'^ajax/submit-file-upload',ajax_views.submit_file_upload, name='get user jobs'),

    url(r'^ajax/export-samples',ajax_views.export_samples, name='export samples'),

    url(r'^ajax/get-files',ajax_views.get_files, name='get files'),

    url(r'^ajax/search-samples',ajax_views.search_samples, name='search samples'),

    url(r'^ajax/get-project-studies',ajax_views.get_project_studies, name='get project studies'),

    url(r'^ajax/delete-samples',ajax_views.delete_samples, name='delete samples'),


]
