#!/usr/bin/env python3
"""
Session Analyzer - Evaluates customer interaction sessions
Analyzes saved session files and generates insights using AI
"""

import os
import json
import asyncio
import glob
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

class SessionAnalyzer:
    def __init__(self, api_key: str):
        """Initialize session analyzer with Gemini API"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # Analysis prompt template
        self.analysis_prompt = """
You are a customer service quality analyst.professional quality analyst.
Analyze this customer support session and provide insights.

Session Data:
{session_data}

Please analyze and provide the following information in JSON format:

{{
    "session_id": "session_id_here",
    "overall_rating": "1-10",
    "issue_resolved": true/false,
    "customer_satisfaction": "high/medium/low",
    "response_time_quality": "fast/medium/slow",
    "troubleshooting_effectiveness": "effective/partially_effective/ineffective",
    "communication_quality": "excellent/good/fair/poor",
    "key_issues": ["list", "of", "main", "issues"],
    "resolution_steps": ["step1", "step2", "step3"],
    "customer_sentiment": "positive/neutral/negative",
    "escalation_needed": true/false,
    "improvement_suggestions": ["suggestion1", "suggestion2"],
    "session_summary": "Brief summary of the interaction"
}}

Focus on:
1. Whether the customer's issue was actually resolved
2. Quality of troubleshooting steps
3. Communication effectiveness
4. Customer satisfaction indicators
5. Areas for improvement
"""

    def load_session_file(self, filepath: str) -> Dict[str, Any]:
        """Load and parse a session file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse session metadata
            lines = content.split('\n')
            session_data = {
                'filepath': filepath,
                'session_id': '',
                'language': '',
                'start_time': '',
                'end_time': '',
                'duration': '',
                'issue_type': '',
                'resolution_status': '',
                'troubleshooting_attempts': 0,
                'failed_attempts': 0,
                'escalation_triggered': False,
                'conversation_history': []
            }
            
            # Extract metadata
            for line in lines:
                if line.startswith('Session ID:'):
                    session_data['session_id'] = line.split(':', 1)[1].strip()
                elif line.startswith('Language:'):
                    session_data['language'] = line.split(':', 1)[1].strip()
                elif line.startswith('Start Time:'):
                    session_data['start_time'] = line.split(':', 1)[1].strip()
                elif line.startswith('End Time:'):
                    session_data['end_time'] = line.split(':', 1)[1].strip()
                elif line.startswith('Duration:'):
                    session_data['duration'] = line.split(':', 1)[1].strip()
                elif line.startswith('Issue Type:'):
                    session_data['issue_type'] = line.split(':', 1)[1].strip()
                elif line.startswith('Resolution Status:'):
                    session_data['resolution_status'] = line.split(':', 1)[1].strip()
                elif line.startswith('Troubleshooting Attempts:'):
                    session_data['troubleshooting_attempts'] = int(line.split(':', 1)[1].strip())
                elif line.startswith('Failed Attempts:'):
                    session_data['failed_attempts'] = int(line.split(':', 1)[1].strip())
                elif line.startswith('Escalation Triggered:'):
                    session_data['escalation_triggered'] = line.split(':', 1)[1].strip().lower() == 'true'
            
            # Extract conversation history
            in_conversation = False
            current_message = {}
            
            for line in lines:
                if line.strip() == '=== CONVERSATION HISTORY ===':
                    in_conversation = True
                    continue
                
                if in_conversation and line.strip():
                    if line.startswith('[') and '] User:' in line:
                        if current_message:
                            session_data['conversation_history'].append(current_message)
                        timestamp = line.split(']')[0][1:]
                        message = line.split('] User: ')[1]
                        current_message = {
                            'timestamp': timestamp,
                            'user': message,
                            'bot': ''
                        }
                    elif line.startswith('[') and '] Bot:' in line:
                        if current_message:
                            timestamp = line.split(']')[0][1:]
                            message = line.split('] Bot: ')[1]
                            current_message['bot'] = message
            
            # Add the last message if exists
            if current_message and current_message.get('bot'):
                session_data['conversation_history'].append(current_message)
            
            return session_data
            
        except Exception as e:
            print(f"Error loading session file {filepath}: {e}")
            return None

    async def analyze_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single session using AI"""
        try:
            # Format session data for analysis
            formatted_data = f"""
Session ID: {session_data['session_id']}
Language: {session_data['language']}
Duration: {session_data['duration']}
Issue Type: {session_data['issue_type']}
Resolution Status: {session_data['resolution_status']}
Troubleshooting Attempts: {session_data['troubleshooting_attempts']}
Failed Attempts: {session_data['failed_attempts']}
Escalation Triggered: {session_data['escalation_triggered']}

