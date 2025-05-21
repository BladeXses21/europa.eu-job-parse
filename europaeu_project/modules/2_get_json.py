import requests
from load_django import *
from parser_app.models import Job, JobJson

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7",
    "Connection": "keep-alive",
    "Cookie": "EURES_JVSE_SESSIONID=611A3287A599CF339A88B153894284CD; ...",  # кукі повний
    "Host": "europa.eu",
    "Referer": "https://europa.eu/eures/portal/jv-se/jv-details/{}?lang=en",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

BASE_URL = "https://europa.eu/eures/eures-apps/searchengine/page/jv/id/{}?lang=en"

jobs = Job.objects.filter(status='New')

for job in jobs:
    job_id = job.job_id
    if not job_id:
        continue

    url = BASE_URL.format(job_id)
    headers = HEADERS.copy()
    headers["Referer"] = headers["Referer"].format(job_id)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch job {job_id}: {response.status_code}")
        continue

    json_data = response.json()
    jv_profiles = json_data.get("jvProfiles", {})

    if "de" in jv_profiles:
        jv_profile = jv_profiles["de"]
    elif "fr" in jv_profiles:
        jv_profile = jv_profiles["fr"]
    elif jv_profiles:
        jv_profile = next(iter(jv_profiles.values()))
    else:
        jv_profile = {}

    title = jv_profile.get("title", None)

    obj, created = JobJson.objects.get_or_create(
        job_id=job_id,
        defaults={
            "json_data": json_data,
            "title": title
        }
    )
    if created:
        print(f"Created JobJson for job_id={job_id}")
        job.status = 'Done'
        job.save()
    else:
        print(f"JobJson already exists for job_id={job_id}")


