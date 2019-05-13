# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from simple_history.models import HistoricalRecords


# Check if the title already exists
def validate_project_title(value):
    pass
   # if len(Project.objects.filter(title=value)) > 0:
   #     raise ValidationError('Title already exists')

# Check if the description is not blank
def validate_project_description(value):
    pass
    #if value == "":
    #    raise ValidationError('Description must not be blank')

# Check if the group is selected
def validate_project_group(value):

    if not value:
        raise ValidationError('Please select a valid group')


def validate_project_group2(value):

    pass

# Check if the p_code is not empty
# Check if the first letter is a string
def validate_project_p_code(value):

    if not value[:1].isalpha():
        raise ValidationError('Please enter a valid project code')

# Check the campuses are allowed
def validate_campuses(value):

    pass

#   allowed_campuses = ['SK','CXH','HH','SMH']
#
#   if value not in allowed_campuses:
#
#       raise ValidationError('Campus must be one of SK, CXH, HH, or SMH')


class Project(models.Model):


    #title = models.CharField(max_length=80,validators=[validate_project_title])
    title = models.CharField(max_length=80,unique=True)
    description = models.CharField(max_length=5000,null=True,validators=[validate_project_description])

    group = models.ForeignKey(Group,related_name='proj_group',null=True,on_delete=models.PROTECT,validators=[validate_project_group])

    p_code = models.CharField(max_length=10,validators=[validate_project_p_code])
    project_reference_number = models.CharField(max_length=20,null=True,blank=True)
    datetime_created = models.DateTimeField('date created',auto_now_add=True)
    last_modified = models.DateTimeField('last modified',auto_now=True)
    changed_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return '%s' % (self.title)

class Sample(models.Model):

    project = models.ForeignKey(Project,on_delete=models.PROTECT,related_name='samples_project',verbose_name="Project",db_index=True)
    study_title = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    sample_id = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    species = models.CharField(max_length=80,null=True,blank=True)
    sample_matrix = models.CharField(max_length=255,null=True,blank=True)
    collection_protocol = models.CharField(max_length=255,null=True,blank=True)
    parent_type = models.CharField(max_length=255,null=True,blank=True)
    parent_id = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    consent_form_information = models.CharField(max_length=255,null=True,blank=True)
    sample_storage_type = models.CharField(max_length=255,null=True,blank=True)
    hazard_group = models.CharField(max_length=10,null=True,blank=True)
    hazard_description = models.CharField(max_length=255,null=True,blank=True)
    campus = models.CharField(max_length=10,null=True,blank=True,validators=[validate_campuses])
    building = models.CharField(max_length=100,null=True,blank=True)
    room = models.CharField(max_length=100,null=True,blank=True)
    freezer_id = models.CharField(max_length=40,null=True,blank=True,db_index=True)
    shelf_id = models.CharField(max_length=40,null=True,blank=True)
    box_id = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    tissue_bank_reference = models.CharField(max_length=60,null=True,blank=True,db_index=True)
    backfill_data_source = models.CharField(max_length=255,null=True,blank=True)
    is_aliquot = models.BooleanField(default=False)
    sample_parent_id = models.CharField(max_length=40,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,db_index=True)
    delete_method = models.CharField(max_length=255,null=True,blank=True)
    datetime_created = models.DateTimeField('datetime_created',auto_now_add=True,null=True) # Try and populate from the previous DB.
    history = HistoricalRecords()
    last_edited_user = models.ForeignKey(User, on_delete=models.PROTECT,related_name='last_edited_user',null=True)
    last_modified = models.DateTimeField('last modified',auto_now=True,null=True)
    changed_by = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
        self.last_edited_user = value

    def __str__(self):
        return '%s %s' % (self.sample_id,self.study_title)

    def validate(self,data):

        # Human checks
        if data['species'].lower().strip() == 'human':
            if data['tissue_bank_reference'] == '' or not data['tissue_bank_reference']:
                raise ValidationError('Human records must have a tissue bank reference')
            if data['consent_form_information'] == '' or not data['consent_form_information']:
                raise ValidationError('Human records must have consent form information')

        return data



class Job(models.Model):

    statuses = (
        (1, 'pending'),
        (2, 'running'),
        (3, 'failed'),
        (4, 'completed')
    )

    user = models.ForeignKey(User,on_delete=models.PROTECT, related_name='user_job',null=True)
    job_type = models.CharField(max_length=255,null=True,blank=True)
    serialized_worker = models.TextField(blank=True)
    text_to_show = models.TextField(blank=True)
    rq_id = models.CharField(max_length=255,null=True,blank=True)
    rq_exception = models.TextField(blank=True)
    status = models.SmallIntegerField(choices=statuses,blank=True)
    datetime_created = models.DateTimeField('datetime_created',auto_now_add=True)
    datetime_run = models.DateTimeField('datetime_run',blank=True,null=True)
    datetime_failed = models.DateTimeField('datetime_failed',blank=True,null=True)
    datetime_completed = models.DateTimeField('datetime_completed',blank=True,null=True)

    def __str__(self):
        return '%s' % (self.datetime_created)

class File(models.Model):

    project = models.ForeignKey(Project,on_delete=models.PROTECT,related_name='project_file',verbose_name="Project Files",null=True,blank=True)
    user_uploaded = models.ForeignKey(User, on_delete=models.PROTECT,related_name='user_uploaded',null=True)
    filename = models.CharField(max_length=1000,null=True,blank=True)
    filepath = models.TextField('filepath',blank=True)
    datetime_uploaded = models.DateTimeField('datetime_uploaded',auto_now_add=True)
    datetime_last_accessed = models.DateTimeField('datetime_last_accessed',blank=True,null=True)
    type = models.CharField(max_length=255,null=True,blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return '%s' % (self.filename)

# This is for storing sample changes during import and edit.
class Staging(models.Model):

   # statuses = (
   #     (1,'pending'),
   #     (2,'committed'),
   #     (3,'deleted'),
   #     (4, 'error'),
   #     (5, 'ready for commit')
   # )

    statuses = (
        (1, 'pending'),
        (2, 'error'),
        (3, 'ready for commit'),
        (4, 'committed'),
        (5, 'deleted')
    )

    type = models.CharField(max_length=255,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.PROTECT,related_name='project_being_edited',verbose_name="Project",null=True,blank=True)
    json = models.TextField('json',blank=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT, related_name='user_staging',null=True)
    job = models.ForeignKey(Job,on_delete=models.PROTECT,related_name='job_create_staging',null=True)
    datetime_added = models.DateTimeField('datetime_added',auto_now_add=True)
    datetime_committed = models.DateTimeField('datetime_committed',blank=True,null=True)
    datetime_deleted = models.DateTimeField('datetime_committed',blank=True,null=True)
    status = models.SmallIntegerField(choices=statuses,blank=True,null=True)
    datetime_checked = models.DateTimeField('datetime_committed',blank=True,null=True)
    field_validation = models.TextField('field_validation',blank=True)
    file_validation = models.TextField('file_validation',blank=True)
    file = models.ForeignKey(File,on_delete=models.PROTECT,related_name='staging_file',verbose_name="File",null=True,blank=True)
