from django.db import models

# Here we will put the input code as Job Description and the output code will be the extracted key responsibilities from the job description using the GPT-3.5 model.

class JobDescription(models.Model):
    _input_job_description = models.TextField()
    _output_response = models.TextField()

    class Meta:
        db_table = "job_description"