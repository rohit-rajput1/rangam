from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('OPENAI_API_KEY')

# Define your prompts list
prompts = [
    "Extract the key responsibilities from the job description.",
    "Identify the required skills and qualifications for this job.",
    "Suggest possible interview questions based on the job description.",
    # Add more prompts as needed
]

@api_view(['POST'])
def post_job_description(request):
    job_description = request.data.get('job_description')
    if not job_description:
        return Response({'error': 'job_description field is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Send job_description to OpenAI API with the maintained prompts
    results = []
    try:
        openai.api_key = api_key  # Use the api_key variable here
        for prompt in prompts:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prompt}\n\nJob Description:\n{job_description}"}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                n=1,
                temperature=0.7
            )
            result = response['choices'][0]['message']['content'].strip()
            # Convert the result to a list of points
            points = result.split("\n")
            # Remove any empty points
            points = [point for point in points if point.strip()]
            results.append(points)
    except openai.error.OpenAIError as e:
        # Handle specific OpenAI errors
        return Response({'error': f'OpenAI API Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'results': results}, status=status.HTTP_200_OK)
