from django.db import models

class JobDescription(models.Model):
    _input_job_description = models.TextField()
    _output_response = models.TextField()

    class Meta:
        db_table = "job_description"

class JobSkillsRequired(models.Model):
    _input_job_description = models.TextField()
    _output_response = models.TextField()

    class Meta:
        db_table = "job_skills_required"

class JobQuestionsRequired(models.Model):
    _input_job_description = models.TextField()
    _output_response = models.TextField()

    class Meta:
        db_table = "job_questions_required"

class JobKeyResponsibilitiesRequired(models.Model):
    _input_job_description = models.TextField()
    _output_response = models.TextField()

    class Meta:
        db_table = "job_key_responsibilities_required"
