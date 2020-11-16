from typing import Optional, Any

from telegram_bot.objects import Product


def telegram_message(product: Product) -> str:
    from telegram_bot import DEVICES, SOCIAL, CHANNEL, STOCK_ALERT

    add_lines = lambda s, n=1: ("\n" * n) + s

    def quote(s: Optional[Any]) -> Optional[str]:
        chars = '-+().!*_~=|'
        if not s:
            return None
        for char in chars:
            s = str(s).replace(char, f"\\{char}").strip()
        return s

    def social_link(name: str, url: str) -> str:
        return f"[{name.title()}]({quote(url)})"

    default_icon = DEVICES.get('default')

    m = f"[{DEVICES.get(product.product_type, default_icon)}]({quote(product.picture_url)}) {quote(product.title)}"

    if product.before_price:
        price_line = f"❌ ~{quote(product.before_price)} €~ 🔥 Ahora: *{quote(product.now_price)} €*"
    else:
        price_line = f"💰 Precio: {quote(product.now_price)} €"

    m += add_lines(price_line, 2)

    if product.stock <= STOCK_ALERT:
        if product.stock == 1:
            m += add_lines(f"*Solo queda {product.stock} disponible* ‼️")
        else:
            m += add_lines(f"*Solo quedan {product.stock} disponibles* ‼️")

    if product.features:
        m += add_lines("✅ *Características:*", 2)
        for feature in product.features:
            m += add_lines(f"🔸 {quote(feature)}")

    if product.description:
        m += add_lines(f"ℹ️ {quote(product.description)}", 2)

    social_line = ''
    for name, url in SOCIAL.items():
        social_line += f"{social_link(name, url)} "

    m += add_lines(f"🧐 {quote(CHANNEL)}", 2)
    m += add_lines(f"👉 Síguenos en {social_line}")

    return m
