from django.shortcuts import render
import os
import time
from rest_framework.views import APIView
from rest_framework.decorators import api_view
import google.generativeai as genai
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
def read_file_from_local(path):
    """Reads the file from the local file system."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, 'r') as file:
        content = file.read()
    print(f"Read file '{os.path.basename(path)}' from local repository.")
    return content

@api_view(['POST'])
def answer(request):
  query = request.data.get('query', None)
  print(type(settings.GOOGLE_API_KEY))
  genai.configure(api_key=settings.GOOGLE_API_KEY)
  print(settings.GOOGLE_API_KEY)
  # Create the model
  generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
  }
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  # Read the file directly from the local repository
  file_content = read_file_from_local("./answer/Userfiles/annual_survey.csv")

  chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                file_content,
                "what is the content about",
            ],
        },

    ]
  )
  response = chat_session.send_message(query)

  print(response.text)
  return Response(response.text, status=status.HTTP_201_CREATED)
