from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.http import QueryDict
import json
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core import serializers
from sampledbapp.models import *
import django_rq
from datetime import datetime, timedelta
import sampledbapp.rq_workers
from django.core.files.storage import default_storage
from django.core.files.uploadhandler import InMemoryUploadedFile, TemporaryUploadedFile
import os
from io import BytesIO
import openpyxl
from django.conf import settings
from sampledbapp.utils import *
from sampledbapp import rq_workers
import urllib
import operator
#import unicode
import shutil

# Save a new or edited project
def save_project(request):

    form_data = QueryDict(request.POST['form_data'])

    # save project

    if 'project_id' in form_data:

        project = Project.objects.get(id=form_data['project_id'])

        project.title = form_data['title']
        project.description = form_data['description']
        project.group = Group.objects.get(id=form_data['group_id'])
        project.p_code = form_data['p_code']

    else:

        #New object
        project = Project( title=form_data['title'],
                           description=form_data['description'],
                           group=Group.objects.get(id=form_data['group_id']),
                           p_code=form_data['p_code'])

    try:
        project.full_clean()

    except Exception as e:

        error_map = {}

        for field,error in e:

            error_map[field] = error

        data = {'failure': True,'Error': error_map}

    else:

        project.save()
        data = {'success':True}

    return HttpResponse(json.dumps(data), content_type = "application/json")

# Get the samples by project
def get_samples(request):

    #filters = request.POST['filters']

    #print(request.POST.getlist['filters'])

    if request.POST['project_id'] and request.POST['study_title']:

        samples = Sample.objects.filter(project__in=Project.objects.filter(pk=int(request.POST['project_id'])),study_title=request.POST['study_title']).order_by('id').exclude(is_deleted=True)

        deleted_samples = Sample.objects.filter(project__in=Project.objects.filter(pk=int(request.POST['project_id'])),study_title=request.POST['study_title'],is_deleted=True).order_by('id')

    else:

        samples = []
        deleted_samples = []
    #samples = Sample.objects.filter(project__in=Project.objects.filter(group__in=Group.objects.filter(user=request.user))).order_by('id')


    data = {'success': True, 'samples': serializers.serialize('json',samples),'deleted_samples':serializers.serialize('json',deleted_samples)}

    return HttpResponse(json.dumps(data), content_type = "application/json")

# Submit sample changes for staging
def submit_edit_samples(request):

    project_id = request.POST['project_id']

    form_data = QueryDict(request.POST['form_data'])

    edited_pks = extract_edited_pks(request.POST.getlist('edited_pks'))

    objects = extract_objects(edited_pks,form_data)
    #print objects

    #json_data = json.dumps({'edited_pks': edited_pks,'form_data': form_data})
    json_data = json.dumps(json.dumps({'edited_pks': edited_pks,'objects': objects}))

    staging_object = Staging.objects.create(status=1,
                                            user=request.user,
                                            json=json_data,
                                            project=Project.objects.get(pk=int(project_id)),
                                            type="UI submission")

    job = Job.objects.create(user=request.user,job_type='check_staging_samples',status=1,text_to_show=json_data,datetime_created=datetime.now())

    staging_object.job = job
    staging_object.save()

    #rq_workers.check_staging_samples(job.id,staging_object.id)
    rq_job = django_rq.enqueue(rq_workers.check_staging_samples, job.id,staging_object.id)
    job.rq_id = rq_job.id

    job.save()

    messages.add_message(request, messages.SUCCESS, "Sample changes submitted for validation")

    data = {'success':True,'staging_id':staging_object.id}

    return HttpResponse(json.dumps(data), content_type = "application/json")

def extract_objects(edited_pks,form_data):

    #print(form_data);

    data = {}

    for pk in edited_pks:

        data[pk] = extract_data(pk,form_data)

    return data

