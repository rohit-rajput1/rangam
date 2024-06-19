import openai
from django.conf import settings

# create a new variable for storing api key.
openai.api_key = settings.APIKEY

#Define your prompts list
prompts = [
    "Extract the key responsibilities from the job description.",
    "Identify the required skills and qualifications for this job.",
    "Suggest possible interview questions based on the job description.",
]

def send_job_description_to_api(job_description):
    try:
        # call the completion create method to send the job description to the api
        res = openai.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a experienced recruiter."},
                {"role": "user", "content": f"{job_description}"},
            ],
        )
        return res["choices"][0]["message"]["content"]
    except openai.error.APIError as e:
        raise ValueError(f"OpenAI API returned as API Error: {e}")
    except openai.error.APIConnectionError as e:
        raise ValueError(f"OpenAI API returned as API Connection Error: {e}")
    except openai.error.RateLimitError as e:
        raise ValueError(f"OpenAI API request exceeded the rate limit: {e}")          
    