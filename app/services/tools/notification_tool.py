import os
import requests
from langchain.agents import Tool

def send_push_notification(message: str) -> str:
    """Send a push notification to the user"""
    try:
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_user = os.getenv("PUSHOVER_USER")
        
        if not pushover_token or not pushover_user:
            return "❌ Pushover credentials not configured. Please set PUSHOVER_TOKEN and PUSHOVER_USER environment variables."
        
        pushover_url = "https://api.pushover.net/1/messages.json"
        
        response = requests.post(
            pushover_url,
            data={
                "token": pushover_token,
                "user": pushover_user,
                "message": message
            }
        )
        
        if response.status_code == 200:
            return f"✅ Push notification sent: {message}"
        else:
            return f"❌ Failed to send push notification: {response.text}"
            
    except Exception as e:
        return f"❌ Error sending push notification: {str(e)}"

notification_tool = Tool(
    name="send_push_notification",
    func=send_push_notification,
    description="Send a push notification to the user's device via Pushover service."
)
