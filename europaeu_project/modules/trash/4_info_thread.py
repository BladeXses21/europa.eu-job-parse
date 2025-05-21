import re
from load_django import *
from parser_app.models import JobJson, JobInfo
from concurrent import futures

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

def process_job(job):
    job_id = job.job_id
    if not job_id:
        return

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

    locations = jv_profile.get("locations", []) or []
    location_country_code = locations[0].get("countryCode", None) if locations else None

    employer_data = jv_profile.get("employer", {}) or {}
    employer_name = employer_data.get("name", None)
    employer_website = employer_data.get("website", None)

    contact_data = (jv_profile.get("personContacts", [{}]) or [{}])[0]
    contact_given_name = contact_data.get("givenName", None)
    contact_family_name = contact_data.get("familyName", None)

    communications = contact_data.get("communications", {}) or {}
    contact_emails = format_uri(communications.get("emails"))
    contact_phone = format_phone(communications.get("telephoneNumbers"))

    link = f"https://europa.eu/eures/portal/jv-se/jv-details/{job_id}?lang=en"

    obj, created = JobInfo.objects.get_or_create(
        job_id=job_id,
        defaults={
            "job_id": job_id,
            "title": title,
            "company": employer_name,
            "website": employer_website,
            "country": location_country_code,
            "full_name": f"{contact_given_name or ''} {contact_family_name or ''}".strip(),
            "givenName": contact_given_name,
            "familyName": contact_family_name,
            "salary": salary,
            "email": contact_emails,
            "phone": contact_phone,
            "description": description,
            "link": link,
        }
    )

    if created:
        print(f"Created JobInfo for job_id={job_id}")
    else:
        print(f"JobInfo already exists for job_id={job_id}")

with futures.ThreadPoolExecutor(20) as executor:
    executor.map(process_job, jobs)