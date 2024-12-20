import aiohttp
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from data import rex
from pyrogram import Client

Client.parse_mode = 'html'

class SiteChecker:
    def __init__(self, url):
        self.url = url
        self.server = 'Unknown'
        self.security_message = 'Not found'
        self.payment_gateways = []

    async def fetch_site_data(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=headers) as response:
                    response.raise_for_status()

                    self.server = response.headers.get('Server', 'Unknown')

                    if self.server == 'Unknown':
                        content = await response.read()
                        soup = BeautifulSoup(content, 'html.parser')
                        meta_server = soup.find('meta', attrs={'name': 'generator'})
                        if meta_server:
                            self.server = meta_server.get('content', 'Unknown')

                    content = await response.read()
                    await self.check_security(content)
                    await self.find_payment_gateways(content)

        except aiohttp.ClientError as e:
            return {
                "Sitio": self.url,
                "Valid": "Error",
                "Web": self.url,
                "Server": "Not Found",
                "Protections": "Not Found",
                "Gateways": "Not Found"
            }

        return self.format_result()

    async def check_security(self, content):
        security_services = ["Cloudflare", "Akamai", "Cloudfront", "Recaptcha", "captcha", "hcaptcha"]
        soup = BeautifulSoup(content, 'html.parser')

        for service in security_services:
            if soup.find_all(string=re.compile(r'\b' + re.escape(service) + r'\b', re.I)):
                self.security_message = service
                break

    async def find_payment_gateways(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        gateways = [
            "Stripe", "Square", "PayPal", "Shopify", "Braintree", "BraintreeAvs",
            "Adyen", "Eway", "Zuora", "Bluepay", "Usaepay", "NMI", "Payflow", "WooCommerce", "Bambora", "Payeezy", "Magento", "Cybersource", "Recurly", "Moneris", "PayConex", "Elavon", "Authorize.net", "Spreedly", "Chase", "Worldpay", "First Data", "Sagepay", "Convergepay", "Wix"
        ]

        found_gateways = set()
        for gateway in gateways:
            if soup.find_all(string=re.compile(r'\b' + re.escape(gateway) + r'\b', re.I)):
                found_gateways.add(gateway)

        self.payment_gateways = list(found_gateways)

    def format_result(self):
        gateways_message = ", ".join(self.payment_gateways) if self.payment_gateways else "No gateways found"

        result = {
            "Sitio": self.url,
            "Valid": True,
            "Web": self.url,
            "Server": self.server,
            "Protections": self.security_message,
            "Gateways": gateways_message
        }

        return result


@rex(["site"])
async def site_info(client, msg):
    site_url = msg.text.split(" ", 1)[1] if len(msg.text.split(" ", 1)) > 1 else None
    if not site_url:
        await msg.reply_text("<b>[⌁](t.me/VortexChekBot) Uso: /site URL</b>", reply_to_message_id=msg.id, disable_web_page_preview=True)
        return

    site_url = site_url.split()[0]
    parsed_url = urlparse(site_url.strip())
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    loading_msg = await msg.reply_text(f"<b>[⌁](t.me/VortexChekBot) Buscando Site</b> <code>{base_url}</code>", reply_to_message_id=msg.id, disable_web_page_preview=True)

    start_time = time.time()

    site_checker = SiteChecker(base_url)

    site_data = await site_checker.fetch_site_data()

    elapsed_time = round(time.time() - start_time, 2)

    result = f"""
<b>[⌁](t.me/VortexChekBot) SITE SECURITY</b>
━━━━━━━━━━━
<b>[⌁](t.me/VortexChekBot) Site:</b> <code>{site_data['Sitio']}</code>
<b>[⌁](t.me/VortexChekBot) Server: {site_data['Server'].capitalize()}</b>
<b>[⌁](t.me/VortexChekBot) Protection: {site_data['Protections']}</b>
<b>[⌁](t.me/VortexChekBot) Gateway: {site_data['Gateways']}</b>
━━━━━━━━━━━
<b>[⌁](t.me/VortexChekBot) Time: {elapsed_time}</b> <b>Seconds</b>
<b>[⌁](t.me/VortexChekBot) Request By: @{msg.from_user.username}</b>
"""

    await loading_msg.edit_text(text=result, disable_web_page_preview=True)
