import asyncio
from playwright.async_api import async_playwright
import requests

TELEGRAM_TOKEN = '8047337853:AAGizHiBxQSrrUl8IQw-TX9Zjz86PcJGhlU'
TELEGRAM_CHAT_ID = '6821521589'

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensagem})

def analisar_resultados(ultimos_resultados):
    if ultimos_resultados[-3:] == ['preto', 'vermelho', 'vermelho']:
        return 'branco'
    elif ultimos_resultados[-1] == 'preto':
        return 'vermelho'
    elif ultimos_resultados[-1] == 'vermelho':
        return 'preto'
    return 'aguardar'

async def buscar_resultados():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://blaze.bet.br/pt/games/double")

        print("Bot iniciado. Aguardando sinais...")

        resultados_anteriores = []

        while True:
            await page.reload()
            await page.wait_for_selector('.entries .entry')
            elements = await page.query_selector_all('.entries .entry')
            resultados = []

            for el in elements[:20]:
                cor = await el.get_attribute("class")
                if "white" in cor:
                    resultados.append("branco")
                elif "red" in cor:
                    resultados.append("vermelho")
                else:
                    resultados.append("preto")

            resultados.reverse()

            if resultados != resultados_anteriores:
                resultados_anteriores = resultados
                proxima = analisar_resultados(resultados)
                if proxima != 'aguardar':
                    enviar_telegram(f"🎯 Apostar na próxima: {proxima.upper()}")

            await asyncio.sleep(20)

if __name__ == "__main__":
    asyncio.run(buscar_resultados())
