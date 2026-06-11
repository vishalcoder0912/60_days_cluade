from app.core.config import settings


def get_ai_service():
    """Return the appropriate AI service based on config."""
    if settings.USE_OPENROUTER:
        from app.services.openrouter_service import OpenRouterService
        return OpenRouterService()
    else:
        from app.services.ollama_service import OllamaService
        return OllamaService()