def extract_data(pk,form_data):

    data = {}

    data["study_title"] = form_data['study_title-' + pk]
    data["sample_id"] = form_data['sample_id-' + pk]
    data["species"] = form_data['species-' + pk]
    data["sample_storage_type"] = form_data['sample_storage_type-' + pk]
    data["sample_matrix"] = form_data['sample_matrix-' + pk]
    data["collection_protocol"] = form_data['collection_protocol-' + pk]
    data["campus"] = form_data['campus-' + pk]
    data["building"] = form_data['building-' + pk]
    data["room"] = form_data['room-' + pk]
    data["freezer_id"] = form_data['freezer_id-' + pk]
    data["shelf_id"] = form_data['shelf_id-' + pk]
    data["box_id"] = form_data['box_id-' + pk]
    data["parent_type"] = form_data['parent_type-' + pk]
    data["parent_id"] = form_data['parent_id-' + pk]
    data["consent_form_information"] = form_data['consent_form_information-' + pk]
    data["tissue_bank_reference"] = form_data['tissue_bank_reference-' + pk]
    data["hazard_group"] = form_data['hazard_group-' + pk]
    data["hazard_description"] = form_data['hazard_description-' + pk]

    return data

# Extract the PKs that are being edited.
def extract_edited_pks(submitted_edited_pks):

    # example "edited_pks%5B%5D=1&edited_pks%5B%5D=2"

    url_decoded = urllib.parse.unquote(submitted_edited_pks[0])
    array_of_pks = url_decoded.split('&')

    edited_pks = []

    for elem in array_of_pks:

        split_entry = elem.split('=')

        edited_pks.append(split_entry[1])

    return edited_pks

# Get the staging object, create a job, and add it to the queue
def commit_staging_samples(request):

    staging_id = request.POST['staging_id']

    staging = Staging.objects.get(pk=staging_id)

    #print staging.json

    job = Job.objects.create(user=request.user,job_type='commit_staging_samples',status=1,text_to_show=staging.json)

    staging.job = job
    staging.save()

    # INLINE EXECUTION
    #rq_workers.commit_staging_samples(job.id,staging.id)

    # RQ EXECUTION
    rq_job = django_rq.enqueue(rq_workers.commit_staging_samples, job.id, staging.id)
    job.rq_id = rq_job.id

    job.save()

    messages.add_message(request, messages.SUCCESS, "Pending changes job submitted")

    data = {'success':True}

    return HttpResponse(json.dumps(data), content_type = "application/json")

# Take a staging object and commit it. This now actually happens in redis-queue workers.
def convert_and_commit_json(staging_object):

    # IDK why this is double encoded. Just leave it for now.
    json_objects = json.loads(json.loads(staging_object.json))

    for sample_id,sample_fields in json_objects['objects'].items():

        if sample_id == 'new':

            staging_object = Sample.objects.create(**sample_fields)

        else:

            update_sample_model(sample_id,sample_fields)


# Take the number of days and return the jobs
def get_user_jobs(request):

    days = request.POST.get("days",7)

    time_threshold = datetime.now() - timedelta(days=int(days))

    # If reverse is set, reverse it. Otherwise default to 0
    if request.POST.get("reverse",0) == 0:
        jobs = Job.objects.filter(user=request.user,datetime_created__gt=time_threshold).order_by('pk')
    else:
        jobs = Job.objects.filter(user=request.user,datetime_created__gt=time_threshold).order_by('-pk')[:5]

    data = serializers.serialize('json',jobs)
    #jobs = serializers.serialize('json',jobs)

    return HttpResponse(data, content_type = "application/json")


# Get the pending commits
def get_pending_commits(request):

    # If reverse is set, reverse it. Otherwise default to 0
    stagings = Staging.objects.filter(user=request.user,status__in=[1,2,3]).order_by('-pk')[:10]
    project_ids = []
    for staging in stagings:
        project_ids.append(staging.project_id)
    projects = Project.objects.filter(pk__in=project_ids).all()
    project_names = {}
    for project in projects:
        project_names[project.pk] = project.title
    data = {}
    data['stagings'] = serializers.serialize('json', stagings)
    data['project_names'] = project_names
    #jobs = serializers.serialize('json',jobs)

    return HttpResponse(json.dumps(data), content_type = "application/json")


# Get the pending commits
def clear_all_non_completed_staging_tasks(request):

    # If reverse is set, reverse it. Otherwise default to 0
    stagings = Staging.objects.filter(user=request.user,status__in=[1,2,3])

    for staging in stagings:

        staging.status = 5
        staging.datetime_deleted = datetime.now()
        staging.save()

    messages.add_message(request, messages.SUCCESS, "All non-committed changes removed")

    data = {'success':True}

    return HttpResponse(json.dumps(data), content_type = "application/json")

