import anthropic
import os


class ChatAnthropic:
    def __init__(self, model_name: str = "claude-sonnet-4-5-20250929"):
        self.model_name = model_name
        self.base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
        if self.auth_token is None:
            raise ValueError("ANTHROPIC_AUTH_TOKEN is not set")

    def run(self, messages, text_only: bool = True, **kwargs):
        if not isinstance(messages, list):
            raise ValueError("messages must be a list")

        client = anthropic.Anthropic(
            base_url=self.base_url,
            api_key=self.auth_token,
        )

        # Extract system message if present
        system_content = None
        chat_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_content = msg["content"]
            else:
                chat_messages.append(msg)

        # Build request kwargs
        request_kwargs = {
            "model": self.model_name,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": chat_messages,
        }
        if system_content:
            request_kwargs["system"] = system_content

        response = client.messages.create(**request_kwargs)

        if text_only:
            return response.content[0].text

        return response
