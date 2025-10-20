import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

class LLMService:
    """Service for managing different LLM providers and models"""
    
    def __init__(self):
        self.available_models = {
            "OpenRouter - Claude 3.5 Sonnet": {
                "provider": "openrouter",
                "model": "anthropic/claude-3-5-sonnet",
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": "https://openrouter.ai/api/v1"
            },
            "OpenRouter - GPT-4o": {
                "provider": "openrouter", 
                "model": "openai/gpt-4o",
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": "https://openrouter.ai/api/v1"
            },
            "OpenRouter - Mistral 7B": {
                "provider": "openrouter",
                "model": "mistralai/mistral-7b-instruct", 
                "api_key": os.getenv("OPENROUTER_API_KEY"),
                "base_url": "https://openrouter.ai/api/v1"
            },
            "OpenAI - GPT-4o Mini": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "api_key": os.getenv("OPENAI_API_KEY")
            }
        }
    
    def get_model(self, model_name: str) -> ChatOpenAI:
        """Get a configured model instance"""
        if model_name not in self.available_models:
            raise ValueError(f"Model {model_name} not found")
        
        config = self.available_models[model_name]
        
        if config["provider"] == "openrouter":
            return ChatOpenAI(
                model=config["model"],
                api_key=config["api_key"],
                base_url=config["base_url"],
                temperature=0.7,
                max_tokens=4000
            )
        elif config["provider"] == "openai":
            return ChatOpenAI(
                model=config["model"],
                api_key=config["api_key"],
                temperature=0.7,
                max_tokens=4000
            )
        else:
            raise ValueError(f"Unsupported provider: {config['provider']}")
    
    def get_available_models(self) -> list:
        """Get list of available model names"""
        return list(self.available_models.keys())
