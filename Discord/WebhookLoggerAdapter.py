import logging
import aiohttp

class WebhookLoggerAdapter:
    def __init__(self, logger: logging.Logger, webhook_url: str = None):
        self.logger = logger
        self.webhook_url = webhook_url

    async def _send_webhook(self, content: str):
        if not self.webhook_url:
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json={"content": content}) as resp:
                    if resp.status >= 400:
                        self.logger.warning(f"Webhook failed: {resp.status} {await resp.text()}")
        except Exception as e:
            self.logger.warning(f"Exception during webhook send: {e}")

    async def info(self, message: str, *args, webhook: bool = False, **kwargs):
        self.logger.info(message, *args, **kwargs)
        if webhook and self.webhook_url:
            await self._send_webhook(f"[INFO] {message}")

    async def error(self, message: str, *args, webhook: bool = False, **kwargs):
        self.logger.error(message, *args, **kwargs)
        if webhook and self.webhook_url:
            await self._send_webhook(f"[ERROR] {message}")

    async def warning(self, message: str, *args, webhook: bool = False, **kwargs):
        self.logger.warning(message, *args, **kwargs)
        if webhook and self.webhook_url:
            await self._send_webhook(f"[WARNING] {message}")

    # Delegate useful logger methods
    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def removeHandler(self, handler):
        self.logger.removeHandler(handler)

    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def isEnabledFor(self, level):
        return self.logger.isEnabledFor(level)

