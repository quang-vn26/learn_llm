# Tuần 4 - Module: LLM Client
# ====================================
# Gọi API Azure OpenAI với retry (exponential backoff)
# Tái sử dụng logic từ Tuần 1

import asyncio
import os
import random
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

load_dotenv()

# Azure OpenAI configuration
client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


async def send_message(messages: list[dict], max_retries: int = 3) -> dict:
    """
    Gửi messages lên Azure OpenAI API với exponential backoff retry.
    
    Returns dict chứa:
    - content: nội dung trả lời
    - usage: thông tin token sử dụng
    - model: model đã dùng
    - finish_reason: lý do dừng
    """
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=deployment,
                messages=messages
            )

            choice = response.choices[0]
            usage = response.usage

            return {
                "content": choice.message.content,
                "finish_reason": choice.finish_reason,
                "model": response.model,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                },
            }

        except Exception as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"API thất bại sau {max_retries} lần thử: {e}")

            wait_time = (2 ** attempt) + random.uniform(0, 1)
            wait_time = min(wait_time, 30)
            print(f"  ⚠️ Lỗi API: {type(e).__name__}. Thử lại sau {wait_time:.1f}s...")
            await asyncio.sleep(wait_time)
