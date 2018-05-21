# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.

#from simple_history.admin import SimpleHistoryAdmin
from .models import Project, Sample, Job, Staging, File

admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(Sample, SimpleHistoryAdmin)
#admin.site.register(Project)
#admin.site.register(Sample)
admin.site.register(Job)
admin.site.register(Staging)
admin.site.register(File)

