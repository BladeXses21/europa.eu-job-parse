import requests
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime

from load_django import *
from parser_app.models import Job
from datetime import datetime

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,uk;q=0.7',
    'connection': 'keep-alive',
    'content-length': '482',
    'content-type': 'application/json',
    'cookie': 'EURES_JVSE_SESSIONID=7087A84E4AD6205AE3E63261FB9662E3; XSRF-TOKEN=48d19dbf-6e53-43df-bddb-1db1aca90e1f; _pk_ses.ba1b52b1-f8e5-42ec-93dc-088e1cd6d80f.53d5=*; _pk_id.ba1b52b1-f8e5-42ec-93dc-088e1cd6d80f.53d5=015d147e7af38d07.1741165734.1.1741166103.1741165734.; cck1=%7B%22cm%22%3Afalse%2C%22all1st%22%3Afalse%2C%22closed%22%3Afalse%7D',
    'host': 'europa.eu',
    'origin': 'https://europa.eu',
    'referer': 'https://europa.eu/eures/portal/jv-se/search?page=3&resultsPerPage=10&orderBy=BEST_MATCH&keywordsEverywhere=%D0%90%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D0%BE%D1%80&lang=en',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-xsrf-token': '48d19dbf-6e53-43df-bddb-1db1aca90e1f',
}

all_jobs = []

for page in range(1, 10):
    payload = {
        "resultsPerPage": 10,
        "page": page,
        "sortSearch": "BEST_MATCH",
        "keywords": [{"keyword": "Архитектор", "specificSearchCode": "EVERYWHERE"}],  # Запит "Архитектор"
        "publicationPeriod": None,
        "occupationUris": [],
        "skillUris": [],
        "requiredExperienceCodes": [],
        "positionScheduleCodes": [],
        "sectorCodes": [],
        "educationAndQualificationLevelCodes": [],
        "positionOfferingCodes": [],
        "locationCodes": [],
        "euresFlagCodes": [],
        "otherBenefitsCodes": [],
        "requiredLanguages": [],
        "minNumberPost": None,
        "sessionId": "husdqga2b652k1f3vaqhk",
    }

    url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()

        if not data['jvs']:
            print("На сторінці немає вакансій, цикл зупинено.")
            break

        print(f"Знайдено {data['numberRecords']} вакансій.")
        all_jobs.extend(data['jvs'])
    else:
        print(f"Помилка запиту: {response.status_code}")

print(f"Знайдено {len(all_jobs)} вакансій")

for job in all_jobs:
    job_info = {}

    try:
        job_info['title'] = job.get('title', None)
    except KeyError as e:
        job_info['title'] = None
        print(f"Error getting title: {e}")

    try:
        job_info['id'] = job.get('id', None)
    except KeyError as e:
        job_info['id'] = None
        print(f"Error getting id: {e}")

    try:
        job_info['description'] = job.get('description', None)
    except KeyError as e:
        job_info['description'] = None
        print(f"Error getting description: {e}")

    try:
        job_info['availableLanguages'] = job.get('availableLanguages', [])
    except KeyError as e:
        job_info['availableLanguages'] = None
        print(f"Error getting availableLanguages: {e}")

    try:
        job_info['numberOfPosts'] = job.get('numberOfPosts', None)
    except KeyError as e:
        job_info['numberOfPosts'] = None
        print(f"Error getting numberOfPosts: {e}")

    try:
        job_info['locationMap'] = job.get('locationMap', [])
    except KeyError as e:
        job_info['locationMap'] = []
        print(f"Error getting locationMap: {e}")

    try:
        job_info['jobCategoriesCodes'] = job.get('jobCategoriesCodes', [])
    except KeyError as e:
        job_info['jobCategoriesCodes'] = []
        print(f"Error getting jobCategoriesCodes: {e}")

    try:
        job_info['positionScheduleCodes'] = job.get('positionScheduleCodes', [])
    except KeyError as e:
        job_info['positionScheduleCodes'] = []
        print(f"Error getting positionScheduleCodes: {e}")

    try:
        job_info['employer'] = job.get('employer', {}).get('name', None)
    except KeyError as e:
        job_info['employer'] = None
        print(f"Error getting employer: {e}")

    try:
        creation_date = job.get('creationDate', None)

        if creation_date:
            if isinstance(creation_date, str):
                parsed_date = parse_datetime(creation_date)
                if not parsed_date:
                    print(f"Невірний формат дати для вакансії {job_info['id']}")
                    job_info['creationDate'] = None
            else:
                print(f"Невірний тип даних для creationDate: {type(creation_date)}")
                job_info['creationDate'] = None
        else:
            job_info['creationDate'] = None
    except KeyError as e:
        job_info['creationDate'] = None
        print(f"Error getting creationDate: {e}")


    try:
        job, created = Job.objects.get_or_create(
            title=job_info['title'],
            job_id=job_info['id'],
            description=job_info['description'],
            languages=job_info['availableLanguages'],
            number_of_posts=job_info['numberOfPosts'],
            location_map=job_info['locationMap'],
            job_categories=job_info['jobCategoriesCodes'],
            position_schedule=job_info['positionScheduleCodes'],
            employer=job_info['employer'],
            created_at=job_info['creationDate']
        )

        if created:
            print(f"✅ Вакансія ID: {job_info['id']} | {job_info['title']}, успішно додано.")
        else:
            print(f"🔄 Вакансія ID: {job_info['id']} | {job_info['title']}, вже існує.")
    except ValidationError as e:
        print(f"Помилка при додаванні вакансії: {e}")

    for key, value in job_info.items():
        print(f"{key}: {value}")
