# 🎓 Learn AI - Ôn tập kiến thức

## 📚 Python Async/Await

### ❓ Câu 1: Sự khác biệt giữa Sync và Async là gì?

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

### ❓ Câu 2: Tại sao gọi hàm `async` mà nó không chạy ngay?

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

### ❓ Câu 3: Làm sao để coroutine THỰC SỰ chạy?

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

### ❓ Câu 4: Đoạn code này làm gì? Tại sao CHƯA chạy ngay?

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

### ❓ Câu 5: `asyncio.gather(*tasks)` hoạt động như thế nào?

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

### ❓ Câu 6: Token là gì? LLM có hiểu "từ" không?

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

### ❓ Câu 7: Tại sao LLM thường tính toán sai?

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

### ❓ Câu 8: Tại sao LLM đếm sai số chữ 'r' trong "strawberry"?

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

### ❓ Câu 9: Chi phí API được tính như thế nào?

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

## 📁 Files trong project

| File | Mô tả |
|------|-------|
| `hello_llm.py` | Demo gọi Azure OpenAI cơ bản (sync) |
| `async_llm.py` | Demo gọi Azure OpenAI bất đồng bộ (async) |
| `token_kung_fu.py` | Demo tokenization - cách LLM "nhìn" văn bản |

---

## 🔧 Cấu hình

Tạo file `.env` với các biến:
```
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```
