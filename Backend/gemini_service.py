import json
import time
import asyncio
import google.generativeai as genai
from typing import Dict, Any

class GeminiService:
    def __init__(self, api_key: str, faq_data_path: str = "Company_data.json"):
        """Initialize Gemini service with company context"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Load company data
        with open(faq_data_path, 'r', encoding='utf-8') as f:
            self.faq_data = json.load(f)
        
        # Initialize Gemini model (latest model)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create custom prompt
        self.custom_prompt = self._create_custom_prompt()
        
        print("Gemini service initialized with company context")
    
    def _create_custom_prompt(self) -> str:
        """Create custom prompt with company context"""
        company_info = self.faq_data.get("company", {})
        
        prompt = f"""
You are Kan-guroo, a friendly and knowledgeable customer care agent for {company_info.get('name', 'Kan-Guroo')}.

Company Information:
- Name: {company_info.get('name', 'Kan-Guroo')}
- Website: {company_info.get('website', 'https://www.kan-guroo.com')}
- Description: {company_info.get('description', '')}
- Mission: {company_info.get('mission', '')}
- Vision: {company_info.get('vision', '')}

Available Programs:
"""
        
        # Add programs information
        programs = company_info.get('programs', {})
        for program_type, program_list in programs.items():
            prompt += f"\n{program_type.replace('_', ' ').title()}:\n"
            for program in program_list:
                prompt += f"- {program['name']}: {program['description']}\n"
                if 'url' in program:
                    prompt += f"  URL: {program['url']}\n"
        
        prompt += f"""
Team Information:
"""
        
        # Add team information
        team = company_info.get('team', [])
        for member in team:
            prompt += f"- {member['name']}: {member['role']}\n"
        
        prompt += f"""
Contact Information:
- Phone: {company_info.get('contact', {}).get('phone', 'N/A')}
- Email: {company_info.get('contact', {}).get('email', 'N/A')}

Your Role as Kan-guroo:
1. You are an enthusiastic and helpful customer care agent
2. Answer questions about our educational programs and services
3. Be encouraging and positive about our programs
4. If asked about specific courses/programs, mention how they've helped many students
5. Keep responses SHORT and CONCISE (1-2 sentences maximum)
6. Always be helpful and supportive
7. You have access to team information, company details, and all program information
8. IMPORTANT: Keep responses under 80 words for faster voice generation
9. Be direct and to the point while *maintaining enthusiasm*
10. When asked about founders, CEO, CTO, or team members, ALWAYS use the team information provided above
11. If asked "Who's your CEO?" answer with the actual CEO name from the team information
12. If asked about founders or team, provide the specific names and roles from the team information

Examples:
- "Who's your CEO?" → "Our CEO is Otari Melanashvili, who is also our Co-Founder!"
- "Who are the founders?" → "Our founders are Otari Melanashvili (CEO), Saba Gelashvili, and Lasha Bevia!"

User Question: """
        
        return prompt
    
    async def generate_response(self, user_question: str) -> str:
        """Generate response using Gemini with custom prompt"""
        start_time = time.time()
        print(f"🤖 Gemini response started [{time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z]")
        
        try:
            # Create the full prompt
            full_prompt = self.custom_prompt + user_question
            
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt
            )
            
            # Extract text from response
            if response and response.text:
                response_text = response.text.strip()
            else:
                response_text = "I apologize, but I couldn't generate a response. Please try rephrasing your question or contact our support team."
            
            # Log performance
            elapsed_time = (time.time() - start_time) * 1000
            print(f"✅ Gemini response completed in {elapsed_time:.3f}ms")
            
            return response_text
            
        except Exception as e:
            print(f"Error in Gemini service: {e}")
            return "I'm sorry, I encountered an error processing your request. Please try again or contact our support team."
    
    def get_faq_context(self) -> str:
        """Get FAQ context for debugging"""
        return json.dumps(self.faq_data, indent=2)
