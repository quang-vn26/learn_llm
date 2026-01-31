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
    
    # Kết luận
    print("\n" + "="*50)
    print("📚 KẾT LUẬN - Tại sao Tokenization quan trọng?")
    print("="*50)
    print("""
    1. LLM không hiểu từ/chữ cái - chỉ hiểu TOKEN
    2. Token = mảnh văn bản có thể là từ, phần từ, hoặc dấu cách
    3. Giải thích được tại sao LLM:
       - Kém toán (số bị chia cắt không logic)
       - Không đếm được chữ cái (nhìn token, không phải letter)
       - Tính tiền theo token (không phải từ/ký tự)
    """)
