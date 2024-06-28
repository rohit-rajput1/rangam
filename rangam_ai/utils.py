import openai
import time
from django.conf import settings

# Set API key from Django settings
openai.api_key = settings.APIKEY

# Define your prompts dictionary
prompts = {
    "keySkills": "Identify the required skills and qualifications for this job in bullet points.",
    "keyQuestions": "Suggest 5-6 possible interview questions based on the job description and provide answers.",
    "keyResponsibilities": "Extract the key responsibilities from the job description in bullet points."
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
            
            # Process the response to format it appropriately
            response = res["choices"][0]["message"]["content"]
            
            if prompt_type == "keySkills":
                bullet_points = [point.strip("- ") for point in response.split("\n- ") if point.strip()]
                return {"skills_and_qualifications": bullet_points}
            
            elif prompt_type == "keyQuestions":
                q_and_a = []
                items = response.split("\n\n")
                for i in range(0, len(items), 2):
                    if i + 1 < len(items):
                        question = items[i].replace("Question:", "").strip()
                        answer = items[i + 1].replace("Answer:", "").strip()
                        q_and_a.append({"Question": question, "Answer": answer})
                return {"questions_and_answers": q_and_a}
            
            elif prompt_type == "keyResponsibilities":
                responsibilities = [point.strip("- ") for point in response.split("\n- ") if point.strip()]
                return {"responsibilities": responsibilities}
        
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

