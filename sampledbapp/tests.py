# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from sampledbapp.models import *
from django.contrib.auth.models import Group,User,UserManager
from django.test import Client

class ProjectSamplesTestCase(TestCase):

    def setUp(self):

        new_group, created = Group.objects.get_or_create(name='Test Group')
        testproject1 = Project.objects.create(title='testproject1',group=new_group,p_code='P12345')
        testproject2 = Project.objects.create(title='testproject2',group=new_group,p_code='P23456')

        self.create_sample(testproject1,'sample1','human1')
        self.create_sample(testproject2,'sample2','human2')

    def test_projects_exist(self):

        testproject1 = Project.objects.get(title="testproject1")
        testproject2 = Project.objects.get(title="testproject2")

        self.assertNotEqual(testproject1,None)
        self.assertNotEqual(testproject2,None)


    def test_samples_exist(self):

        sample1 = Sample.objects.filter(project=Project.objects.get(title="testproject1"))
        sample2 = Sample.objects.filter(project=Project.objects.get(title="testproject2"))

        self.assertEqual(len(sample1),1)
        self.assertEqual(len(sample2),1)


    def create_sample(self,project,sample_id,parent_id):

        sample = Sample.objects.create(project=project,
                                       study_title='study title test',
                                       sample_id=sample_id,
                                       species = 'Human',
                                       sample_matrix='Plasma',
                                       collection_protocol='Something',
                                       parent_type='human id',
                                       parent_id=parent_id,
                                       consent_form_information='Consent form is here...',
                                       sample_storage_type='NMR Tubes',
                                       hazard_group='1',
                                       #hazard_description,
                                       campus='SK',
                                       building='SAF',
                                       room='LG134',
                                       freezer_id='123',
                                       box_id='45678',
                                       tissue_bank_reference='THIS-IS-A-CODE')

        sample.save()


    def test_logged_out_views_redirects(self):

        c = Client()

        response = c.get('/')
        self.assertEquals(response.status_code,200)

        response = c.get('/home/')
        self.assertEquals(response.status_code,302)

        response = c.get('/login/')
        self.assertEquals(response.status_code,302)

        response = c.get('/logout/')
        self.assertEquals(response.status_code,302)

        response = c.get('/edit-project/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-projects/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-samples/')
        self.assertEquals(response.status_code,302)

        response = c.get('/sample-staging/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-tasks/')
        self.assertEquals(response.status_code,302)

        response = c.get('/pending-commits/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-commit/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-files/')
        self.assertEquals(response.status_code,302)

        response = c.get('/sample-search/')
        self.assertEquals(response.status_code,302)

        response = c.get('/download-file/')
        self.assertEquals(response.status_code,302)


    def test_logged_in_views_redirects(self):

        User.objects.create_user(username='testuser', email=None, password='testpass')

        c = Client()
        c.login(username='testuser',password='testpass')

        response = c.get('/')
        self.assertEquals(response.status_code,302)

        response = c.get('/home/')
        self.assertEquals(response.status_code,200)

        response = c.get('/login/')
        self.assertEquals(response.status_code,302)

        response = c.get('/logout/')
        self.assertEquals(response.status_code,302)

        c.login(username='testuser',password='testpass')

        response = c.get('/edit-project/?project_id=1')
        self.assertEquals(response.status_code,200)

        response = c.get('/view-projects/')
        self.assertEquals(response.status_code,200)

        response = c.get('/view-samples/')
        self.assertEquals(response.status_code,200)

        response = c.get('/sample-staging/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-tasks/')
        self.assertEquals(response.status_code,200)

        response = c.get('/pending-commits/')
        self.assertEquals(response.status_code,200)

        response = c.get('/view-commit/')
        self.assertEquals(response.status_code,302)

        response = c.get('/view-files/?file_id=1')
        self.assertEquals(response.status_code,200)

        response = c.get('/sample-search/')
        self.assertEquals(response.status_code,302)

        response = c.get('/download-file/')
        self.assertEquals(response.status_code,302)


