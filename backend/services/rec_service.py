"""Recommendation service for generating interview questions using AI models.

Supports multiple AI providers: Google Generative AI (Gemini) and Groq.
"""

import json
import logging
import os
from typing import List, Dict

import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Configure Google Generative AI
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logger.warning("GEMINI_API_KEY not found in environment variables")
else:
    genai.configure(api_key=gemini_api_key)
    logger.info("Google Generative AI configured successfully")

# Configure Groq
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    logger.warning("GROQ_API_KEY not found in environment variables")
else:
    logger.info("Groq API key configured successfully")


class RecommendationService:
    """Service for generating interview questions using AI.

    Supports both Gemini (Google) and Groq models.

    Attributes:
        context (str): System prompt for the AI model
    """

    SYSTEM_PROMPT = (
        "Assume you're a hiring manager. Return 3 thoughtful interview questions "
        "for the given job title. Your response must be a JSON object with a single "
        "key 'questions' containing a list of strings."
    )
    GEMINI_MODEL = "gemini-2.5-flash"
    GROQ_MODEL = "llama-3.3-70b-versatile"

    def __init__(self):
        """Initialize the recommendation service."""
        self.context = self.SYSTEM_PROMPT
        self.gemini_model = None
        self.groq_client = None

        # Initialize Gemini
        try:
            self.gemini_model = genai.GenerativeModel(
                self.GEMINI_MODEL,
                generation_config={"response_mime_type": "application/json"},
            )
            logger.info(f"Gemini model {self.GEMINI_MODEL} initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")

        # Initialize Groq
        try:
            if groq_api_key:
                self.groq_client = Groq(api_key=groq_api_key)
                logger.info(f"Groq client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")

    def _categorize_question(self, question: str) -> str:
        """Categorize a question based on keyword matching.

        Args:
            question (str): The question text to categorize

        Returns:
            str: The category of the question
        """
        question_lower = question.lower()

        # Category keywords mapping
        categories = {
            "technical-skills": [
                "technical",
                "technology",
                "programming",
                "coding",
                "framework",
                "language",
                "database",
                "architecture",
                "algorithm",
                "system design",
            ],
            "problem-solving": [
                "problem",
                "solve",
                "approach",
                "challenge",
                "solution",
                "troubleshoot",
                "debug",
                "overcome",
            ],
            "teamwork": [
                "team",
                "collaborate",
                "communication",
                "conflict",
                "cooperation",
                "cross-team",
                "work together",
                "stakeholder",
            ],
            "leadership": [
                "lead",
                "leadership",
                "manage",
                "mentor",
                "responsibility",
                "initiative",
                "project",
                "team lead",
            ],
            "time-management": [
                "prioritize",
                "deadline",
                "time",
                "fast-paced",
                "urgent",
                "schedule",
                "organize",
            ],
            "learning": [
                "learn",
                "stay updated",
                "industry trends",
                "growth",
                "development",
                "knowledge",
                "skill",
            ],
            "metrics": [
                "metric",
                "measure",
                "success",
                "kpi",
                "data",
                "analyze",
                "performance",
            ],
            "decision-making": [
                "decision",
                "choose",
                "prioritize",
                "trade-off",
                "align",
                "objective",
                "goal",
            ],
        }

        # Find the category with the most keyword matches
        max_matches = 0
        best_category = "general"

        for category, keywords in categories.items():
            matches = sum(1 for keyword in keywords if keyword in question_lower)
            if matches > max_matches:
                max_matches = matches
                best_category = category

        return best_category

    def _add_metadata_to_questions(self, questions: List[str]) -> List[Dict]:
        """Add ID and category metadata to questions.

        Args:
            questions (List[str]): Raw question texts

        Returns:
            List[Dict]: Questions with id and category
        """
        enriched_questions = []
        for idx, question in enumerate(questions, 1):
            enriched_questions.append(
                {
                    "id": idx,
                    "text": question,
                    "category": self._categorize_question(question),
                }
            )
        return enriched_questions

    def fetch_recs(self, job_title: str, model: str = "gemini") -> List[Dict]:
        """Generate interview questions for a given job title.

        Args:
            job_title (str): The job position to generate questions for
            model (str): AI model to use - either 'gemini' or 'groq' (default: 'gemini')

        Returns:
            List[Dict]: List of interview questions with metadata (id, text, category)

        Raises:
            ValueError: If job_title is empty, invalid, or model is unsupported
            Exception: If AI generation fails
        """
        if not job_title or not job_title.strip():
            logger.warning("Empty job_title provided to fetch_recs")
            raise ValueError("job_title cannot be empty")

        job_title = job_title.strip()
        model = model.lower().strip()

        if model not in ["gemini", "groq"]:
            logger.warning(f"Unsupported model requested: {model}")
            raise ValueError(f"Unsupported model: {model}. Use 'gemini' or 'groq'")

        logger.info(f"Generating recommendations for job title: {job_title} using {model}")

        try:
            if model == "gemini":
                return self._fetch_gemini(job_title)
            else:  # groq
                return self._fetch_groq(job_title)

        except Exception as e:
            logger.error(f"AI generation failed for job_title '{job_title}': {e}")
            raise Exception(f"AI Generation failed: {str(e)}")

    def _fetch_gemini(self, job_title: str) -> List[Dict]:
        """Generate questions using Gemini model.

        Args:
            job_title (str): The job position to generate questions for

        Returns:
            List[Dict]: List of interview questions with metadata

        Raises:
            Exception: If Gemini model is not available or generation fails
        """
        if not self.gemini_model:
            raise Exception("Gemini model not initialized. Check GEMINI_API_KEY.")

        try:
            prompt = f"{self.context} for {job_title}"
            res = self.gemini_model.generate_content(prompt)
            data = json.loads(res.text)
            questions = data.get("questions", [])

            # Add metadata to questions
            enriched_questions = self._add_metadata_to_questions(questions)
            logger.info(f"Successfully generated {len(enriched_questions)} questions using Gemini")
            return enriched_questions

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            raise Exception(f"Invalid response format from Gemini: {str(e)}")

    def _fetch_groq(self, job_title: str) -> List[Dict]:
        """Generate questions using Groq model.

        Args:
            job_title (str): The job position to generate questions for

        Returns:
            List[Dict]: List of interview questions with metadata

        Raises:
            Exception: If Groq client is not available or generation fails
        """
        if not self.groq_client:
            raise Exception("Groq client not initialized. Check GROQ_API_KEY.")

        try:
            prompt = f"{self.context} for {job_title}"
            message = self.groq_client.chat.completions.create(
                model=self.GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": self.context,
                    },
                    {
                        "role": "user",
                        "content": f"Generate interview questions for: {job_title}",
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            response_text = message.choices[0].message.content
            data = json.loads(response_text)
            questions = data.get("questions", [])

            # Add metadata to questions
            enriched_questions = self._add_metadata_to_questions(questions)
            logger.info(f"Successfully generated {len(enriched_questions)} questions using Groq")
            return enriched_questions

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {e}")
            raise Exception(f"Invalid response format from Groq: {str(e)}")