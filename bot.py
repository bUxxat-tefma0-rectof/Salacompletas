import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import mercadopago
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_PUBLIC_TOKEN")
sdk = mercadopago.SDK(os.getenv("MERCADO_PAGO_ACCESS_TOKEN"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Bot de teste de pagamento.\nUse: /recarga 10")

@dp.message(Command("recarga"))
async def recarga(message: types.Message):
    try:
        # Pega o valor após o comando
        args = message.text.split()
        if len(args) < 2:
            return await message.answer("Use: /recarga 10")
        
        valor = float(args[1])
        
        # Cria preferência de pagamento
        preference_data = {
            "items": [
                {
                    "title": "Recarga Xixa Marketing",
                    "quantity": 1,
                    "unit_price": valor
                }
            ],
            "back_urls": {
                "success": "https://seusite.com/sucesso",
                "failure": "https://seusite.com/falha",
                "pending": "https://seusite.com/pendente"
            },
            "auto_return": "approved"
        }
        
        preference_response = sdk.preference().create(preference_data)
        payment_url = preference_response["response"]["init_point"]
        
        await message.answer(f"Pagamento de R$ {valor:.2f} gerado!\n\n{payment_url}")
        
    except Exception as e:
        await message.answer(f"Erro: {str(e)}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
