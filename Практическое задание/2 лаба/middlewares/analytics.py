from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from database.models import log_action

class AnalyticsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable[Any]],
        event: TelegramObject,
        data: dict,
    ) -> Any:
        user = None
        action = ""
        details = ""

        if isinstance(event, Message):
            user = event.from_user
            action = "message"
            details = event.text or ""
        elif isinstance(event, CallbackQuery):
            user = event.from_user
            action = "callback"
            details = event.data or ""

        if user:
            try:
                await log_action(user.id, action, details[:200])
            except Exception:
                pass

        return await handler(event, data)
