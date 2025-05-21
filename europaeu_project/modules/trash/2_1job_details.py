import os
import sys
import time
import requests
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from load_django import *
from parser_app.models import Job, JobDocument
from datetime import datetime
from django.utils.timezone import make_aware

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/134.0.0.0 Safari/537.36",
    "Referer": "https://europa.eu/eures/portal/jv-se/",
}

BASE_URL = "https://europa.eu/eures/eures-apps/searchengine/page/jv/id/{}?lang=en"
LANG = "de"

job_ids = Job.objects.values_list('job_id', flat=True)

for job in Job.objects.filter(status="New"):
    job_id = job.job_id
    url = BASE_URL.format(job_id)

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ {job_id}: Помилка статусу {response.status_code}")
            continue

        data = response.json()
        profile = data.get("jvProfiles", {}).get("fr") or data.get("jvProfiles", {}).get("de") or {}


        job_data = {
            "job_id": data.get("id"),
            "reference": data.get("reference"),
            "creation_data": data.get("creationDate"),
            "last_modification_data": data.get("lastModificationDate"),
            "preferred_language": data.get("preferredLanguage"),

            "language_version": profile.get("languageVersion"),
            "job_title": profile.get("title"),
            "position_schedule_codes": profile.get("positionScheduleCodes"),
            "employment_period": profile.get("employmentPeriod"),
            "job_description": profile.get("description"),
            "required_skills": profile.get("requiredSkills"),
            "locations": profile.get("locations"),

            "required_experiences": profile.get("requiredExperiences"),
            "offered_remuneration_package": profile.get("offeredRemunerationPackage"),
            "required_driving_licenses": profile.get("requiredDrivingLicenses"),
            "position_languages": profile.get("positionLanguages"),
            "working_language_codes": profile.get("workingLanguageCodes"),

            "employer": profile.get("employer"),
            "application_instruction": profile.get("applicationInstructions"),
            "person_contacts": profile.get("personContacts"),
            "last_application_date": profile.get("lastApplicationDate"),
            "travel_preference": profile.get("travelPreference"),
        }

        try:
            doc, created = JobDocument.objects.get_or_create(**job_data)
            if created:
                print(f"✅ Додано JobDocument: {job_id}")
                job.status = 'Done'
                job.save()
            else:
                print(f"🔄 Вже існує JobDocument: {job_id}")
        except ValidationError as e:
            print(f"ValidationError для job_id={job_id}: {e}")
        except Exception as e:
            print(f"Інша помилка job_id={job_id}: {e}")

    except requests.RequestException as e:
        print(f"Запит до {job_id} провалився: {e}")

    time.sleep(2)
