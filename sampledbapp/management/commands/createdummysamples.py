from django.core.management.base import BaseCommand, CommandError
from sampledbapp.models import *
from django.contrib.auth.models import Group

class Command (BaseCommand):

    def handle(self, *args, **options):

        Sample.objects.all().delete()

        new_group, created = Group.objects.get_or_create(name='Test PI Name')

        project = Project.objects.create(title='test project1',group=new_group,p_code='P12345')

        self.create_sample(project,'sample1','human1')
        self.create_sample(project,'sample2','human2')
        self.create_sample(project,'sample3','human2')
        self.create_sample(project,'sample4','human2')
        self.create_sample(project,'sample5','human2')
        self.create_sample(project,'sample6','human2')
        self.create_sample(project,'sample7','human2')
        self.create_sample(project,'sample8','human2')
        self.create_sample(project,'sample9','human2')
        self.create_sample(project,'sample10','human2')
        self.create_sample(project,'sample11','human2')
        self.create_sample(project,'sample12','human2')
        self.create_sample(project,'sample13','human2')
        self.create_sample(project,'sample14','human2')
        self.create_sample(project,'sample15','human2')
        self.create_sample(project,'sample16','human2')
        self.create_sample(project,'sample17','human2')
        self.create_sample(project,'sample18','human2')
        self.create_sample(project,'sample19','human2')
        self.create_sample(project,'sample20','human2')
        self.create_sample(project,'sample21','human2')
        self.create_sample(project,'sample22','human2')
        self.create_sample(project,'sample23','human2')
        self.create_sample(project,'sample24','human2')


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
                              sample_storage_type='Eppendorf',
                              hazard_group='1',
                              #hazard_description,
                              campus='campus1',
                              building='building1',
                              room='room1',
                              freezer_id='123',
                              box_id='45678',
                              tissue_bank_reference='THIS-IS-A-CODE')

        sample.save()

        #print(sample)



