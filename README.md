# 🎓 Learn AI - Ôn tập kiến thức

## 🤖 LLM & Transformer Cơ bản

### ❓ Câu 1: LLM viết tắt của từ gì?

<details>
<summary>👉 Xem đáp án</summary>

**LLM = Large Language Model** (Mô hình Ngôn ngữ Lớn)

| Thành phần | Ý nghĩa |
|------------|---------|
| **Large** | Lớn - hàng tỷ tham số (parameters), được train trên lượng dữ liệu khổng lồ |
| **Language** | Ngôn ngữ - hiểu và sinh ra văn bản của con người |
| **Model** | Mô hình - thuật toán AI được huấn luyện |

**Ví dụ các LLM phổ biến:**
- GPT-4, GPT-4o (OpenAI)
- Claude 3.5 Sonnet (Anthropic)
- Gemini 1.5, Gemini 2.0 (Google)
- Llama 3 (Meta)

**LLM làm được gì?**
- Trả lời câu hỏi, viết văn bản
- Dịch thuật, tóm tắt
- Viết code, sửa lỗi
- Phân tích dữ liệu

</details>

---

### ❓ Câu 2: Cơ chế chính của Transformer là gì?

<details>
<summary>👉 Xem đáp án</summary>

**Self-Attention** (Cơ chế Tự Chú Ý) là trái tim của kiến trúc Transformer!

**Self-Attention là gì?**

Nó cho phép mỗi từ trong câu "nhìn" và "chú ý" đến tất cả các từ khác để hiểu ngữ cảnh.

**Ví dụ minh họa:**

```
Câu: "Con mèo đuổi con chuột vì nó đói"
                                  ↓
                          "nó" chỉ ai?
```

Self-Attention giúp model hiểu được "nó" chỉ **"con mèo"** (vì mèo mới đói và đuổi chuột).

**Cách hoạt động đơn giản:**

```
Bước 1: Mỗi từ tạo ra 3 vector: Query (Q), Key (K), Value (V)
Bước 2: Tính độ "liên quan" giữa các từ: Q × K
Bước 3: Dùng độ liên quan làm trọng số để kết hợp các Value
```

| Từ | Chú ý nhiều đến | Lý do |
|----|-----------------|-------|
| "nó" | "mèo" (80%), "chuột" (15%) | Ngữ cảnh "đuổi" và "đói" |
| "đuổi" | "mèo" (70%), "chuột" (25%) | Mèo là chủ thể hành động |

**Tại sao Self-Attention mạnh?**
- Hiểu được ngữ cảnh xa (không giới hạn khoảng cách từ)
- Xử lý song song (nhanh hơn RNN/LSTM)
- Linh hoạt với nhiều loại quan hệ

</details>

---

### ❓ Câu 3: Tokenization là gì?

<details>
<summary>👉 Xem đáp án</summary>

**Tokenization** là quá trình **chia văn bản thành các mảnh nhỏ (tokens)** để LLM có thể xử lý.

**Tại sao cần Tokenization?**

LLM không thể đọc text trực tiếp! Nó cần chuyển text → số (token IDs).

```
"Hello World" → [15496, 2159] → LLM xử lý → [Output IDs] → "Xin chào"
```

**Ví dụ Tokenization thực tế:**

| Văn bản | Tokens | Số lượng |
|---------|--------|----------|
| `"Hello"` | `["Hello"]` | 1 token |
| `"Hello World"` | `["Hello", " World"]` | 2 tokens |
| `"Xin chào"` | `["X", "in", " ch", "ào"]` | 4 tokens |
| `"GPT-4"` | `["G", "PT", "-", "4"]` | 4 tokens |
| `"strawberry"` | `["st", "raw", "berry"]` | 3 tokens |

**Quy luật tokenization:**
```python
# Từ phổ biến → ít tokens
"the"        → ["the"]           # 1 token
"computer"   → ["computer"]       # 1 token

# Từ hiếm hoặc tiếng Việt → nhiều tokens hơn
"Việt Nam"   → ["Vi", "ệt", " Nam"]  # 3 tokens
"Lập trình"  → ["L", "ập", " tr", "ình"]  # 4 tokens
```