# Recommit changes from the view-commit page
def recommit_staging_samples(request):

    # 1. Update fields in staging json with new entries
    # 2. Schedule a new validation check job

    stagings = Staging.objects.filter(pk=request.POST['staging_id'],user=request.user)

    if len(stagings) == 0:
        data = {'failure':True}
        return HttpResponse(json.dumps(data), content_type = "application/json")

    form_data = QueryDict(request.POST['form_data'])

    edited_pks = extract_edited_pks(request.POST.getlist('edited_pks'))

    #print edited_pks

    staging = stagings[0]

    json_data = json.loads(json.loads(staging.json))

    objects = extract_objects_for_recommit(json_data['objects'],edited_pks,form_data)

   # print objects

    json_data['objects'] = objects

    staging.json = json.dumps(json.dumps(json_data))
    staging.status = 1

    job = Job.objects.create(user=request.user,job_type='check_staging_samples',status=1,text_to_show=staging.json,datetime_created=datetime.now())

    staging.job = job
    staging.save()
    rq_workers.check_staging_samples(job.id,staging.id)
    #rq_job = django_rq.enqueue(rq_workers.check_staging_samples, job.id,staging.id)
    #job.rq_id = rq_job.id

    job.save()

    data = {'success':True}
    return HttpResponse(json.dumps(data), content_type = "application/json")

# Loop over the changed edits and add them to the json
def extract_objects_for_recommit(objects,edited_pks,form_data):

   # print edited_pks

   # print objects

    # Loop over the data. If its been edited, pull out the edit.
    for pk in edited_pks:

        #objects[pk] = test_extract_data(objects,pk,form_data)
        objects[pk] = extract_data_for_recommit(pk,objects[pk],form_data)

    return objects

def extract_data_for_recommit(pk,object,form_data):

    for key, value in form_data.items():

        key_array = key.split("-")

        sample_field_key = key_array[0]
        field_pk = key_array[1]

        if field_pk == pk:
            object[sample_field_key] = value

    return object


# File upload via ajax
def submit_file_upload(request):

    project_id = request.POST['project_id']

    filename = request.FILES['file'].name # received file name
    file_obj = request.FILES['file']

    folder_path = os.path.join(default_storage.location,'user_uploads',project_id)

    if not os.path.isdir(folder_path):
      # # print os.path.join(default_storage.location,path_to_save)
        os.mkdir(folder_path)

    # check its file extension

    filename_array = str.split(file_obj.name,".")
    file_extension = filename_array[1]

    allowed_filetypes = ['xlsx']

    if file_extension not in allowed_filetypes:
        return HttpResponse(json.dumps({'failure':True,'error':'file type not allowed'}), content_type = "application/json")



    file_obj.name = build_and_check_file_name(folder_path,0,file_obj.name)

   # print file_obj.name

    full_path = os.path.join(folder_path,file_obj.name)

    shutil.move(file_obj.temporary_file_path(),full_path)

    file = File.objects.create(project=Project.objects.get(pk=project_id),
                               user_uploaded=request.user,
                               filename=file_obj.name,
                               filepath=full_path,
                               datetime_uploaded=datetime.now(),
                               datetime_last_accessed = datetime.now(),
                               type='import')

    staging_object = Staging.objects.create(status=1,
                                            user=request.user,
                                            project=Project.objects.get(pk=project_id),
                                            type='File upload',
                                            file=file)

    job = Job.objects.create(user=request.user,job_type='validate_sample_file',status=1,datetime_created=datetime.now())

    staging_object.job = job
    staging_object.save()

    # INLINE EXECUTION
    #rq_workers.validate_sample_file(job.id,staging_object.id,file.id)

    # RQ EXECUTION
    rq_job = django_rq.enqueue(rq_workers.validate_sample_file, job.id,staging_object.id,file.id)
    job.rq_id = rq_job.id

    job.save()

    messages.add_message(request, messages.SUCCESS, "Sample changes submitted for validation")

    return HttpResponse(json.dumps({'success':True}), content_type = "application/json")


def get_files(request):

    projects = Project.objects.filter(group__in=Group.objects.filter(user=request.user))
    files = File.objects.filter(project__in=projects).order_by('-pk')
    usernames = {}
    projectnames = {}

    for file in files:
        if file.user_uploaded.username:
            usernames[file.pk] = file.user_uploaded.username
        else:
            usernames[file.pk] = "<i>unknown</i>"

        projectnames[file.pk] = file.project.title

    data = {'success':True,
            'files':serializers.serialize('json',files),
            'usernames': usernames,
            'projectnames': projectnames }


    return HttpResponse(json.dumps(data), content_type = "application/json")

