# Tuần 1 - Thứ 6-7: Xử lý lỗi & Retry
# ==========================================
# API AI thường xuyên bị lỗi 429 (Too Many Requests) hoặc 500.
# Cần cơ chế exponential backoff để retry thông minh.

import asyncio
import os
import random
import time
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1️⃣  Cách 1: Tự viết Exponential Backoff (First Principles)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def call_llm_manual_retry(prompt: str, max_retries: int = 5) -> str:
    """
    Gọi LLM với cơ chế retry tự viết.
    
    Exponential Backoff: thời gian chờ tăng gấp đôi sau mỗi lần thất bại.
    Jitter: thêm random nhỏ để tránh nhiều client retry cùng lúc.
    
    Lần 1 thất bại → Chờ ~1s  → Thử lại
    Lần 2 thất bại → Chờ ~2s  → Thử lại
    Lần 3 thất bại → Chờ ~4s  → Thử lại
    ...
    """
    for attempt in range(max_retries):
        try:
            print(f"  🔄 Lần thử {attempt + 1}/{max_retries}...")
            response = await client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "Trả lời ngắn gọn."},
                    {"role": "user", "content": prompt}
                ]
            )
            print(f"  ✅ Thành công ở lần thử {attempt + 1}!")
            return response.choices[0].message.content
            
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"  ❌ Hết {max_retries} lần thử. Lỗi cuối: {e}")
                raise  # Hết lần thử → raise lỗi

            # Exponential backoff + jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            wait_time = min(wait_time, 30)  # Cap tối đa 30s
            print(f"  ⚠️ Lỗi: {type(e).__name__}: {e}")
            print(f"  ⏳ Chờ {wait_time:.1f}s rồi thử lại...")
            await asyncio.sleep(wait_time)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2️⃣  Cách 2: Dùng thư viện tenacity (Production-ready)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

try:
    from tenacity import retry, wait_exponential, stop_after_attempt, before_sleep_log
    import logging
    
    logger = logging.getLogger(__name__)

    @retry(
        wait=wait_exponential(multiplier=1, min=1, max=30),  # 1s, 2s, 4s, 8s... max 30s
        stop=stop_after_attempt(5),  # Tối đa 5 lần thử
    )
    async def call_llm_tenacity_retry(prompt: str) -> str:
        """
        Gọi LLM với retry bằng tenacity.
        Decorator @retry tự động xử lý backoff.
        """
        response = await client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "Trả lời ngắn gọn."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    HAS_TENACITY = True
except ImportError:
    HAS_TENACITY = False
    print("⚠️ Thư viện tenacity chưa cài. Dùng: pip install tenacity")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3️⃣  Demo: So sánh 2 cách
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def main():
    print("🔁 RETRY WRAPPER - Xử lý lỗi API thông minh")
    print("=" * 50)
    
    prompt = "Exponential backoff là gì? Trả lời trong 1 câu."
    
    # --- Cách 1: Manual retry ---
    print("\n📌 Cách 1: Tự viết Exponential Backoff")
    print("-" * 40)
    start = time.time()
    try:
        result = await call_llm_manual_retry(prompt)
        print(f"  📝 Kết quả: {result}")
        print(f"  ⏱️ Thời gian: {time.time() - start:.2f}s")
    except Exception as e:
        print(f"  ❌ Thất bại hoàn toàn: {e}")
    
    # --- Cách 2: Tenacity ---
    if HAS_TENACITY:
        print("\n📌 Cách 2: Dùng tenacity")
        print("-" * 40)
        start = time.time()
        try:
            result = await call_llm_tenacity_retry(prompt)
            print(f"  📝 Kết quả: {result}")
            print(f"  ⏱️ Thời gian: {time.time() - start:.2f}s")
        except Exception as e:
            print(f"  ❌ Thất bại hoàn toàn: {e}")

    # --- Tóm tắt ---
    print("\n" + "=" * 50)
    print("📚 TÓM TẮT")
    print("=" * 50)
    print("""
    Exponential Backoff:
    - Thời gian chờ tăng gấp đôi: 1s → 2s → 4s → 8s → 16s
    - Jitter (random): tránh nhiều client retry cùng lúc
    - Cap (giới hạn): không chờ quá 30s
    
    Khi nào cần retry?
    - 429 Too Many Requests (rate limit)
    - 500 Internal Server Error
    - 503 Service Unavailable
    - Timeout / Connection Error
    """)


if __name__ == "__main__":
    asyncio.run(main())
