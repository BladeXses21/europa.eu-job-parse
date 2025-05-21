from django.db import models


# Create your models here.

class Job(models.Model):
    status = models.CharField(max_length=20, default="New")

    job_id = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)


class JobJson(models.Model):
    job_id = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)

    json_data = models.JSONField(blank=True, null=True)

    status = models.CharField(max_length=20, default="New")


class JobFullInfo(models.Model):
    job_id = models.CharField(max_length=255, null=True, blank=True)

    preferred_language = models.CharField(max_length=10, blank=True, null=True)

    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    salary = models.CharField(max_length=255, blank=True, null=True)

    location_region = models.CharField(max_length=255, blank=True, null=True)
    location_city_name = models.CharField(max_length=255, blank=True, null=True)
    location_postal_code = models.CharField(max_length=20, blank=True, null=True)
    location_address_lines = models.JSONField(blank=True, null=True)

    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_website = models.URLField(blank=True, null=True)
    employer_description = models.TextField(blank=True, null=True)
    employer_organisation_size = models.CharField(max_length=255, blank=True, null=True)

    contact_given_name = models.CharField(max_length=255, blank=True, null=True)
    contact_family_name = models.CharField(max_length=255, blank=True, null=True)
    contact_country_code = models.CharField(max_length=10, blank=True, null=True)
    contact_region = models.CharField(max_length=255, blank=True, null=True)
    contact_city_name = models.CharField(max_length=255, blank=True, null=True)
    contact_postal_code = models.CharField(max_length=20, blank=True, null=True)
    contact_address_lines = models.JSONField(blank=True, null=True)

    contact_telephone_numbers = models.CharField(max_length=200, blank=True, null=True)
    contact_mobile_telephone_numbers = models.JSONField(blank=True, null=True)
    contact_emails = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(max_length=20, default="New")


class JobInfo(models.Model):
    job_id = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=525, blank=True, null=True)

    company = models.CharField(max_length=525, blank=True, null=True) # employer[name]
    website = models.CharField(max_length=525, blank=True, null=True) # employer[website]
    country = models.CharField(max_length=525, blank=True, null=True) # locations[countryCode]

    full_name = models.CharField(max_length=525, blank=True, null=True) # personContacts[givenName] + personContacts[familyName]
    givenName = models.CharField(max_length=525, blank=True, null=True)
    familyName = models.CharField(max_length=525, blank=True, null=True)

    salary = models.CharField(max_length=525, blank=True, null=True)
    email = models.CharField(max_length=525, blank=True, null=True)
    phone = models.CharField(max_length=525, blank=True, null=True)
    description = models.TextField(blank=True, null=True) # no HTML code

    link = models.CharField(max_length=525, blank=True, null=True)

    status = models.CharField(max_length=20, default="New")


class Final(models.Model):
    job_id = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=525, blank=True, null=True)

    company = models.CharField(max_length=525, blank=True, null=True) # employer[name]
    website = models.CharField(max_length=525, blank=True, null=True) # employer[website]
    country = models.CharField(max_length=525, blank=True, null=True) # locations[countryCode]

    full_name = models.CharField(max_length=525, blank=True, null=True) # personContacts[givenName] + personContacts[familyName]
    givenName = models.CharField(max_length=525, blank=True, null=True)
    familyName = models.CharField(max_length=525, blank=True, null=True)

    salary = models.CharField(max_length=525, blank=True, null=True)
    email = models.CharField(max_length=525, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=525, blank=True, null=True)
    description = models.TextField(blank=True, null=True) # no HTML code

    link = models.CharField(max_length=525, blank=True, null=True)

    status = models.CharField(max_length=20, default="New")