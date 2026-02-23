# Buổi tối Ngày 1: Giải mã "Hộp đen" Tokenization
# =============================================
# LLM không hiểu "Từ" - chúng xử lý các chuỗi số (tokens)
# Token có thể là: một từ, một phần của từ, hoặc dấu cách

import tiktoken

def token_kung_fu(text):
    """
    Phân tích cách LLM "nhìn" văn bản thông qua tokenization.
    Sử dụng encoding của model gpt-4o (tương thích Azure OpenAI)
    """
    # Sử dụng encoding của model gpt-4o
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    # Mã hóa văn bản thành list các token IDs
    tokens = encoding.encode(text)
    
    print(f"\n{'='*50}")
    print(f"📝 Văn bản: '{text}'")
    print(f"📊 Số lượng token: {len(tokens)}")
    print(f"🔢 Token IDs: {tokens}")
    print(f"\n🔍 Chi tiết từng token:")
    
    # Giải mã từng ID để thấy LLM thực sự "nhìn" gì
    for i, token_id in enumerate(tokens):
        decoded = encoding.decode([token_id])
        print(f"   [{i+1}] ID {token_id:6d} -> '{decoded}'")
    
    return tokens

def demo_why_llm_bad_at_math():
    """
    Demo: Tại sao LLM thường tính toán sai?
    Vì các con số bị chia cắt thành các token không logic
    """
    print("\n" + "="*50)
    print("🧮 DEMO: TẠI SAO LLM KÉM TOÁN?")
    print("="*50)
    
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    numbers = ["12345", "123456789", "1000000"]
    for num in numbers:
        tokens = encoding.encode(num)
        print(f"\nSố '{num}':")
        print(f"  → Bị chia thành {len(tokens)} tokens: ", end="")
        for token_id in tokens:
            print(f"'{encoding.decode([token_id])}'", end=" ")
        print()

def demo_strawberry_problem():
    """
    Demo: Tại sao LLM không đếm được chữ 'r' trong 'strawberry'?
    Vì tokenizer chia từ thành các mảnh, không phải từng chữ cái
    """
    print("\n" + "="*50)
    print("🍓 DEMO: VẤN ĐỀ 'STRAWBERRY'")
    print("="*50)
    
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    word = "strawberry"
    tokens = encoding.encode(word)
    
    print(f"\nTừ '{word}' được LLM nhìn như thế nào?")
    print(f"→ Bị chia thành {len(tokens)} tokens:")
    
    for i, token_id in enumerate(tokens):
        decoded = encoding.decode([token_id])
        r_count = decoded.count('r')
        print(f"   Token {i+1}: '{decoded}' (chứa {r_count} chữ 'r')")
    
    print(f"\n💡 Kết luận:")
    print(f"   LLM KHÔNG nhìn từng chữ cái 'r' riêng lẻ!")
    print(f"   Nó chỉ thấy các token, nên đếm sai là điều dễ hiểu.")

