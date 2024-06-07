import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobDescription

def preprocess_text(text):
    # Simple preprocessing: convert to lowercase and remove punctuation
    return re.sub(r'[^\w\s]', '', text.lower())

def load_prompts():
    file_path = '/home/rohit/Documents/Rangam/rangam_ai/prompts.txt'
    prompts = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                prompt = line.strip()
                if prompt:
                    prompts.append(prompt)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return prompts


def match_prompts(text, prompts):
    return [prompt for prompt in prompts if prompt.lower() in text]

class PostJobDescription(APIView):
    def post(self, request):
        file = request.FILES.get('file', None)
        if file is None:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Read the contents of the file
        job_description_text = file.read().decode('utf-8')

        # Load prompts from the file
        prompts = load_prompts()

        # Match prompts against the job description text
        matched_prompts = match_prompts(job_description_text, prompts)

        return Response({'matched_prompts': matched_prompts}, status=status.HTTP_200_OK)

class TestRecruiterBox(APIView):
    def post(self, request):
        job_description_id = request.data.get('job_description_id', None)
        if job_description_id is None:
            return Response({'error': 'No job description ID provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Load prompts from the file
            prompts = load_prompts()

            # Fetch the job description text based on the ID
            job_description = JobDescription.objects.get(id=job_description_id)

            # Match prompts against the job description text
            matched_prompts = match_prompts(job_description.description, prompts)

            return Response({'matched_prompts': matched_prompts}, status=status.HTTP_200_OK)

        except JobDescription.DoesNotExist:
            return Response({'error': 'Job description not found'}, status=status.HTTP_404_NOT_FOUND)
