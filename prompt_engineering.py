"""
🧠 Prompt Engineering as Code
==============================
Prompt không phải là văn xuôi, nó là LOGIC.

Script này demo 3 kỹ thuật Prompt Engineering:
1. Zero-shot:  Hỏi trực tiếp, không có ví dụ mẫu
2. Few-shot:   Cung cấp 3 ví dụ mẫu (Input → Output) trước khi hỏi
3. Chain-of-Thought (CoT): Thêm "Let's think step by step" để tăng logic
"""

import os
import sys
import time
from dotenv import load_dotenv
from openai import AzureOpenAI

# ─── Cấu hình ──────────────────────────────────────────────
load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

LOG_FILE = os.path.join(os.path.dirname(__file__), "prompt_engineering_log.txt")


class TeeWriter:
    """Ghi output ra cả console LẪN file cùng lúc."""
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.file = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

    def close(self):
        self.file.close()
        sys.stdout = self.terminal


# ─── Helper: gọi LLM và in kết quả ────────────────────────
def ask(technique_name: str, messages: list[dict]) -> str:
    """Gửi prompt đến LLM, đo thời gian, in kết quả."""
    print(f"\n{'='*60}")
    print(f"🔬 Kỹ thuật: {technique_name}")
    print(f"{'='*60}")

    # Hiển thị prompt đã gửi
    for msg in messages:
        role_icon = "🤖" if msg["role"] == "system" else "👤"
        print(f"  {role_icon} [{msg['role']}]: {msg['content'][:120]}...")
    print()

    start = time.time()
    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
    )
    duration = time.time() - start

    answer = response.choices[0].message.content
    tokens = response.usage

    print(f"📝 Trả lời:\n{answer}")
    print(f"\n⏱️  Thời gian: {duration:.2f}s")
    print(f"📊 Tokens — Input: {tokens.prompt_tokens} | Output: {tokens.completion_tokens} | Total: {tokens.total_tokens}")

    return answer


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1️⃣  ZERO-SHOT: Hỏi trực tiếp, không ví dụ mẫu
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def demo_zero_shot():
    """
    Zero-shot = Hỏi LLM trực tiếp mà KHÔNG cung cấp bất kỳ ví dụ nào.
    LLM phải tự hiểu task dựa vào kiến thức đã học.

    Ưu điểm: Đơn giản, ít token
    Nhược điểm: Có thể trả lời sai format hoặc thiếu chính xác
    """
    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý phân loại cảm xúc (sentiment analysis)."
        },
        {
            "role": "user",
            "content": 'Phân loại cảm xúc của câu sau thành Positive, Negative, hoặc Neutral:\n\n"Bộ phim này hay đến nỗi tôi xem đi xem lại 3 lần!"'
        }
    ]
    return ask("ZERO-SHOT (Hỏi trực tiếp)", messages)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2️⃣  FEW-SHOT: Cung cấp 3 ví dụ mẫu (Input → Output)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def demo_few_shot():
    """
    Few-shot = Cung cấp VÍ DỤ MẪU trong prompt để LLM "học" pattern.
    Thường dùng 3 ví dụ (Input → Output) trước câu hỏi thật.

    Ưu điểm: LLM hiểu chính xác format mong muốn
    Nhược điểm: Tốn nhiều token hơn (mỗi ví dụ = thêm token)
    """
    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý phân loại cảm xúc. Trả lời ĐÚNG format: chỉ 1 từ (Positive/Negative/Neutral)."
        },
        # ─── Ví dụ 1 ───
        {
            "role": "user",
            "content": 'Phân loại cảm xúc:\n"Món ăn ngon tuyệt vời, tôi rất hài lòng!"'
        },
        {
            "role": "assistant",
            "content": "Positive"
        },
        # ─── Ví dụ 2 ───
        {
            "role": "user",
            "content": 'Phân loại cảm xúc:\n"Dịch vụ tệ quá, đợi 2 tiếng mà không ai phục vụ."'
        },
        {
            "role": "assistant",
            "content": "Negative"
        },
        # ─── Ví dụ 3 ───
        {
            "role": "user",
            "content": 'Phân loại cảm xúc:\n"Cửa hàng mở cửa từ 8h đến 22h."'
        },
        {
            "role": "assistant",
            "content": "Neutral"
        },
        # ─── Câu hỏi THẬT ───
        {
            "role": "user",
            "content": 'Phân loại cảm xúc:\n"Bộ phim này hay đến nỗi tôi xem đi xem lại 3 lần!"'
        }
    ]
    return ask("FEW-SHOT (3 ví dụ mẫu)", messages)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3️⃣  CHAIN-OF-THOUGHT (CoT): Suy nghĩ từng bước
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def demo_chain_of_thought():
    """
    CoT = Thêm câu "Let's think step by step" để buộc LLM
    trình bày LOGIC TỪNG BƯỚC trước khi đưa ra kết luận.

    Đặc biệt hiệu quả với:
    - Bài toán logic / suy luận
    - Bài toán toán học
    - So sánh phức tạp

    Ưu điểm: Tăng khả năng suy luận đáng kể
    Nhược điểm: Output dài hơn, tốn token hơn
    """
    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý giải toán thông minh."
        },
        {
            "role": "user",
            "content": (
                "Một cửa hàng bán áo với giá 200,000 VNĐ/chiếc. "
                "Nếu mua từ 3 chiếc trở lên được giảm 15%. "
                "Thuế VAT là 10% (tính sau giảm giá). "
                "Hỏi: Mua 5 chiếc thì phải trả bao nhiêu?\n\n"
                "Let's think step by step."  # ← Câu thần chú CoT!
            )
        }
    ]
    return ask("CHAIN-OF-THOUGHT (Suy luận từng bước)", messages)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔥 SO SÁNH: Cùng 1 bài toán, KHÔNG có CoT vs CÓ CoT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def demo_cot_comparison():
    """So sánh kết quả KHÔNG CoT vs CÓ CoT trên cùng 1 bài toán logic."""

    math_problem = (
        "Một cửa hàng bán áo với giá 200,000 VNĐ/chiếc. "
        "Nếu mua từ 3 chiếc trở lên được giảm 15%. "
        "Thuế VAT là 10% (tính sau giảm giá). "
        "Hỏi: Mua 5 chiếc thì phải trả bao nhiêu?"
    )

    # ❌ Không có CoT
    print("\n" + "🔴" * 30)
    print("SO SÁNH: KHÔNG CÓ CoT vs CÓ CoT")
    print("🔴" * 30)

    no_cot = [
        {"role": "system", "content": "Bạn là trợ lý giải toán. Trả lời ngắn gọn."},
        {"role": "user", "content": math_problem}
    ]
    ask("❌ KHÔNG CÓ CoT", no_cot)

    # ✅ Có CoT
    with_cot = [
        {"role": "system", "content": "Bạn là trợ lý giải toán. Trình bày rõ từng bước."},
        {"role": "user", "content": math_problem + "\n\nLet's think step by step."}
    ]
    ask("✅ CÓ CoT (Let's think step by step)", with_cot)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🏁 MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == "__main__":
    # Ghi log ra file (ghi đè mỗi lần chạy)
    tee = TeeWriter(LOG_FILE)
    sys.stdout = tee

    print("🧠 PROMPT ENGINEERING AS CODE")
    print("=" * 60)
    print("Prompt không phải là văn xuôi, nó là LOGIC!")
    print("Hôm nay ta sẽ so sánh 3 kỹ thuật prompting.\n")

    # 1. Zero-shot
    demo_zero_shot()

    # 2. Few-shot
    demo_few_shot()

    # 3. Chain-of-Thought
    demo_chain_of_thought()

    # 4. So sánh trực quan CoT vs không CoT
    demo_cot_comparison()

    # Tổng kết
    print("\n" + "=" * 60)
    print("📋 TỔNG KẾT")
    print("=" * 60)
    print("""
┌──────────────────┬───────────────────────────────────────────────┐
│ Kỹ thuật         │ Khi nào dùng?                                │
├──────────────────┼───────────────────────────────────────────────┤
│ Zero-shot        │ Task đơn giản, LLM đã hiểu sẵn              │
│ Few-shot         │ Cần output đúng format, task đặc thù         │
│ Chain-of-Thought │ Bài toán logic, suy luận, toán học           │
└──────────────────┴───────────────────────────────────────────────┘

💡 Tips:
  • Zero-shot tốn ít token nhất → rẻ nhất
  • Few-shot giúp LLM hiểu format → ít "ảo" nhất
  • CoT tốn nhiều token nhất nhưng chính xác nhất cho logic
  • Có thể KẾT HỢP: Few-shot + CoT = combo mạnh nhất!
""")

    # Đóng log file
    tee.close()
    print(f"📄 Log đã được lưu tại: {LOG_FILE}")
