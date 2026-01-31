# import library
import asyncio
import os
import time
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

# 1. Cấu hình môi trường
load_dotenv()

# Azure OpenAI configuration from .env
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# LƯU Ý: Dùng AsyncAzureOpenAI thay vì AzureOpenAI
client = AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

# 2. Hàm gửi request đơn lẻ (bất đồng bộ)
async def ask_llm_async(question_id : int, question : str):
    print(f"➡️ [Task {question_id}] Bắt đầu gửi: '{question}'...")
    start_time = time.time()
    
    response = await client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "Bạn trả lời cực ngắn gọn (dưới 1 câu)."},
            {"role": "user", "content": question}
        ]
    )
    
    duration = time.time() - start_time
    answer = response.choices[0].message.content
    print(f"✅ [Task {question_id}] Hoàn thành trong {duration:.2f}s")
    
    return {
        "id": question_id,
        "question": question,
        "answer": answer,
        "duration": duration
    }

# 3. Hàm chính (Orchestrator)
async def main():
    questions = [
        "Định nghĩa AI trong 5 từ.",
        "Python là gì?", 
        "Tại sao bầu trời màu xanh?"
    ]
    
    print(f"🚀 BẮT ĐẦU GỬI {len(questions)} REQUESTS CÙNG LÚC...\n")
    total_start = time.time()

    # Tạo danh sách các coroutine (chưa chạy ngay)
    tasks = [
        ask_llm_async(i+1, q) 
        for i, q in enumerate(questions)
    ]
    
    # asyncio.gather kích hoạt tất cả tasks chạy song song
    # và chờ cho đến khi TẤT CẢ đều xong
    results = await asyncio.gather(*tasks)
    
    total_end = time.time()
    total_duration = total_end - total_start

    # 4. Phân tích hiệu năng (Tư duy Kỹ sư)
    print("\n" + "="*40)
    print("KẾT QUẢ TỔNG HỢP")
    print("="*40)
    
    sum_duration = 0
    for res in results:
        print(f"- Q: {res['question']}")
        print(f"  A: {res['answer']}")
        print(f"  ⏱️ Thời gian riêng: {res['duration']:.2f}s")
        sum_duration += res['duration']

    print("-" * 40)
    print(f"Tổng thời gian nếu chạy tuần tự (Sync): {sum_duration:.2f}s")
    print(f"Tổng thời gian thực tế chạy Async:     {total_duration:.2f}s")
    
    # Chứng minh hiệu quả
    saved_time = sum_duration - total_duration
    if saved_time > 0:
        print(f"⚡ Bạn đã tiết kiệm được: {saved_time:.2f}s (Nhanh hơn {sum_duration/total_duration:.1f}x)")
    else:
        print("Mạng quá nhanh hoặc chỉ có 1 request nên không thấy rõ khác biệt.")

if __name__ == "__main__":
    # Điểm khởi đầu của chương trình Async
    asyncio.run(main())
