import time

import requests
from load_django import *
from parser_app.models import Job

url = "https://europa.eu/eures/eures-apps/searchengine/page/jv-search/search"
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

for p in range(1, 1000):
    payload = {
        "resultsPerPage": 10,
        "page": p,
        "sortSearch": "BEST_MATCH",
        "keywords": [{"keyword": "Архитектор", "specificSearchCode": "EVERYWHERE"}],  # Request "Архитектор"
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

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        break

    data = response.json()
    jobs = data.get("jvs", [])
    # print(data)

    if not jobs:
        break

    for job in jobs:
        job_id = job.get('id', None)
        title = job.get('title', None)

        obj, created = Job.objects.get_or_create(
            job_id=job_id,
            title=title,
        )

        if created:
            print(f"New: {title} (ID: {job_id})")
        else:
            print(f"Pass: {title} (ID: {job_id})")

    # time.sleep(1)
