from http.client import responses

import requests
import time

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en-US;q=0.9,en;q=0.8,uk;q=0.7",
    "Connection": "keep-alive",
    "Cookie": "EURES_JVSE_SESSIONID=611A3287A599CF339A88B153894284CD; XSRF-TOKEN=48d19dbf-6e53-43df-bddb-1db1aca90e1f; _pk_ses.ba1b52b1-f8e5-42ec-93dc-088e1cd6d80f.53d5=*; _pk_id.ba1b52b1-f8e5-42ec-93dc-088e1cd6d80f.53d5=015d147e7af38d07.1741165734.2.1741176442.1741176322.; cck1=%7B%22cm%22%3Atrue%2C%22all1st%22%3Atrue%2C%22closed%22%3Afalse%7D",
    "Host": "europa.eu",
    "Referer": "https://europa.eu/eures/portal/jv-se/jv-details/MTE5NTYtMjIwODA1MTczOTc0NjgwMS1TIDE?lang=en",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

BASE_URL = "https://europa.eu/eures/eures-apps/searchengine/page/jv/id/{}?lang=en"

job_ids = [
    "MTE5NTYtMjIwODA1MTczOTc0NjgwMS1TIDE",
]

for job_id in job_ids:
    url = BASE_URL.format(job_id)
    lang = 'de'
    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            data = response.json()
            print(f"Отримано деталі для вакансії {job_id}")
            result = {}

            try:
                result['id'] = data.get("id", None)
            except KeyError as e:
                result['id'] = None
                print(f"Error while fetching `id`: {e}")

            try:
                result['reference'] = data.get("reference", None)
            except KeyError as e:
                result['reference'] = None
                print(f"Error while fetching `reference`: {e}")

            try:
                result['documentId'] = data.get("documentId", None)
            except KeyError as e:
                result['documentId'] = None
                print(f"Error while fetching `documentId`: {e}")

            try:
                result['creationDate'] = data.get("creationDate", None)
            except KeyError as e:
                result['creationDate'] = None
                print(f"Error while fetching `creationDate`: {e}")

            try:
                result['lastModificationDate'] = data.get("lastModificationDate", None)
            except KeyError as e:
                result['lastModificationDate'] = None
                print(f"Error while fetching `lastModificationDate`: {e}")

            try:
                result['preferredLanguage'] = data.get("preferredLanguage", None)
            except KeyError as e:
                result['preferredLanguage'] = None
                print(f"Error while fetching `preferredLanguage`: {e}")

            try:
                result['preferredLanguage'] = data.get("preferredLanguage", None)
            except KeyError as e:
                result['preferredLanguage'] = None
                print(f"Error while fetching `preferredLanguage`: {e}")

            # Із змінної lang

            try:
                result['languageVersion'] = data.get("jvProfiles", {}).get(lang, {}).get("languageVersion", None)
            except KeyError as e:
                result['languageVersion'] = None
                print(f"Error while fetching `languageVersion`: {e}")

            try:
                result['jobTitle'] = data.get("jvProfiles", {}).get(lang, {}).get("title", None)
            except KeyError as e:
                result['jobTitle'] = None
                print(f"Error while fetching `jobTitle`: {e}")

            try:
                result['positionScheduleCodes'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "positionScheduleCodes", [])
            except KeyError as e:
                result['positionScheduleCodes'] = []
                print(f"Error while fetching `positionScheduleCodes`: {e}")

            try:
                result['employmentPeriod'] = data.get("jvProfiles", {}).get(lang, {}).get("employmentPeriod", {})
            except KeyError as e:
                result['employmentPeriod'] = {}
                print(f"Error while fetching `employmentPeriod`: {e}")

            try:
                result['jobDescription'] = data.get("jvProfiles", {}).get(lang, {}).get("description", None)
            except KeyError as e:
                result['jobDescription'] = None
                print(f"Error while fetching `jobDescription`: {e}")

            try:
                result['requiredSkills'] = data.get("jvProfiles", {}).get(lang, {}).get("requiredSkills", [])
            except KeyError as e:
                result['requiredSkills'] = []
                print(f"Error while fetching `requiredSkills`: {e}")

            try:
                result['locations'] = data.get("jvProfiles", {}).get(lang, {}).get("locations", [{}])
            except KeyError as e:
                result['locations'] = [{}]
                print(f"Error while fetching `locations`: {e}")

            try:
                result['requiredEducationLevel'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "requiredEducationLevelCode", None)
            except KeyError as e:
                result['requiredEducationLevel'] = None
                print(f"Error while fetching `requiredEducationLevel`: {e}")

            try:
                result['requiredQualificationLevel'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "requiredQualificationLevelCode", None)
            except KeyError as e:
                result['requiredQualificationLevel'] = None
                print(f"Error while fetching `requiredQualificationLevel`: {e}")

            try:
                result['requiredYearsOfExperience'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "requiredYearsOfExperience", None)
            except KeyError as e:
                result['requiredYearsOfExperience'] = None
                print(f"Error while fetching `requiredYearsOfExperience`: {e}")

            try:
                result['requiredExperiences'] = data.get("jvProfiles", {}).get(lang, {}).get("requiredExperiences",
                                                                                             [{}])
            except KeyError as e:
                result['requiredExperiences'] = [{}]
                print(f"Error while fetching `requiredExperiences`: {e}")

            try:
                result['offeredRemunerationPackage'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "offeredRemunerationPackage", None)
            except KeyError as e:
                result['offeredRemunerationPackage'] = None
                print(f"Error while fetching 'offeredRemunerationPackage': {e}")

            try:
                result['requiredDrivingLicenses'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "requiredDrivingLicenses", [])
            except KeyError as e:
                result['requiredDrivingLicenses'] = []
                print(f"Error while fetching 'requiredDrivingLicenses': {e}")

            try:
                result['positionLanguages'] = data.get("jvProfiles", {}).get(lang, {}).get("positionLanguages", [{}])
            except KeyError as e:
                result['positionLanguages'] = [{}]
                print(f"Error while fetching 'positionLanguages': {e}")

            try:
                result['workingLanguageCodes'] = data.get("jvProfiles", {}).get(lang, {}).get("workingLanguageCodes",
                                                                                              [])
            except KeyError as e:
                result['workingLanguageCodes'] = []
                print(f"Error while fetching 'workingLanguageCodes': {e}")

            try:
                result['employer'] = data.get("jvProfiles", {}).get(lang, {}).get("employer", {})
            except KeyError as e:
                result['employer'] = {}
                print(f"Error while fetching 'employer': {e}")

            try:
                result['applicationInstructions'] = data.get("jvProfiles", {}).get(lang, {}).get(
                    "applicationInstructions", [])
            except KeyError as e:
                result['applicationInstructions'] = []
                print(f"Error while fetching 'applicationInstructions': {e}")

            try:
                result['personContacts'] = data.get("jvProfiles", {}).get(lang, {}).get("personContacts", [{}])
            except KeyError as e:
                result['personContacts'] = [{}]
                print(f"Error while fetching 'personContacts': {e}")

            try:
                result['lastApplicationDate'] = data.get("jvProfiles", {}).get(lang, {}).get("lastApplicationDate",
                                                                                             None)
            except KeyError as e:
                result['lastApplicationDate'] = None
                print(f"Error while fetching 'lastApplicationDate': {e}")

            try:
                result['travelPreference'] = data.get("jvProfiles", {}).get(lang, {}).get("travelPreference", None)
            except KeyError as e:
                result['travelPreference'] = None
                print(f"Error while fetching 'travelPreference': {e}")

            # [location.get("cityName", None) for location in data.get("jvProfiles", {}).get("de", {}).get("locations", [])],
            # [experience.get("description", None) for experience in data.get("jvProfiles", {}).get("de", {}).get("requiredExperiences", [])],
            for key, value in result.items():
                print(f"{key}: {value}")

        else:
            print(f"Помилка {response.status_code} при отриманні {job_id}")

    except requests.RequestException as e:
        print(f"Запит до {job_id} провалився: {e}")

    time.sleep(2)

# print(f"Отримано {len(job_details)} даних з вакансій.")
