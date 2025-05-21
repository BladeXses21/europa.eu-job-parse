import json
from load_django import *
from parser_app.models import Job, JobData


def parse_jobs():
    jobs = Job.objects.all()

    for job in jobs:
        if not job.json_data:
            continue

        if isinstance(job.json_data, str):
            json_data = json.loads(job.json_data)
        else:
            json_data = job.json_data

        external_id = json_data.get("id", None)
        creation_date = json_data.get("creationDate", None)
        last_modification_date = json_data.get("lastModificationDate", None)
        title = json_data.get("title", None)
        description = json_data.get("description", None)
        number_of_posts = json_data.get("numberOfPosts", None)

        location_map = json_data.get("locationMap", {})
        location = None
        if "NO" in location_map:
            location_list = location_map.get("NO", None)
            if isinstance(location_list, list) and location_list:
                location = location_list[0]

        eures_flag = json_data.get("euresFlag", None)
        job_categories_codes = json_data.get("jobCategoriesCodes", None)
        position_schedule_codes = json_data.get("positionScheduleCodes", None)
        position_offering_code = json_data.get("positionOfferingCode", None)
        available_languages = json_data.get("availableLanguages", None)
        score = json_data.get("score", None)

        if isinstance(available_languages, list):
            available_languages = ", ".join(available_languages)

        employer_info = json_data.get("employer", {})
        employer_name = employer_info.get("name", None)
        employer_website = employer_info.get("website", None)
        employer_description = employer_info.get("description", None)
        employer_legal_id = employer_info.get("legalID", None)
        organisation_size_code = employer_info.get("organisationSizeCode", None)
        organisation_ownership_type_code = employer_info.get("organisationOwnershipTypeCode", None)
        sector_codes = employer_info.get("sectorCodes", None)
        if isinstance(sector_codes, list):
            sector_codes = ", ".join(sector_codes)

        obj, created = JobData.objects.get_or_create(
            job_id=job.job_id,
            employer=employer_name or job.employer,
            defaults={
                "title": title,
                "description": description,
                "number_of_posts": number_of_posts,
                "location": location,
                "employer_website": employer_website,
                "employer_description": employer_description,
                "available_languages": available_languages,
                "creation_date": creation_date,
                "last_modification_date": last_modification_date,
                "eures_flag": eures_flag,
                "job_categories_codes": job_categories_codes,
                "position_schedule_codes": position_schedule_codes,
                "position_offering_code": position_offering_code,
                "employer_legal_id": employer_legal_id,
                "score": score,
            }
        )

        if created:
            print(f"Додано: {external_id})")
        else:
            print(f"Вже існує: {external_id})")

if __name__ == "__main__":
    parse_jobs()
