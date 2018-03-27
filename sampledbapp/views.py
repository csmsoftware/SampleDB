# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect,QueryDict
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,tokens
from django.contrib.auth.models import User, Group
import json
from sampledbapp.models import *
from django.utils.encoding import smart_str
from django.core.files.storage import default_storage
from datetime import datetime, timedelta

# Create your views here.
def index(request):

    #html = "<html><body>Hello world!</body></html>"
    #return HttpResponse(html)

    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to='/home/')

    template = loader.get_template('index.html')
    template_variables = {}

    return HttpResponse(template.render(template_variables,request))




def home(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

    template = loader.get_template('home.html')
    template_variables =  {}

    return HttpResponse(template.render(template_variables,request))




def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                # Redirect to a success page.

                messages.add_message(request, messages.SUCCESS, 'You have successfully logged in')
                return HttpResponseRedirect('/home/')
        else:
            messages.add_message(request, messages.ERROR, 'Login details incorrect')
            return HttpResponseRedirect('/')

    else:

        return HttpResponseRedirect('/')


def logout_user(request):

    logout(request)
    messages.add_message(request, messages.SUCCESS, 'You have successfully logged out')
    return HttpResponseRedirect('/')


def edit_project(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

    template = loader.get_template('edit-project.html')
    template_variables =  {}

    # Is there a project_id in the get param?
    if request.method == 'GET' and 'project_id' in request.GET:

        projects_to_edit = Project.objects.filter(pk=request.GET['project_id'])

        if len(projects_to_edit) == 0:
            messages.add_message(request, messages.ERROR, 'Project id ' + request.GET['project_id'] + ' not recognised.' )
            return HttpResponseRedirect('/')

        template_variables['project_to_edit'] = projects_to_edit[0]


    groups = Group.objects.all()
    template_variables['groups'] = groups

    return HttpResponse(template.render(template_variables,request))

def save_project(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

#    template = loader.get_template('edit-project.html')
#    template_variables =  {}

    if request.method == 'POST':

        project = save_project_data(request)
        return HttpResponseRedirect('/edit-project/?project_id='+ str(project.id))

    else:

        return HttpResponseRedirect('/')


def save_project_data(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

    if 'project_id' in request.POST:

        # existing object
        #print(request.POST)
        project = Project.objects.get(id=request.POST['project_id'])
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.group = Group.objects.get(id=request.POST['group_id'])
        project.p_code = request.POST['p_code']

        what = project.full_clean()
        #print('here..')
        #print(what)

        project.save()

    else:

        #New object
        project = Project( title=request.POST['title'],
                            description=request.POST['description'],
                            group=Group.objects.get(id=request.POST['group_id']),
                            p_code=request.POST['p_code'])

        #print(project.full_clean())

        project.save()

    messages.add_message(request,messages.SUCCESS,'Project saved!')

    return project



def view_projects(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')


    projects = Project.objects.filter(group__in=Group.objects.filter(user=request.user))

    template = loader.get_template('view-projects.html')
    template_variables = {}
    template_variables['projects'] = projects

    return HttpResponse(template.render(template_variables,request))


def view_samples(request):

    #Get the projects the user is in.

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')


    # Default all:
    #samples = Sample.objects.filter(project__in=Project.objects.filter(group__in=Group.objects.filter(user=request.user))).order_by('id')

    projects = Project.objects.filter(group__in=Group.objects.filter(user=request.user))

    template = loader.get_template('view-samples.html')
    template_variables = {}
    #template_variables['samples'] = samples
    template_variables['projects'] = projects
    #print request.session['current_project']
   # template_variables['current_project'] = request.session['current_project']

    return HttpResponse(template.render(template_variables,request))


def sample_staging(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')
    #

    if request.method == 'GET' and 'staging_id' in request.GET:

        staging_list = Staging.objects.filter(id=request.GET['staging_id'],user=request.user)

        if len(staging_list) > 0:

            staging = staging_list[0]

        else:
            messages.add_message(request, messages.ERROR, 'Staging ID not found...!' )
            return HttpResponseRedirect('/view-samples/')

    else:
        messages.add_message(request, messages.ERROR, 'Staging ID not found...!' )
        return HttpResponseRedirect('/view-samples/')

    staging_json = json.loads(staging.json)

   # print staging_json

    template = loader.get_template('sample-staging.html')
    template_variables = {'staging': staging, 'staging_json': staging_json}


    return HttpResponse(template.render(template_variables,request))

def view_tasks(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

    #jobs = Job.objects.filter(user=request.user).order_by('pk')

    template = loader.get_template('view-tasks.html')

    template_variables = {}

    return HttpResponse(template.render(template_variables,request))


def pending_commits(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

        #jobs = Job.objects.filter(user=request.user).order_by('pk')

    #staging = Staging.objects.filter(user=request.user,job.status__in=[1,2])

    template = loader.get_template('pending-commits.html')

    template_variables = {}

    return HttpResponse(template.render(template_variables,request))


def view_commit(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

        #jobs = Job.objects.filter(user=request.user).order_by('pk')

    staging = None

    if request.method == 'GET' and 'staging_id' in request.GET:

        staging = Staging.objects.filter(user=request.user,pk=request.GET['staging_id'],status__in=[2,3])[0]

    if not staging:

        messages.add_message(request, messages.ERROR, 'You do not have access to this data' )
        return HttpResponseRedirect('/')

    template = loader.get_template('view-commit.html')

    if staging.json:
        staging_json = json.loads(staging.json)
    else:
        staging_json = ''

   # print staging.field_validation


    template_variables = {'staging': staging, 'staging_json': staging_json}

    return HttpResponse(template.render(template_variables,request))


def view_files(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

        #jobs = Job.objects.filter(user=request.user).order_by('pk')
    projects = Project.objects.filter(group__in=Group.objects.filter(user=request.user))
    files = File.objects.filter(project__in=projects).order_by('-pk')
    template = loader.get_template('view-files.html')


    template_variables = {'files': files,'projects':projects}

    return HttpResponse(template.render(template_variables,request))

def download_file(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')

    if request.method == 'GET' and 'file_id' in request.GET:

        file_id = request.GET['file_id']
        file = File.objects.filter(pk=file_id)[0]
        file.datetime_last_accessed = datetime.now()
        file.save()

        response = HttpResponse(default_storage.open(file.filepath, "rb"),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file.filename)
        response['X-Sendfile'] = smart_str(file.filepath)

        response['X-Accel-Limit-Rate'] = 1024
        response['X-Accel-Buffering'] = "no"
        response['X-Accel-Charset'] = "utf-8"

        return response

    else:
        messages.add_message(request, messages.ERROR, 'No file recognised' )
        return HttpResponseRedirect('/home/')


def sample_search(request):

    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view this page' )
        return HttpResponseRedirect('/')


    if not request.user.groups.filter(name='Auditors').exists():

        messages.add_message(request, messages.ERROR, 'You do not have permission to view this page' )
        return HttpResponseRedirect('/home/')


    template = loader.get_template('sample-search.html')

    template_variables = {}

    return HttpResponse(template.render(template_variables,request))




