**Code demo:**
```python
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")

text = "Xin chào Việt Nam!"
tokens = encoder.encode(text)

print(f"Text: {text}")
print(f"Token IDs: {tokens}")
print(f"Số tokens: {len(tokens)}")

# Xem từng token là gì
for token_id in tokens:
    print(f"  {token_id} → '{encoder.decode([token_id])}'")
```

**Output:**
```
Text: Xin chào Việt Nam!
Token IDs: [55, 258, 559, 3975, 79136, 23561, 0]
Số tokens: 7
  55 → 'X'
  258 → 'in'
  559 → ' ch'
  3975 → 'ào'
  79136 → ' Vi'
  23561 → 'ệt'
  ...
```

**💡 Ghi nhớ:** Tiếng Việt tốn nhiều tokens hơn tiếng Anh → chi phí API cao hơn!

</details>

---

## 📚 Python Async/Await

### ❓ Câu 4: Sự khác biệt giữa Sync và Async là gì?

<details>
<summary>👉 Xem đáp án</summary>

**Đồng bộ (Sync)** - Chạy tuần tự, phải đợi task trước xong mới chạy task sau:
```
Request 1 ────> (3s) ────> Xong
                           Request 2 ────> (4s) ────> Xong
                                                      Request 3 ────> (5s) ────> Xong
Tổng: 12 giây
```

**Bất đồng bộ (Async)** - Chạy song song, tất cả task chạy cùng lúc:
```
Request 1 ────> (3s) ────> Xong
Request 2 ────> (4s) ──────────> Xong
Request 3 ────> (5s) ────────────────> Xong
Tổng: ~5 giây (bằng task lâu nhất)
```

</details>

---

### ❓ Câu 5: Tại sao gọi hàm `async` mà nó không chạy ngay?

```python
async def say_hello():
    print("Hello!")

result = say_hello()  # Tại sao không in ra "Hello!"?
```

<details>
<summary>👉 Xem đáp án</summary>

Khi định nghĩa hàm với `async def`, Python biến nó thành **coroutine function**.

| Loại hàm | Khi gọi | Kết quả |
|----------|---------|---------|
| Hàm thường `def` | `say_hello()` | **Thực thi ngay** |
| Hàm async `async def` | `say_hello()` | **Không thực thi**, trả về `coroutine object` |

**Coroutine** giống như **"công thức nấu ăn"** - bạn có công thức nhưng chưa nấu!

</details>

---

### ❓ Câu 6: Làm sao để coroutine THỰC SỰ chạy?

<details>
<summary>👉 Xem đáp án</summary>

**Cách 1:** Dùng `await` (bên trong hàm async khác)
```python
async def main():
    result = await say_hello()  # ✅ CHẠY và đợi kết quả
```

**Cách 2:** Dùng `asyncio.run()` hoặc `asyncio.gather()`
```python
# Chạy 1 coroutine
asyncio.run(say_hello())  # ✅ CHẠY

# Chạy nhiều coroutines song song
await asyncio.gather(task1, task2, task3)  # ✅ CHẠY TẤT CẢ
```

</details>

---

### ❓ Câu 7: Đoạn code này làm gì? Tại sao CHƯA chạy ngay?

```python
tasks = [
    ask_llm_async(i+1, q) 
    for i, q in enumerate(questions)
]
```

<details>
<summary>👉 Xem đáp án</summary>

Đoạn code này **tạo danh sách 3 coroutine objects** (chưa chạy):

1. `ask_llm_async(1, "Câu hỏi 1")` → coroutine object
2. `ask_llm_async(2, "Câu hỏi 2")` → coroutine object
3. `ask_llm_async(3, "Câu hỏi 3")` → coroutine object

**Chưa chạy vì:** Hàm `async` chỉ tạo ra "lời hứa", cần `await` hoặc `asyncio.gather()` để kích hoạt!

</details>

---

### ❓ Câu 8: `asyncio.gather(*tasks)` hoạt động như thế nào?