def demo_cost_calculation():
    """
    Demo: Tính chi phí dựa trên token (không phải từ hay ký tự)
    """
    print("\n" + "="*50)
    print("💰 DEMO: TÍNH CHI PHÍ API")
    print("="*50)
    
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    texts = [
        "Hello",
        "Xin chào",
        "Lập trình AI với Python",
        "The quick brown fox jumps over the lazy dog"
    ]
    
    # Giá ước tính cho GPT-4o (input)
    price_per_1k_tokens = 0.005  # $0.005 per 1K tokens
    
    print(f"\nGiá: ${price_per_1k_tokens} / 1000 tokens")
    print("-" * 50)
    
    for text in texts:
        tokens = encoding.encode(text)
        char_count = len(text)
        word_count = len(text.split())
        token_count = len(tokens)
        cost = (token_count / 1000) * price_per_1k_tokens
        
        print(f"\n'{text}'")
        print(f"   Ký tự: {char_count}, Từ: {word_count}, Token: {token_count}")
        print(f"   Chi phí: ${cost:.6f}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🥋 BÀI TẬP "TOKEN KUNG FU" (Code Kata - Thứ 4)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Đề bài: Viết hàm truncate_text(text, max_tokens)
# Yêu cầu: Cắt text không vượt quá max_tokens,
#           không cắt giữa từ hoặc câu (nếu có thể).
# Mục đích: Kỹ năng quan trọng khi nạp dữ liệu vào Context Window.

def truncate_text(text: str, max_tokens: int) -> str:
    """
    Cắt text sao cho không vượt quá max_tokens.
    
    Thuật toán (suy nghĩ từng bước):
    Bước 1: Encode toàn bộ text → list token IDs
    Bước 2: Nếu đã ngắn hơn max_tokens → trả về nguyên
    Bước 3: Cắt lấy max_tokens token đầu tiên
    Bước 4: Decode lại → tìm ranh giới câu/từ gần nhất
    Bước 5: Trả về text đã cắt gọn
    """
    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(text)
    
    # Bước 2: Không cần cắt
    if len(tokens) <= max_tokens:
        return text
    
    # Bước 3: Cắt theo token
    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoding.decode(truncated_tokens)
    
    # Bước 4a: Tìm ranh giới câu gần nhất (dấu chấm, ?, !)
    sentence_ends = ['.', '!', '?', '。']
    last_sentence_end = -1
    for i, char in enumerate(truncated_text):
        if char in sentence_ends:
            last_sentence_end = i
    
    # Nếu tìm được ranh giới câu (và không mất quá 50% nội dung)
    if last_sentence_end > len(truncated_text) * 0.5:
        return truncated_text[:last_sentence_end + 1]
    
    # Bước 4b: Fallback - cắt tại ranh giới từ (khoảng trắng)
    last_space = truncated_text.rfind(' ')
    if last_space > 0:
        return truncated_text[:last_space] + "..."
    
    return truncated_text + "..."


def demo_truncate_text():
    """Demo hàm truncate_text - cắt văn bản thông minh theo token."""
    print("\n" + "="*50)
    print("✂️ DEMO: TRUNCATE TEXT (Code Kata)")
    print("="*50)
    
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    # Tạo đoạn văn dài
    long_text = (
        "Trí tuệ nhân tạo đang thay đổi thế giới. "
        "Các mô hình ngôn ngữ lớn có thể hiểu và sinh ra văn bản. "
        "Python là ngôn ngữ phổ biến nhất để phát triển AI. "
        "Tokenization là bước đầu tiên để LLM xử lý văn bản. "
        "Mỗi model có giới hạn context window khác nhau."
    )
    
    original_tokens = len(encoding.encode(long_text))
    print(f"\n📝 Văn bản gốc ({original_tokens} tokens):")
    print(f"   {long_text}")
    
    # Cắt với các giới hạn khác nhau
    for max_t in [30, 20, 10]:
        result = truncate_text(long_text, max_t)
        result_tokens = len(encoding.encode(result))
        print(f"\n✂️ max_tokens={max_t} → ({result_tokens} tokens):")
        print(f"   {result}")
    
    print(f"\n💡 Tại sao kỹ năng này quan trọng?")
    print(f"   - Context Window có giới hạn (128K tokens cho GPT-4o)")
    print(f"   - RAG cần nhét nhiều tài liệu → phải cắt gọn")
    print(f"   - Cắt sai → mất ý nghĩa → LLM trả lời sai!")


# ===== CHẠY TẤT CẢ DEMO =====
if __name__ == "__main__":
    print("🥋 TOKEN KUNG FU - Giải mã Tokenization")
    print("="*50)
    
    # Bài tập cơ bản
    token_kung_fu("Apple")
    token_kung_fu("apple")
    token_kung_fu("Lập trình AI")
    token_kung_fu("Hello, how are you?")
    
    # Demo các vấn đề thực tế
    demo_why_llm_bad_at_math()
    demo_strawberry_problem()
    demo_cost_calculation()
    
    # Bài tập Token Kung Fu (Code Kata)
    demo_truncate_text()
    
    # Kết luận
    print("\n" + "="*50)
    print("📚 KẾT LUẬN - Tại sao Tokenization quan trọng?")
    print("="*50)
    print("""
    1. LLM không hiểu từ/chữ cái - chỉ hiểu TOKEN
    2. Token = mảnh văn bản có thể là từ, phần từ, hoặc dấu cách
    3. truncate_text: cắt thông minh theo token, không cắt giữa từ
    4. Giải thích được tại sao LLM:
       - Kém toán (số bị chia cắt không logic)
       - Không đếm được chữ cái (nhìn token, không phải letter)
       - Tính tiền theo token (không phải từ/ký tự)
    """)