def delete_staging_object(request):

    stagings = Staging.objects.filter(pk=request.POST['staging_id'],user=request.user)

    if len(stagings) == 0:
        data = {'failure':True}
        return HttpResponse(json.dumps(data), content_type = "application/json")

    staging_object = stagings[0]

    if staging_object.file:

        file = staging_object.file

        os.remove(file.filepath)

        file.delete()

    staging_object.delete()

    messages.add_message(request, messages.SUCCESS, "Sample changes deleted")

    return HttpResponse(json.dumps({'success':True}), content_type = "application/json")

def export_samples(request):

    job = Job.objects.create(user=request.user,job_type='export_to_excel',status=1,datetime_created=datetime.now())

    #print request.POST

   # print request.POST['sample_pks']

    # INLINE EXECUTION
    #rq_workers.export_to_excel(job.id,request.user,json.loads(request.POST['sample_pks']))

    # RQ EXECUTION
    rq_job = django_rq.enqueue(rq_workers.export_to_excel, job.id,request.user,json.loads(request.POST['sample_pks']))
    job.rq_id = rq_job.id

    job.save()

    messages.add_message(request, messages.SUCCESS, "Sample scheduled for export")

    return HttpResponse(json.dumps({'success':True}), content_type = "application/json")

# Ajax search samples
def search_samples(request):

    if request.user.groups.filter(name='Auditors').exists():

        samples = Sample.objects.all()

    else:

        samples = Sample.objects.filter(project__in=Project.objects.filter(group__in=Group.objects.filter(user=request.user)))

    # Filter the samples
    if request.POST['sample_id'] != '':
        samples = samples.filter(sample_id__icontains=request.POST['sample_id'].strip())

    if request.POST['box_id'] != '':
        samples = samples.filter(box_id__icontains=request.POST['box_id'].strip())

    if request.POST['freezer_id'] != '':
        samples = samples.filter(freezer_id__icontains=request.POST['freezer_id'].strip())

    if request.POST['parent_id'] != '':
        samples = samples.filter(parent_id__icontains=request.POST['parent_id'].strip())

    if request.POST['tissue_bank_reference'] != '':
        samples = samples.filter(tissue_bank_reference__icontains=request.POST['tissue_bank_reference'].strip())

    samples = samples.order_by('pk')

    sample_extras = {}

    # Set the extras needed for the view
    for sample in samples:

        sample_extras[sample.pk] = {}

        if sample.project:
            sample_extras[sample.pk]['project_title'] = sample.project.title
        else:
            sample_extras[sample.pk]['project_title'] = "None"

        if sample.last_edited_user:
            sample_extras[sample.pk]['last_edited_user'] = sample.last_edited_user.username
        else:
            sample_extras[sample.pk]['last_edited_user'] = "None"

    return HttpResponse(json.dumps({'success':True,
                                    'samples':serializers.serialize('json',samples),
                                    'sample_extras':sample_extras}),
                        content_type = "application/json")


def get_project_studies(request):

    if request.POST['project_id']:

        study_titles = Sample.objects.filter(project__in=Project.objects.filter(pk=int(request.POST['project_id']))).values('study_title').distinct()

    else:
        data = {'failure':True}

        return HttpResponse(json.dumps(data), content_type = "application/json")


    study_title_json = []

    for entry in study_titles:
        study_title_json.append(entry['study_title'])

    data = {'success':True,'study_titles':study_title_json}

    return HttpResponse(json.dumps(data), content_type = "application/json")


def delete_samples(request):

    samples = Sample.objects.filter(pk__in=json.loads(request.POST['sample_pks']))

    for sample in samples:

        sample.is_deleted = True
        sample.delete_method = request.POST['disposal_route']
        sample.save()

    data = {'success':True}

    return HttpResponse(json.dumps(data), content_type = "application/json")


def move_samples_to_project(request):

    samples = Sample.objects.filter(pk__in=json.loads(request.POST['sample_pks']))

    project = Project.objects.get(pk=request.POST['project'])

    for sample in samples:

        sample.project = project
        sample.save()

    data = {'success':True}

    return HttpResponse(json.dumps(data), content_type = "application/json")