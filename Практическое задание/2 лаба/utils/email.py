import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from config import config

logger = logging.getLogger(__name__)

async def send_order_email(order_id: int, user, items: list, total: float, address: str):
    """Send order notification to admin email."""
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        logger.warning("SMTP not configured, skipping email")
        return

    try:
        subject = f"Новый заказ #{order_id} — АвтоЗапчасти"
        items_html = "".join(
            f"<tr><td>{i['name']}</td><td>{i['quantity']}</td><td>{float(i['price']):.2f} ₽</td></tr>"
            for i in items
        )
        body = f"""
        <html><body>
        <h2>🛒 Новый заказ #{order_id}</h2>
        <p><b>Покупатель:</b> {getattr(user, 'full_name', '')} (@{getattr(user, 'username', '')})</p>
        <p><b>Адрес доставки:</b> {address}</p>
        <h3>Состав заказа:</h3>
        <table border="1" cellpadding="5">
            <tr><th>Товар</th><th>Кол-во</th><th>Цена</th></tr>
            {items_html}
        </table>
        <p><b>Итого: {total:.2f} ₽</b></p>
        </body></html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config.SMTP_USER
        msg["To"] = config.ADMIN_EMAIL
        msg.attach(MIMEText(body, "html", "utf-8"))

        await aiosmtplib.send(
            msg,
            hostname=config.SMTP_HOST,
            port=config.SMTP_PORT,
            username=config.SMTP_USER,
            password=config.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info(f"Order #{order_id} email sent to {config.ADMIN_EMAIL}")
    except Exception as e:
        logger.error(f"Failed to send email for order #{order_id}: {e}")
