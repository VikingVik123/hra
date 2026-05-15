"""Recommendation service for generating interview questions using Google Generative AI."""

import json
import logging
import os
from typing import List

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Google Generative AI
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.warning("GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=api_key)
    logger.info("Google Generative AI configured successfully")


class RecommendationService:
    """Service for generating interview questions using AI.

    Attributes:
        context (str): System prompt for the AI model
        model: Google Generative AI model instance
    """

    SYSTEM_PROMPT = (
        "Assume you're a hiring manager. Return 3 thoughtful interview questions "
        "for the given job title. Your response must be a JSON object with a single "
        "key 'questions' containing a list of strings."
    )
    MODEL_NAME = "gemini-2.5-flash"

    def __init__(self):
        """Initialize the recommendation service."""
        self.context = self.SYSTEM_PROMPT
        try:
            self.model = genai.GenerativeModel(
                self.MODEL_NAME,
                generation_config={"response_mime_type": "application/json"},
            )
            logger.info(f"RecommendationService initialized with model {self.MODEL_NAME}")
        except Exception as e:
            logger.error(f"Failed to initialize GenerativeModel: {e}")
            raise

    def fetch_recs(self, job_title: str) -> List[str]:
        """Generate interview questions for a given job title.

        Args:
            job_title (str): The job position to generate questions for

        Returns:
            List[str]: List of interview questions

        Raises:
            ValueError: If job_title is empty or invalid
            Exception: If AI generation fails
        """
        if not job_title or not job_title.strip():
            logger.warning("Empty job_title provided to fetch_recs")
            raise ValueError("job_title cannot be empty")

        job_title = job_title.strip()
        logger.info(f"Generating recommendations for job title: {job_title}")

        try:
            prompt = f"{self.context} for {job_title}"
            res = self.model.generate_content(prompt)
            data = json.loads(res.text)
            questions = data.get("questions", [])

            logger.info(f"Successfully generated {len(questions)} questions for {job_title}")
            return questions

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise Exception(f"Invalid response format from AI model: {str(e)}")
        except Exception as e:
            logger.error(f"AI generation failed for job_title '{job_title}': {e}")
            raise Exception(f"AI Generation failed: {str(e)}")