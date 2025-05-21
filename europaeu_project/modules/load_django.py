import os
import sys

import django

sys.path.append("C:\\Users\\artur\\PycharmProjects\\JobSearchProject\\europaeu_project")
os.environ["DJANGO_SETTINGS_MODULE"] = "europaeu_project.settings"
django.setup()