# Tuần 4 - Module: Memory (Bộ nhớ hội thoại)
# =============================================
# Quản lý history với FIFO trim - Tái sử dụng từ Tuần 3

from chatbot.utils import count_tokens_messages

# System prompt mặc định
DEFAULT_SYSTEM_PROMPT = "Bạn là trợ lý AI thân thiện và thông minh. Trả lời bằng tiếng Việt, ngắn gọn nhưng đầy đủ."


class ChatMemory:
    """
    Quản lý bộ nhớ hội thoại cho chatbot.
    
    - Lưu trữ history dạng List[Dict]
    - Tự động trim khi vượt max_tokens (FIFO)
    - Luôn giữ system prompt
    """

    def __init__(self, system_prompt: str = DEFAULT_SYSTEM_PROMPT, max_tokens: int = 3000):
        self.max_tokens = max_tokens
        self.history: list[dict] = [
            {"role": "system", "content": system_prompt}
        ]
        self._total_tokens_used = 0  # Tổng token đã dùng (tích lũy)

    def add_user_message(self, content: str):
        """Thêm tin nhắn người dùng vào history."""
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str):
        """Thêm câu trả lời AI vào history."""
        self.history.append({"role": "assistant", "content": content})

    def add_token_usage(self, total_tokens: int):
        """Cộng dồn tổng token đã dùng."""
        self._total_tokens_used += total_tokens

    def trim(self) -> int:
        """
        Trim history bằng FIFO nếu vượt max_tokens.
        Returns: số message đã xóa.
        """
        before = len(self.history)

        if count_tokens_messages(self.history) <= self.max_tokens:
            return 0

        # Giữ system message (index 0)
        system_msg = [self.history[0]]
        conversation = self.history[1:]

        while conversation and count_tokens_messages(system_msg + conversation) > self.max_tokens:
            conversation.pop(0)  # FIFO: xóa tin cũ nhất

        self.history = system_msg + conversation
        removed = before - len(self.history)
        return removed

    def clear(self):
        """Xóa toàn bộ history, giữ lại system prompt."""
        system_msg = self.history[0]
        self.history = [system_msg]
        self._total_tokens_used = 0

    def get_messages(self) -> list[dict]:
        """Trả về history hiện tại để gửi lên API."""
        return self.history

    @property
    def message_count(self) -> int:
        """Số lượng messages (không tính system)."""
        return len(self.history) - 1

    @property
    def current_tokens(self) -> int:
        """Số token hiện tại trong history."""
        return count_tokens_messages(self.history)

    @property
    def total_tokens_used(self) -> int:
        """Tổng token đã dùng từ đầu phiên."""
        return self._total_tokens_used

    def get_stats(self) -> str:
        """Trả về chuỗi thống kê để hiển thị."""
        return (
            f"📊 Messages: {self.message_count} | "
            f"Context: ~{self.current_tokens} tokens | "
            f"Tổng đã dùng: {self.total_tokens_used} tokens"
        )