<details>
<summary>👉 Xem đáp án</summary>

```python
results = await asyncio.gather(*tasks)
```

| Phần | Ý nghĩa |
|------|---------|
| `*tasks` | Unpack list thành từng coroutine riêng lẻ |
| `asyncio.gather()` | Chạy tất cả coroutines **SONG SONG** |
| `await` | Đợi cho đến khi **TẤT CẢ** đều hoàn thành |
| `results` | List chứa kết quả của tất cả tasks (theo thứ tự) |

</details>

---

## 🔤 Tokenization (Ngày 1)

### ❓ Câu 9: Token là gì? LLM có hiểu "từ" không?

<details>
<summary>👉 Xem đáp án</summary>

**LLM KHÔNG hiểu từ như con người!** Chúng xử lý các **Token** - là các mảnh văn bản nhỏ.

Token có thể là:
- Một từ hoàn chỉnh: `"Hello"` → 1 token
- Một phần của từ: `"Lập trình"` → `"L"` + `"ập"` + `" trình"` = 3 tokens
- Dấu câu hoặc khoảng trắng: `","` → 1 token

**LLM thực chất là bộ máy dự đoán xác suất token tiếp theo!**

</details>

---

### ❓ Câu 10: Tại sao LLM thường tính toán sai?

```python
"12345"    → ['123', '45']      # 2 tokens
"1000000"  → ['100', '000', '0'] # 3 tokens
```

<details>
<summary>👉 Xem đáp án</summary>

**Vì các con số bị chia cắt thành tokens không logic!**

| Số | Cách LLM nhìn | Vấn đề |
|----|---------------|--------|
| `12345` | `123` + `45` | Không phải từng chữ số |
| `1000000` | `100` + `000` + `0` | Chia không đều |

LLM xử lý toán trên các token, không phải trên từng chữ số → dễ tính sai!

</details>

---

### ❓ Câu 11: Tại sao LLM đếm sai số chữ 'r' trong "strawberry"?

<details>
<summary>👉 Xem đáp án</summary>

```
"strawberry" được tokenize thành:
   Token 1: 'st'    (0 chữ 'r')
   Token 2: 'raw'   (1 chữ 'r')
   Token 3: 'berry' (2 chữ 'r')
```

**LLM không nhìn từng chữ cái!** Nó chỉ thấy 3 tokens.

Để đếm chữ 'r', LLM phải:
1. Hiểu mỗi token chứa những chữ gì (khó)
2. Đếm trong từng token (không được train cho việc này)

→ Đây là lý do LLM đời cũ thường trả lời sai: "2 chữ r" thay vì "3 chữ r"

</details>

---

### ❓ Câu 12: LLM đời mới (GPT-4o, Claude 3.5) fix vấn đề đếm chữ cái bằng cách nào?

<details>
<summary>👉 Xem đáp án</summary>

Các LLM đời mới sử dụng **3 kỹ thuật chính**:

**1. Chain-of-Thought (Suy luận từng bước)**
```
Bước 1: Liệt kê từng chữ: s-t-r-a-w-b-e-r-r-y
Bước 2: Đánh dấu chữ 'r': s-t-[r]-a-w-b-e-[r]-[r]-y
Bước 3: Đếm: 3 chữ 'r'
```

**2. Tool Use (Sử dụng công cụ)**
- LLM gọi code Python để đếm chính xác:
```python
"strawberry".count('r')  # → 3
```

**3. Training tốt hơn**
- Được train với nhiều bài toán character-level
- Học cách "phân tích" token thành từng chữ cái khi cần

**Kết quả:** GPT-4o, Claude 3.5, Gemini 1.5 đều trả lời đúng "3 chữ r"!

</details>

---

### ❓ Câu 13: Chi phí API được tính như thế nào?

<details>
<summary>👉 Xem đáp án</summary>

**Chi phí tính theo TOKEN, không phải từ hay ký tự!**

