from load_django import *
from parser_app.models import JobInfo, Final
from django.db import IntegrityError

jobs = JobInfo.objects.exclude(email__isnull=True).exclude(email__exact="")

count_created = 0
for job in jobs:
    try:
        Final.objects.create(
            job_id=job.job_id,
            title=job.title,
            company=job.company,
            website=job.website,
            country=job.country,
            full_name=job.full_name,
            givenName=job.givenName,
            familyName=job.familyName,
            salary=job.salary,
            email=job.email,
            phone=job.phone,
            description=job.description,
            link=job.link,
            status=job.status,
        )
        count_created += 1
    except IntegrityError:
        continue

print(f"Перенесено {count_created} записів у Final.")
