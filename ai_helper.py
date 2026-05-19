import os
import json
from dotenv import load_dotenv

# Try to import openai, but handle it if not installed
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv()

class AIHelper:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        if OpenAI and self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    def suggest_category(self, description, categories):
        """Suggests a category based on the description using AI or robust keyword matching."""
        desc_lower = description.lower()

        # Improved Keyword-based matching (Fallback & Initial Check)
        keyword_map = {
            "Food": ["pizza", "food", "eat", "restaurant", "lunch", "dinner", "grocery", "groceries", "cafe", "coffee", "starbucks", "burger", "chips", "snacks", "drinks", "meat", "vegetables", "fruit", "milk", "bread"],
            "Travel": ["uber", "taxi", "bus", "train", "flight", "gas", "fuel", "petrol", "parking", "toll", "airline", "hotel", "stay", "vacation", "holiday", "germany", "travel", "trip", "car", "automotive"],
            "Bills": ["rent", "electric", "water", "internet", "bill", "electricity", "gas bill", "phone", "mobile", "recharge", "subscription", "insurance", "loan", "mortgage", "tax"],
            "Entertainment": ["movie", "game", "netflix", "concert", "cinema", "spotify", "hulu", "disney", "theatre", "zoo", "park", "club", "party"],
            "Shopping": ["amazon", "ebay", "clothes", "shoes", "fashion", "electronics", "gadget", "mall", "walmart", "target", "shopping"],
            "Health": ["doctor", "medicine", "pharmacy", "hospital", "gym", "fitness", "workout", "dental", "clinic", "health", "vitamin"]
        }

        # Check keyword map first (fast and reliable for common cases)
        for category, keywords in keyword_map.items():
            if any(word in desc_lower for word in keywords):
                if category in categories:
                    return category

        if not self.client:
            return categories[-1] # Default to 'Other'

        try:
            # AI logic if keyword match fails and client exists
            prompt = f"Categorize this expense description: '{description}'. \nAvailable categories: {', '.join(categories)}. \nReturn ONLY the single category name from the list provided."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a helpful financial assistant that categorizes expenses into a fixed list of categories."},
                          {"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0
            )
            suggested = response.choices[0].message.content.strip()
            # Handle potential punctuation or case issues from AI
            suggested = suggested.replace(".", "").replace("'", "").replace("\"", "")
            
            for cat in categories:
                if cat.lower() == suggested.lower():
                    return cat
            
            return categories[-1]
        except Exception:
            return categories[-1]

    def get_financial_advice(self, summary_data):
        """Provides financial advice based on the summary data."""
        if not self.client:
            return "Tip: Try to keep your expenses lower than your income! Consider saving at least 20% of your income."

        try:
            prompt = f"Given this financial summary: {json.dumps(summary_data)}. Provide a short, professional 2-sentence financial advice."
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting AI advice: {str(e)}"
