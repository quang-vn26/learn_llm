# Tuần 4 - Module: Tiện ích (Utils)
# ====================================
# Đếm token, truncate text - tái sử dụng từ Tuần 2
# Tách riêng để các module khác import được

import tiktoken

# Encoding cho GPT-4o (tương thích Azure OpenAI)
encoding = tiktoken.encoding_for_model("gpt-4o")


def count_tokens_text(text: str) -> int:
    """Đếm số token của một đoạn text."""
    return len(encoding.encode(text))


def count_tokens_messages(messages: list[dict]) -> int:
    """
    Đếm tổng token của list messages (bao gồm overhead).
    Mỗi message có ~4 tokens overhead (role, formatting).
    """
    total = 0
    for msg in messages:
        total += 4  # overhead: role + formatting
        total += len(encoding.encode(msg["content"]))
    total += 2  # overhead cho response format
    return total


def truncate_text(text: str, max_tokens: int) -> str:
    """
    Cắt text sao cho không vượt quá max_tokens.
    Ưu tiên cắt tại ranh giới câu > ranh giới từ.
    """
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return text

    truncated_tokens = tokens[:max_tokens]
    truncated_text = encoding.decode(truncated_tokens)

    # Tìm ranh giới câu gần nhất
    sentence_ends = ['.', '!', '?', '。']
    last_sentence_end = -1
    for i, char in enumerate(truncated_text):
        if char in sentence_ends:
            last_sentence_end = i

    if last_sentence_end > len(truncated_text) * 0.5:
        return truncated_text[:last_sentence_end + 1]

    # Fallback: ranh giới từ
    last_space = truncated_text.rfind(' ')
    if last_space > 0:
        return truncated_text[:last_space] + "..."

    return truncated_text + "..."