| Text | Ký tự | Từ | Token | Chi phí* |
|------|-------|-----|-------|----------|
| `Hello` | 5 | 1 | 1 | $0.000005 |
| `Xin chào` | 8 | 2 | 3 | $0.000015 |
| `Lập trình AI` | 12 | 3 | 4 | $0.000020 |

*Giả sử $0.005/1K tokens

**Lưu ý:** Tiếng Việt thường tốn nhiều token hơn tiếng Anh!

</details>

---

## 🧠 Prompt Engineering (Ngày 5-6)

### ❓ Câu 14: Zero-shot Prompting là gì?

<details>
<summary>👉 Xem đáp án</summary>

**Zero-shot** = Hỏi LLM trực tiếp **KHÔNG** cung cấp bất kỳ ví dụ nào.

LLM phải tự hiểu task dựa vào kiến thức đã học sẵn.

**Ví dụ:**
```
Prompt: "Phân loại cảm xúc câu sau: 'Bộ phim này hay quá!'"
→ LLM tự hiểu cần trả lời: Positive
```

| Ưu điểm | Nhược điểm |
|----------|------------|
| Đơn giản, nhanh | Có thể sai format |
| Tốn ít token → rẻ | Kém chính xác với task đặc thù |

**Khi nào dùng?** Task phổ biến mà LLM đã "biết" sẵn (dịch thuật, tóm tắt, phân loại đơn giản).

</details>

---

### ❓ Câu 15: Few-shot Prompting là gì? Tại sao cần 3 ví dụ?

<details>
<summary>👉 Xem đáp án</summary>

**Few-shot** = Cung cấp **ví dụ mẫu (Input → Output)** trong prompt trước khi hỏi câu thật.

```python
# Cấu trúc Few-shot trong code:
messages = [
    {"role": "system", "content": "Bạn là trợ lý phân loại cảm xúc."},

    # ── Ví dụ 1 ──
    {"role": "user",      "content": '"Món ăn ngon tuyệt!" → Phân loại?'},
    {"role": "assistant", "content": "Positive"},

    # ── Ví dụ 2 ──
    {"role": "user",      "content": '"Dịch vụ tệ quá!" → Phân loại?'},
    {"role": "assistant", "content": "Negative"},

    # ── Ví dụ 3 ──
    {"role": "user",      "content": '"Cửa hàng mở cửa 8h-22h." → Phân loại?'},
    {"role": "assistant", "content": "Neutral"},

    # ── Câu hỏi THẬT ──
    {"role": "user",      "content": '"Phim hay quá xem 3 lần!" → Phân loại?'},
]
```

**Tại sao 3 ví dụ?**
- 1 ví dụ: LLM có thể hiểu sai pattern
- 2 ví dụ: chưa đủ đa dạng
- **3 ví dụ: đủ để LLM nắm rõ format + logic** ← Sweet spot
- 5+ ví dụ: tốn token, ít cải thiện thêm

</details>

---

### ❓ Câu 16: Chain-of-Thought (CoT) là gì? "Câu thần chú" nào kích hoạt nó?

<details>
<summary>👉 Xem đáp án</summary>

**Chain-of-Thought (CoT)** = Buộc LLM **trình bày logic TỪNG BƯỚC** trước khi đưa ra đáp án.

**"Câu thần chú":** Thêm `"Let's think step by step"` (Hãy suy nghĩ từng bước) vào cuối prompt!

**Ví dụ - Bài toán KHÔNG có CoT:**
```
Prompt: "Mua 5 áo, giá 200k/chiếc, giảm 15%, thuế 10%. Tổng?"
→ LLM: "935,000 VNĐ"  (có thể đúng hoặc sai, không rõ cách tính)
```

**Cùng bài toán CÓ CoT:**
```
Prompt: "... Let's think step by step."
→ LLM:
  Bước 1: Giá gốc = 5 × 200,000 = 1,000,000 VNĐ
  Bước 2: Giảm 15% = 1,000,000 × 0.85 = 850,000 VNĐ
  Bước 3: Thuế 10% = 850,000 × 1.10 = 935,000 VNĐ
  → Đáp án: 935,000 VNĐ ✅
```

