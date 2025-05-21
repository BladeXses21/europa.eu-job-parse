import re
from load_django import *
from parser_app.models import Job, JobFullInfo, JobJson

jobs = JobJson.objects.filter(status='New')


def format_phone(numbers):
    if not numbers:
        return None
    num = numbers[0]
    return f"{num.get('countryDialing', '')} {num.get('areaDialing', '')} {num.get('dialNumber', '')}".strip()


def format_uri(items):
    if not items:
        return None
    return items[0].get("uri", None)


def format_salary(salaries):
    if not salaries:
        return None
    salary_info = salaries[0]
    minimum_salary = salary_info.get("minimumSalary", None)
    maximum_salary = salary_info.get("maximumSalary", None)
    currency_code = salary_info.get("currencyCode", "")

    salary_parts = []
    if minimum_salary is not None:
        salary_parts.append(f"{int(minimum_salary)}")
    if maximum_salary is not None:
        if minimum_salary is not None:
            salary_parts.append(f"- {int(maximum_salary)}")
        else:
            salary_parts.append(f"{int(maximum_salary)}")

    if not salary_parts:
        return None

    return " ".join(salary_parts) + (f" {currency_code}" if currency_code else "")


def clean_html(raw_html):
    clean_r = re.compile('<.*?>')
    cleantext = re.sub(clean_r, '', raw_html)
    return cleantext.strip()


for job in jobs:
    job_id = job.job_id
    if not job_id:
        continue

    json_data = job.json_data
    preferred_language = json_data.get("preferredLanguage", None)

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

    description_raw = jv_profile.get("description", None)
    description = clean_html(description_raw) if description_raw else None

    offered_remuneration = jv_profile.get("offeredRemunerationPackage", {}) or {}
    salaries = offered_remuneration.get("salaries", [])
    salary = format_salary(salaries)

    location_data = (jv_profile.get("locations", [{}]) or [{}])[0]
    location_region = location_data.get("region", None)
    location_city_name = location_data.get("cityName", None)
    location_postal_code = location_data.get("postalCode", None)
    location_address_lines = location_data.get("addressLines", None)

    employer_data = jv_profile.get("employer", {}) or {}
    employer_name = employer_data.get("name", None)
    employer_website = employer_data.get("website", None)
    employer_description = employer_data.get("description", None)
    employer_organisation_size = employer_data.get("organisationSizeCode", None)

    contact_data = (jv_profile.get("personContacts", [{}]) or [{}])[0]
    contact_given_name = contact_data.get("givenName", None)
    contact_family_name = contact_data.get("familyName", None)
    communications = contact_data.get("communications", {}) or {}

    address_data = (communications.get("addresses", [{}]) or [{}])[0]
    contact_country_code = address_data.get("countryCode", None)
    contact_region = address_data.get("region", None)
    contact_city_name = address_data.get("cityName", None)
    contact_postal_code = address_data.get("postalCode", None)
    contact_address_lines = address_data.get("addressLines", [])

    # format contact data
    contact_telephone_numbers = format_phone(communications.get("telephoneNumbers"))
    contact_mobile_telephone_numbers = format_phone(communications.get("mobileTelephoneNumbers"))

    contact_emails = format_uri(communications.get("emails"))

    obj, created = JobFullInfo.objects.get_or_create(
        job_id=job_id,
        defaults={
            "job_id": job.job_id,

            "preferred_language": preferred_language,

            "title": title,
            "description": description,

            "salary": salary,

            "location_region": location_region,
            "location_city_name": location_city_name,
            "location_postal_code": location_postal_code,
            "location_address_lines": location_address_lines,

            "employer_name": employer_name,
            "employer_website": employer_website,
            "employer_description": employer_description,
            "employer_organisation_size": employer_organisation_size,

            "contact_given_name": contact_given_name,
            "contact_family_name": contact_family_name,
            "contact_country_code": contact_country_code,
            "contact_region": contact_region,
            "contact_city_name": contact_city_name,
            "contact_postal_code": contact_postal_code,
            "contact_address_lines": contact_address_lines,

            "contact_telephone_numbers": contact_telephone_numbers,
            "contact_mobile_telephone_numbers": contact_mobile_telephone_numbers,
            "contact_emails": contact_emails,
        }
    )
    if created:
        print(f"Created JobFullInfo for job_id={job_id}")
        # job.status = 'Done'
        # job.save()
    else:
        print(f"JobFullInfo already exists for job_id={job_id}")
