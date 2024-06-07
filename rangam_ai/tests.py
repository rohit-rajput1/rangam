from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
import openai

class PostJobDescriptionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('post_job_description')
        self.valid_payload = {'job_description': 'Your job description here'}

    @patch('openai.ChatCompletion.create')
    def test_post_job_description_success(self, mock_create):
        mock_create.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Mock response content.\nPoint 1\nPoint 2'
                    }
                }
            ]
        }
        response = self.client.post(self.url, self.valid_payload, content_type='application/json')
        print("Response Data (Success Test):", response.json())  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.json())
        # We have three prompts, so we should expect three results
        expected_results = [
            ['Mock response content.', 'Point 1', 'Point 2'],
            ['Mock response content.', 'Point 1', 'Point 2'],
            ['Mock response content.', 'Point 1', 'Point 2']
        ]
        self.assertEqual(response.json()['results'], expected_results)

    def test_post_job_description_missing_field(self):
        response = self.client.post(self.url, {}, content_type='application/json')
        print("Response Data (Missing Field Test):", response.json())  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.json())

    @patch('openai.ChatCompletion.create')
    def test_post_job_description_quota_exceeded(self, mock_create):
        mock_create.side_effect = openai.error.RateLimitError('You exceeded your current quota.')
        response = self.client.post(self.url, self.valid_payload, content_type='application/json')
        print("Response Data (Quota Exceeded Test):", response.json())  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'OpenAI API Error: You exceeded your current quota.')