Conversation:
"""
            
            for msg in session_data['conversation_history']:
                formatted_data += f"[{msg['timestamp']}] User: {msg['user']}\n"
                formatted_data += f"[{msg['timestamp']}] Bot: {msg['bot']}\n\n"
            
            # Create analysis prompt
            prompt = self.analysis_prompt.format(session_data=formatted_data)
            
            # Get AI analysis
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            if response and response.text:
                # Try to parse JSON response
                try:
                    # First, try to parse as-is
                    analysis = json.loads(response.text.strip())
                    analysis['session_id'] = session_data['session_id']
                    analysis['filepath'] = session_data['filepath']
                    return analysis
                except json.JSONDecodeError:
                    # Try to extract JSON from markdown code blocks
                    try:
                        import re
                        # Look for JSON content between ```json and ```
                        json_match = re.search(r'```json\s*(.*?)\s*```', response.text, re.DOTALL)
                        if json_match:
                            json_content = json_match.group(1).strip()
                            analysis = json.loads(json_content)
                            analysis['session_id'] = session_data['session_id']
                            analysis['filepath'] = session_data['filepath']
                            return analysis
                    except (json.JSONDecodeError, AttributeError):
                        pass
                    
                    # If all parsing attempts fail, return raw text
                    return {
                        'session_id': session_data['session_id'],
                        'filepath': session_data['filepath'],
                        'raw_analysis': response.text.strip(),
                        'analysis_error': 'Could not parse JSON response'
                    }
            else:
                return {
                    'session_id': session_data['session_id'],
                    'filepath': session_data['filepath'],
                    'analysis_error': 'No response from AI'
                }
                
        except Exception as e:
            return {
                'session_id': session_data['session_id'],
                'filepath': session_data['filepath'],
                'analysis_error': str(e)
            }

    def get_all_session_files(self, sessions_dir: str = "../sessions") -> List[str]:
        """Get all session files in the sessions directory"""
        pattern = os.path.join(sessions_dir, "*.txt")
        return glob.glob(pattern)

    async def analyze_all_sessions(self, sessions_dir: str = "../sessions") -> List[Dict[str, Any]]:
        """Analyze all sessions in the directory"""
        session_files = self.get_all_session_files(sessions_dir)
        print(f"🔍 Found {len(session_files)} session files to analyze")
        
        results = []
        
        for filepath in session_files:
            print(f"📄 Analyzing {os.path.basename(filepath)}...")
            
            # Load session data
            session_data = self.load_session_file(filepath)
            if not session_data:
                continue
            
            # Analyze session
            analysis = await self.analyze_session(session_data)
            results.append(analysis)
            
            print(f"✅ Completed analysis for {session_data['session_id']}")
        
        return results

    def save_analysis_report(self, analyses: List[Dict[str, Any]], output_file: str = None):
        """Save analysis results to a report file"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"analysis_report_{timestamp}.json"
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        output_path = os.path.join("reports", output_file)
        
        # Prepare report data
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'total_sessions': len(analyses),
            'analyses': analyses,
            'summary': self.generate_summary(analyses)
        }
        
        # Save report
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Analysis report saved to {output_path}")
        return output_path

    def extract_metrics_from_raw_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metrics from raw analysis text when JSON parsing failed"""
        import re
        
        metrics = {
            'issue_resolved': False,
            'customer_satisfaction': 'unknown',
            'overall_rating': 0
        }
        
        if 'raw_analysis' in analysis:
            raw_text = analysis['raw_analysis']
            
            # Extract issue_resolved
            issue_resolved_match = re.search(r'"issue_resolved":\s*(true|false)', raw_text, re.IGNORECASE)
            if issue_resolved_match:
                metrics['issue_resolved'] = issue_resolved_match.group(1).lower() == 'true'
            
            # Extract customer_satisfaction
            satisfaction_match = re.search(r'"customer_satisfaction":\s*"([^"]+)"', raw_text, re.IGNORECASE)
            if satisfaction_match:
                metrics['customer_satisfaction'] = satisfaction_match.group(1).lower()
            
            # Extract overall_rating
            rating_match = re.search(r'"overall_rating":\s*"(\d+)"', raw_text, re.IGNORECASE)
            if rating_match:
                metrics['overall_rating'] = int(rating_match.group(1))
        
        return metrics

    def generate_summary(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics from analyses"""
        if not analyses:
            return {}
        
        total_sessions = len(analyses)
        resolved_sessions = 0
        high_satisfaction = 0
        
        for analysis in analyses:
            # Check if JSON parsing was successful
            if 'analysis_error' not in analysis and 'issue_resolved' in analysis:
                # Use parsed JSON data
                if analysis.get('issue_resolved', False):
                    resolved_sessions += 1
                if analysis.get('customer_satisfaction') == 'high':
                    high_satisfaction += 1
            else:
                # Extract from raw analysis text
                metrics = self.extract_metrics_from_raw_analysis(analysis)
                if metrics['issue_resolved']:
                    resolved_sessions += 1
                if metrics['customer_satisfaction'] == 'high':
                    high_satisfaction += 1
        
        return {
            'total_sessions': total_sessions,
            'resolved_sessions': resolved_sessions,
            'resolution_rate': f"{(resolved_sessions/total_sessions)*100:.1f}%" if total_sessions > 0 else "0%",
            'high_satisfaction_sessions': high_satisfaction,
            'satisfaction_rate': f"{(high_satisfaction/total_sessions)*100:.1f}%" if total_sessions > 0 else "0%"
        }

async def main():
    """Main function to run session analysis"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return
    
    # Initialize analyzer
    analyzer = SessionAnalyzer(api_key)
    
    print("🚀 Starting session analysis...")
    
    # Analyze all sessions
    analyses = await analyzer.analyze_all_sessions()
    
    if analyses:
        # Save report
        report_path = analyzer.save_analysis_report(analyses)
        
        # Print summary
        summary = analyzer.generate_summary(analyses)
        print(f"\n📊 Analysis Summary:")
        print(f"Total Sessions: {summary.get('total_sessions', 0)}")
        print(f"Resolution Rate: {summary.get('resolution_rate', '0%')}")
        print(f"Satisfaction Rate: {summary.get('satisfaction_rate', '0%')}")
        
        print(f"\n📄 Detailed report saved to: {report_path}")
    else:
        print("❌ No sessions found to analyze")

if __name__ == "__main__":
    asyncio.run(main())
