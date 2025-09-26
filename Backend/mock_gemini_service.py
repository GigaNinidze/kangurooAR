#!/usr/bin/env python3
"""
Mock Gemini service for testing when API quota is exceeded
"""
import json
import time
import asyncio
from typing import Dict, Any

class MockGeminiService:
    def __init__(self, api_key: str, faq_data_path: str = "Company_data.json"):
        """Initialize mock Gemini service"""
        self.api_key = api_key
        
        # Load company data
        with open(faq_data_path, 'r', encoding='utf-8') as f:
            self.faq_data = json.load(f)
        
        print("Mock Gemini service initialized with company context")
    
    async def generate_response(self, user_question: str) -> str:
        """Generate mock response based on user question"""
        start_time = time.time()
        
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        # Generate contextual responses based on the question
        question_lower = user_question.lower()
        
        if "who" in question_lower and ("ceo" in question_lower or "founder" in question_lower):
            response = "Our CEO is Otari Melanashvili, who is also our Co-Founder! We also have Saba Gelashvili and Lasha Bevia as Co-Founders."
        elif "program" in question_lower or "course" in question_lower:
            response = "We offer amazing programs including High School USA, High School Europe, Bachelor Abroad, Master Abroad, PhD Abroad, and language courses in English and German!"
        elif "language" in question_lower:
            response = "We offer English Language Courses, German Language Courses, and other language courses in different countries. Contact us to learn more!"
        elif "exchange" in question_lower:
            response = "We have fantastic exchange programs! High School USA for 1-year programs in U.S. public schools, and High School Europe for European countries."
        elif "contact" in question_lower or "phone" in question_lower or "email" in question_lower:
            response = "You can reach us at +995 577 30 25 25 or email us at info@kan-guroo.com. We'd love to help you with your educational journey!"
        elif "hello" in question_lower or "hi" in question_lower:
            response = "Hello! Welcome to Kan-Guroo! I'm here to help you discover amazing educational opportunities worldwide. What would you like to know?"
        else:
            response = "Thank you for your question! Kan-Guroo helps students discover exchange programs and create successful futures. We offer programs in the USA, Europe, and worldwide. How can I assist you today?"
        
        # Log performance
        elapsed_time = (time.time() - start_time) * 1000
        print(f"Mock Gemini response time: {elapsed_time:.3f}ms")
        
        return response
    
    def get_faq_context(self) -> str:
        """Get FAQ context for debugging"""
        return json.dumps(self.faq_data, indent=2)
