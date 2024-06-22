import openai
import time
from django.conf import settings

# Set API key from Django settings
openai.api_key = settings.APIKEY

# Define your prompts dictionary
prompts = {
    "keySkills": "Identify the required skills and qualifications for this job.",
    "keyQuestions": "Suggest possible interview questions based on the job description.",
    "keyResponsibilities": "Extract the key responsibilities from the job description."
}

def send_job_description_to_api(job_description, prompt_type):
    retry_count = 0
    max_retries = 5
    
    if prompt_type not in prompts:
        raise ValueError(f"Invalid prompt type: {prompt_type}")
    
    prompt = prompts[prompt_type]
    
    while retry_count < max_retries:
        try:
            user_message = f"- {prompt}\n\n{job_description}"  # Create the full input message
            
            # Call the chat completion create method to send the job description to the API
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an experienced recruiter."},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=150,  # Set maximum number of tokens in the response
                stop=None,  # Optionally define stop sequences
                temperature=0.7,  # Control the randomness of the output
            )
            
            # Process the response to extract bullet points
            response = res["choices"][0]["message"]["content"]
            bullet_points = [point.strip("- ") for point in response.split("\n- ") if point.strip()]
            
            return bullet_points
        
        except openai.error.APIError as e:
            raise ValueError(f"OpenAI API returned an API Error: {e}")
        
        except openai.error.APIConnectionError as e:
            raise ValueError(f"OpenAI API returned an API Connection Error: {e}")
        
        except openai.error.RateLimitError as e:
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(2 ** retry_count)  # Exponential backoff
            else:
                raise ValueError(f"OpenAI API request exceeded the rate limit after {max_retries} retries: {e}")
        
        except openai.error.InvalidRequestError as e:
            raise ValueError(f"OpenAI API request was invalid: {e}")



# import openai
# from django.conf import settings

# # create a new variable for storing api key.
# openai.api_key = settings.APIKEY

# #Define your prompts list
# prompts = [
#     "Extract the key responsibilities from the job description.",
#     "Identify the required skills and qualifications for this job.",
#     "Suggest possible interview questions based on the job description.",
# ]

# def send_job_description_to_api(job_description):
#     try:
#         # call the completion create method to send the job description to the api
#         res = openai.Completion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a experienced recruiter."},
#                 {"role": "user", "content": f"{job_description}"},
#             ],
#         )
#         return res["choices"][0]["message"]["content"]
#     except openai.error.APIError as e:
#         raise ValueError(f"OpenAI API returned as API Error: {e}")
#     except openai.error.APIConnectionError as e:
#         raise ValueError(f"OpenAI API returned as API Connection Error: {e}")
#     except openai.error.RateLimitError as e:
#         raise ValueError(f"OpenAI API request exceeded the rate limit: {e}")          
    
# import openai
# import time
# from django.conf import settings

# # Create a new variable for storing API key
# openai.api_key = settings.APIKEY

# # Define your prompts list
# prompts = [
#     "Extract the key responsibilities from the job description.",
#     "Identify the required skills and qualifications for this job.",
#     "Suggest possible interview questions based on the job description.",
# ]

# def send_job_description_to_api(job_description):
#     retry_count = 0
#     max_retries = 5
    
#     while retry_count < max_retries:
#         try:
#             # Call the chat completion create method to send the job description to the API
#             res = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are an experienced recruiter."},
#                     {"role": "user", "content": job_description},
#                 ],
#                 max_tokens=150,  # Set maximum number of tokens in the response
#                 stop=None,  # Optionally define stop sequences
#                 temperature=0.7,  # Control the randomness of the output
#             )
#             return res["choices"][0]["message"]["content"]
        
#         except openai.error.APIError as e:
#             raise ValueError(f"OpenAI API returned an API Error: {e}")
        
#         except openai.error.APIConnectionError as e:
#             raise ValueError(f"OpenAI API returned an API Connection Error: {e}")
        
#         except openai.error.RateLimitError as e:
#             retry_count += 1
#             if retry_count < max_retries:
#                 time.sleep(2 ** retry_count)  # Exponential backoff
#             else:
#                 raise ValueError(f"OpenAI API request exceeded the rate limit after {max_retries} retries: {e}")
        
#         except openai.error.InvalidRequestError as e:
#             raise ValueError(f"OpenAI API request was invalid: {e}")

# import openai
# import time
# from django.conf import settings
# import random  # Import random module for selecting a prompt

# # Set API key from Django settings
# openai.api_key = settings.APIKEY

# # Define your prompts list
# prompts = [
#     "Extract the key responsibilities from the job description.",
#     "Identify the required skills and qualifications for this job.",
#     "Suggest possible interview questions based on the job description.",
# ]

# def send_job_description_to_api(job_description):
#     retry_count = 0
#     max_retries = 5
    
#     while retry_count < max_retries:
#         try:
#             # Randomly select a prompt for each part of the input
#             user_prompts = random.sample(prompts, 3)
            
#             # Create the full input message with prompts
#             user_message = "\n".join([f"- {prompt}" for prompt in user_prompts])
#             user_message += f"\n\n{job_description}"  # Append job description
            
#             # Call the chat completion create method to send the job description to the API
#             res = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are an experienced recruiter."},
#                     {"role": "user", "content": user_message},
#                 ],
#                 max_tokens=150,  # Set maximum number of tokens in the response
#                 stop=None,  # Optionally define stop sequences
#                 temperature=0.7,  # Control the randomness of the output
#             )
            
#             # Process the response to extract bullet points
#             response = res["choices"][0]["message"]["content"]
#             bullet_points = [point.strip("- ") for point in response.split("\n- ") if point.strip()]
            
#             return bullet_points
        
#         except openai.error.APIError as e:
#             raise ValueError(f"OpenAI API returned an API Error: {e}")
        
#         except openai.error.APIConnectionError as e:
#             raise ValueError(f"OpenAI API returned an API Connection Error: {e}")
        
#         except openai.error.RateLimitError as e:
#             retry_count += 1
#             if retry_count < max_retries:
#                 time.sleep(2 ** retry_count)  # Exponential backoff
#             else:
#                 raise ValueError(f"OpenAI API request exceeded the rate limit after {max_retries} retries: {e}")
        
#         except openai.error.InvalidRequestError as e:
#             raise ValueError(f"OpenAI API request was invalid: {e}")


