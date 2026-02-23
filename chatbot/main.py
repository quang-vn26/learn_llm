# Tuần 4: Milestone Project - Console Chatbot Hoàn chỉnh
# ======================================================
# Kết hợp tất cả kiến thức Tuần 1-3:
# - Async API calls với retry (Tuần 1)
# - Token counting & management (Tuần 2)
# - Conversation memory với FIFO trim (Tuần 3)
#
# Chạy: python -m chatbot.main

import asyncio
import sys
import os

# Thêm root directory vào path để import được package chatbot
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.llm_client import send_message
from chatbot.memory import ChatMemory


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Cấu hình
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM_PROMPT = (
    "Bạn là trợ lý AI thân thiện và thông minh. "
    "Trả lời bằng tiếng Việt, ngắn gọn nhưng đầy đủ. "
    "Nếu không biết, hãy nói thẳng là không biết."
)
MAX_CONTEXT_TOKENS = 3000  # Giới hạn context window


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Các lệnh đặc biệt
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMANDS = {
    "/clear":  "Xóa bộ nhớ hội thoại",
    "/stats":  "Hiển thị thống kê token",
    "/history": "Xem lịch sử hội thoại",
    "/help":   "Hiển thị danh sách lệnh",
    "/quit":   "Thoát chương trình",
}


def print_banner():
    """Hiển thị banner khi khởi động."""
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║    🤖 AI CHATBOT - Tuần 4 Milestone Project     ║")
    print("║    Kết hợp: Async + Token + Memory + Retry      ║")
    print("╠══════════════════════════════════════════════════╣")
    print("║  Gõ câu hỏi để chat, hoặc dùng lệnh:           ║")
    print("║  /clear  - Xóa bộ nhớ   /stats - Thống kê      ║")
    print("║  /history - Lịch sử     /help  - Trợ giúp       ║")
    print("║  /quit   - Thoát                                 ║")
    print("╚══════════════════════════════════════════════════╝")
    print()


def print_help():
    """Hiển thị danh sách lệnh."""
    print("\n📋 Danh sách lệnh:")
    print("-" * 40)
    for cmd, desc in COMMANDS.items():
        print(f"  {cmd:10s} → {desc}")
    print()


def print_history(memory: ChatMemory):
    """Hiển thị lịch sử hội thoại."""
    messages = memory.get_messages()
    print(f"\n📜 Lịch sử ({memory.message_count} tin nhắn, ~{memory.current_tokens} tokens):")
    print("-" * 50)
    for i, msg in enumerate(messages):
        role = msg["role"]
        icon = {"system": "⚙️", "user": "👤", "assistant": "🤖"}.get(role, "❓")
        content = msg["content"]
        # Cắt nội dung dài cho dễ đọc
        if len(content) > 100:
            content = content[:100] + "..."
        print(f"  [{i}] {icon} {role}: {content}")
    print()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main chat loop
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def chat_loop():
    """Vòng lặp chính của chatbot."""
    memory = ChatMemory(system_prompt=SYSTEM_PROMPT, max_tokens=MAX_CONTEXT_TOKENS)
    print_banner()

    while True:
        try:
            # Nhận input từ người dùng
            user_input = input("👤 Bạn: ").strip()

            if not user_input:
                continue

            # Xử lý lệnh đặc biệt
            if user_input.lower() == "/quit":
                print("\n👋 Tạm biệt! Tổng token đã dùng:", memory.total_tokens_used)
                break

            if user_input.lower() == "/clear":
                memory.clear()
                print("🗑️ Đã xóa bộ nhớ hội thoại!")
                print(memory.get_stats())
                continue

            if user_input.lower() == "/stats":
                print(memory.get_stats())
                continue

            if user_input.lower() == "/history":
                print_history(memory)
                continue

            if user_input.lower() == "/help":
                print_help()
                continue

            if user_input.startswith("/"):
                print(f"❓ Lệnh không hợp lệ: {user_input}. Gõ /help để xem danh sách.")
                continue

            # --- Gửi message lên API ---

            # Bước 1: Thêm user message vào memory
            memory.add_user_message(user_input)

            # Bước 2: Trim nếu cần (FIFO)
            removed = memory.trim()
            if removed > 0:
                print(f"  ✂️ Đã xóa {removed} tin cũ để giữ trong giới hạn token.")

            # Bước 3: Gửi lên API (có retry)
            print("🤖 AI: ", end="", flush=True)

            try:
                result = await send_message(memory.get_messages())
            except RuntimeError as e:
                print(f"\n❌ {e}")
                # Xóa message vừa thêm vì API thất bại
                memory.history.pop()
                continue

            ai_reply = result["content"]
            print(ai_reply)

            # Bước 4: Lưu AI reply + cập nhật stats
            memory.add_assistant_message(ai_reply)
            memory.add_token_usage(result["usage"]["total_tokens"])

            # Hiển thị token info (để debug)
            usage = result["usage"]
            print(
                f"  💡 [{usage['prompt_tokens']} in → "
                f"{usage['completion_tokens']} out = "
                f"{usage['total_tokens']} tokens] "
                f"| {memory.get_stats()}"
            )

        except KeyboardInterrupt:
            print("\n\n👋 Tạm biệt! (Ctrl+C)")
            print(f"Tổng token đã dùng: {memory.total_tokens_used}")
            break

        except EOFError:
            print("\n👋 Tạm biệt!")
            break


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Entry point
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    asyncio.run(chat_loop())
