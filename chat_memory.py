# Tuần 3: Xây dựng Bộ nhớ (Memory) - "Tự tay làm nên cơm cháo"
# =============================================================
# LLM là "vô tri" (stateless) - mỗi lần gọi API, nó quên sạch.
# Bạn phải tự quản lý lịch sử hội thoại (history).

import asyncio
import os
import tiktoken
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

# Tiktoken encoding (để đếm token)
encoding = tiktoken.encoding_for_model("gpt-4o")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1️⃣  Thứ 2-4: Cấu trúc dữ liệu hội thoại (List[Dict])
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def count_tokens(messages: list[dict]) -> int:
    """Đếm tổng số token của toàn bộ messages."""
    total = 0
    for msg in messages:
        # Mỗi message có overhead ~4 tokens (role, formatting)
        total += 4
        total += len(encoding.encode(msg["content"]))
    total += 2  # Overhead cho response format
    return total


def print_history(history: list[dict]):
    """In lịch sử hội thoại đẹp."""
    print(f"\n📜 Lịch sử ({len(history)} messages, ~{count_tokens(history)} tokens):")
    print("-" * 50)
    for i, msg in enumerate(history):
        role = msg["role"]
        icon = {"system": "⚙️", "user": "👤", "assistant": "🤖"}.get(role, "❓")
        content = msg["content"][:80] + ("..." if len(msg["content"]) > 80 else "")
        print(f"  [{i}] {icon} {role}: {content}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2️⃣  Thứ 5-7: Quản lý Context Window - trim_history (FIFO)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def trim_history(history: list[dict], max_tokens: int) -> list[dict]:
    """
    Cắt bớt history khi vượt quá max_tokens.

    Thuật toán FIFO (First-In-First-Out):
    - Luôn giữ system message (index 0)
    - Xóa tin nhắn CŨ NHẤT trước (giữ lại tin nhắn mới nhất)
    - Dừng khi tổng token <= max_tokens

    Tại sao FIFO?
    - Tin nhắn gần đây quan trọng hơn (ngữ cảnh hiện tại)
    - Tin nhắn cũ ít ảnh hưởng đến cuộc hội thoại
    """
    if count_tokens(history) <= max_tokens:
        return history  # Chưa vượt giới hạn

    # Luôn giữ system message
    system_msg = [history[0]] if history[0]["role"] == "system" else []
    conversation = history[1:] if system_msg else history[:]

    # Xóa tin nhắn cũ nhất (từ đầu) cho đến khi đủ nhỏ
    while conversation and count_tokens(system_msg + conversation) > max_tokens:
        removed = conversation.pop(0)  # FIFO: xóa tin cũ nhất
        print(f"  🗑️ Xóa tin cũ: [{removed['role']}] {removed['content'][:40]}...")

    result = system_msg + conversation
    print(f"  ✂️ Đã trim: {len(history)} → {len(result)} messages")
    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3️⃣  Chat function: gửi message + quản lý memory
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def chat(history: list[dict], user_message: str, max_tokens: int = 2000) -> str:
    """
    Gửi message lên API với memory management.
    
    Bước 1: Thêm user message vào history
    Bước 2: Trim history nếu quá dài (FIFO)
    Bước 3: Gửi toàn bộ history lên API
    Bước 4: Thêm AI reply vào history
    """
    # Bước 1: Thêm user message
    history.append({"role": "user", "content": user_message})
    
    # Bước 2: Trim nếu cần
    trimmed = trim_history(history, max_tokens)
    history.clear()
    history.extend(trimmed)
    
    # Bước 3: Gửi lên API
    response = await client.chat.completions.create(
        model=deployment,
        messages=history
    )
    
    ai_reply = response.choices[0].message.content
    
    # Bước 4: Lưu AI reply
    history.append({"role": "assistant", "content": ai_reply})
    
    return ai_reply


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4️⃣  Demo: Chatbot có bộ nhớ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def demo_memory():
    """Demo chatbot có bộ nhớ hội thoại."""
    print("🧠 DEMO: CHATBOT CÓ BỘ NHỚ")
    print("=" * 50)
    
    # Khởi tạo history với system prompt
    history = [
        {"role": "system", "content": "Bạn là trợ lý AI thân thiện. Trả lời ngắn gọn bằng tiếng Việt."}
    ]
    
    # Cuộc hội thoại demo (chứng minh LLM "nhớ" được)
    conversations = [
        "Tôi tên là Quang, tôi là lập trình viên Java.",
        "Tôi đang học AI. Bạn có lời khuyên gì cho tôi?",
        "Nhắc lại tên tôi và ngôn ngữ lập trình tôi dùng?",  # Test memory!
    ]
    
    for user_msg in conversations:
        print(f"\n👤 User: {user_msg}")
        reply = await chat(history, user_msg, max_tokens=2000)
        print(f"🤖 AI: {reply}")
    
    print_history(history)


async def demo_trim_history():
    """Demo trim_history FIFO khi history quá dài."""
    print("\n\n✂️ DEMO: TRIM HISTORY (FIFO)")
    print("=" * 50)
    
    # Tạo history dài giả lập
    history = [
        {"role": "system", "content": "Bạn là trợ lý AI."},
        {"role": "user", "content": "Câu hỏi cũ số 1: Thời tiết hôm nay thế nào?"},
        {"role": "assistant", "content": "Tôi không biết thời tiết hiện tại vì tôi không có truy cập internet."},
        {"role": "user", "content": "Câu hỏi cũ số 2: Dịch 'Hello World' sang tiếng Việt"},
        {"role": "assistant", "content": "Hello World = Xin chào Thế giới"},
        {"role": "user", "content": "Câu hỏi cũ số 3: Python hay Java tốt hơn?"},
        {"role": "assistant", "content": "Tùy mục đích. Python cho AI/Data, Java cho Enterprise."},
        {"role": "user", "content": "Câu hỏi mới: Tên tôi là gì?"},
    ]
    
    print("📊 TRƯỚC khi trim:")
    print_history(history)
    total_before = count_tokens(history)
    
    # Trim với giới hạn thấp để thấy hiệu quả
    max_tokens = total_before // 2  # Giới hạn = 50% tổng token
    print(f"\n⚙️ Giới hạn: {max_tokens} tokens (50% của {total_before})")
    trimmed = trim_history(history, max_tokens)
    
    print("\n📊 SAU khi trim:")
    print_history(trimmed)
    
    print(f"\n💡 Kết quả: {len(history)} → {len(trimmed)} messages")
    print(f"   System message: {'✅ Giữ nguyên' if trimmed[0]['role'] == 'system' else '❌ Bị mất!'}")
    print(f"   Tin nhắn mới nhất: {'✅ Còn' if 'Tên tôi' in trimmed[-1]['content'] else '❌ Bị mất!'}")


async def main():
    await demo_memory()
    await demo_trim_history()
    
    print("\n" + "=" * 50)
    print("📚 TÓM TẮT TUẦN 3")
    print("=" * 50)
    print("""
    1. LLM là stateless - không có bộ nhớ tự nhiên
    2. Bạn phải tự quản lý history bằng List[Dict]
    3. 3 roles: system (nhân cách), user (người dùng), assistant (AI)
    4. trim_history FIFO: xóa tin cũ nhất, giữ system + tin mới
    5. Luôn đếm token (không phải từ!) để kiểm soát chi phí
    """)


if __name__ == "__main__":
    asyncio.run(main())