| Không CoT | Có CoT |
|-----------|--------|
| Đáp án ngắn, có thể sai | Trình bày rõ ràng từng bước |
| Ít token | Nhiều token hơn |
| Khó kiểm tra logic | Dễ kiểm tra và debug |

</details>

---

### ❓ Câu 17: So sánh chi phí token của 3 kỹ thuật prompting?

<details>
<summary>👉 Xem đáp án</summary>

| Kỹ thuật | Input Tokens | Output Tokens | Tổng chi phí |
|----------|-------------|---------------|-------------|
| **Zero-shot** | ⭐ Ít nhất | Trung bình | 💰 Rẻ nhất |
| **Few-shot** | ⭐⭐⭐ Nhiều (có ví dụ) | Ngắn gọn | 💰💰 Vừa phải |
| **CoT** | ⭐⭐ Vừa | ⭐⭐⭐ Dài (có giải thích) | 💰💰💰 Đắt nhất |

**Kết hợp tối ưu:**
```
Few-shot + CoT = Combo mạnh nhất! (nhưng cũng đắt nhất)
```

**Quy tắc chọn:**
- Task đơn giản → **Zero-shot** (tiết kiệm)
- Cần đúng format → **Few-shot** (chính xác)
- Cần suy luận → **CoT** (logic)
- Task phức tạp + cần format → **Few-shot + CoT** (toàn diện)

</details>

---

## 📝 Ôn tập Feynman: Giải thích "Tokenization" (Ngày 7)

### ❓ Câu 18: Hãy giải thích Tokenization cho người không biết gì về AI

<details>
<summary>👉 Xem đáp án</summary>

### 🍕 Tokenization = Cắt pizza thành miếng

Tưởng tượng bạn có một cái pizza lớn (= đoạn văn bản). Bạn không thể nhét cả cái pizza vào miệng cùng lúc, phải **cắt thành từng miếng** để ăn.

**Tokenization** cũng vậy — nó **cắt văn bản thành những mảnh nhỏ (gọi là token)** để máy tính có thể "ăn" được.

**Ví dụ đời thường:**

```
Câu: "Tôi yêu Việt Nam"

Con người đọc:  "Tôi" "yêu" "Việt" "Nam"     (4 từ)
Máy tính đọc:  "T" "ôi" " yêu" " Vi" "ệt" " Nam"  (6 mảnh = 6 tokens)
```

**Tại sao máy không cắt theo từ như người?**

Vì máy dùng **từ điển có sẵn** (khoảng 50,000-100,000 mảnh). Nếu từ nào có trong từ điển → giữ nguyên. Nếu không → chia nhỏ hơn.

- `"Hello"` → có trong từ điển → **1 token** ✅
- `"Xin chào"` → không có nguyên → chia thành `"X"` + `"in"` + `" ch"` + `"ào"` = **4 tokens**

**Vậy sao phải quan tâm?**

1. **Tiền bạc:** API tính tiền theo token. Tiếng Việt tốn ~2-3x token so với tiếng Anh → **đắt hơn!**
2. **Giới hạn:** Mỗi model có giới hạn token (ví dụ 128,000 tokens). Viết tiếng Việt = hết giới hạn nhanh hơn.
3. **Tính toán sai:** LLM nhìn `"12345"` thành `["123", "45"]` chứ không phải từng số → hay tính sai!

**Tóm lại:** Tokenization giống như cắt pizza — cách cắt ảnh hưởng đến cách ăn (xử lý), giá tiền, và chất lượng! 🍕

</details>

---

## 📁 Files trong project

| File | Mô tả |
|------|-------|
| `hello_llm.py` | Demo gọi Azure OpenAI cơ bản (sync) |
| `async_llm.py` | Demo gọi Azure OpenAI bất đồng bộ (async) |
| `token_kung_fu.py` | Demo tokenization - cách LLM "nhìn" văn bản |
| `prompt_engineering.py` | Demo 3 kỹ thuật prompting: Zero-shot, Few-shot, CoT |

---

## 🔧 Cấu hình

Tạo file `.env` với các biến:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```
