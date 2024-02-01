import hashlib
import re
import time

from playwright.sync_api import sync_playwright

from Business import Business
from functions import save_businesses


def scrape(city_list, b_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_selector('//input[@id="searchboxinput"]')
        page.wait_for_timeout(5000)
        cnt = 0

        for l_i in city_list.keys():
            for l_j in city_list[l_i]:
                for l_k in b_list.keys():
                    try:
                        if not b_list[l_k]:
                            b_list[l_k].append(l_k)
                    except:
                        pass

                    for l_l in b_list[l_k]:
                        cnx = 1
                        l_i = l_i.replace(" ", "-")
                        l_j = l_j.replace(" ", "-")
                        l_k = l_k.replace(" ", "-")
                        l_l = l_l.replace(" ", "-")

                        hash_object = hashlib.sha256(str(l_i + l_j + l_l).encode())
                        hashed_value = hash_object.hexdigest()
                        business_listtt = []

                        search_key = f'{l_l} in {l_j}, {l_i}'
                        cnt += 1
                        print('//////////////////////////////////------', cnt,
                              '------//////////////////////////////////')

                        if page.locator('//button[contains(@class, "yAuNSb")]').count() > 0:
                            try:
                                page.locator('//button[contains(@class, "yAuNSb")]').click()
                            except:
                                continue

                        page.wait_for_timeout(1000)
                        page.locator('//input[@id="searchboxinput"]').fill(search_key)
                        page.keyboard.press("Enter")

                        print(f"scrapping for {l_l} in {l_j}, {l_i} ......")

                        final_s = 'na'
                        ts = time.time()
                        while True:
                            if page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() > 0:
                                final_s = '//a[contains(@href, "https://www.google.com/maps/place")]'
                                break
                            if page.locator('//h1[contains(@class, "DUwDvf")]').count() > 0:
                                final_s = '//h1[contains(@class, "DUwDvf")]'
                                break
                            tm = time.time() - ts
                            if tm > 20:
                                page.locator('//input[@id="searchboxinput"]').fill(search_key)
                                page.keyboard.press("Enter")
                                break

                        if final_s == '//a[contains(@href, "https://www.google.com/maps/place")]':
                            page.hover(final_s)

                            previously_counted = 0

                            while True:
                                page.mouse.wheel(0, 10000)

                                if page.locator(final_s).count() == previously_counted:
                                    listings = page.locator(final_s).all()
                                    break
                                else:
                                    previously_counted = page.locator(final_s).count()

                            prv_name = "na"

                            for listing in listings:
                                try:
                                    listing.click()
                                except:
                                    print("Timeout error occurred while clicking the element. Skipping this entry.")
                                    continue

                                if page.locator('//div[contains(@class, "GZz5vb")]').count() != 0:
                                    print('Sponsored...')
                                    continue

                                name_xpath = '//h1[contains(@class, "DUwDvf")]'
                                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                                reviews_span_xpath = '//div[@class="F7nice "]'

                                business = Business()
                                business.state = l_i
                                business.city = l_j
                                business.main_business = l_k
                                business.sub_business = l_l
                                business.hash_value = hashed_value

                                ts = time.time()
                                bs = 0
                                while True:
                                    if page.locator(name_xpath).count() <= 0 or page.locator(
                                            name_xpath).inner_text() == prv_name:
                                        try:
                                            listing.click()
                                        except:
                                            print(
                                                "Timeout error occurred while clicking the element. Skipping this entry.")
                                            continue

                                    else:
                                        break
                                    tm = time.time() - ts
                                    if tm > 10:
                                        bs = 1
                                        break
                                if bs == 1:
                                    continue
                                try:
                                    page.wait_for_selector(name_xpath)
                                except:
                                    continue
                                txt = page.locator(name_xpath).inner_text()
                                prv_name = txt
                                try:
                                    business.name = page.locator(name_xpath).inner_text(timeout=20)
                                    print(business.name)
                                except:
                                    business.name = ""
                                try:
                                    business.address = page.locator(address_xpath).inner_text(timeout=20)
                                except:
                                    business.address = ""
                                try:
                                    business.website = page.locator(website_xpath).inner_text(timeout=20)
                                except:
                                    business.website = ""
                                try:
                                    business.phone_number = page.locator(phone_number_xpath).inner_text(timeout=20)
                                except:
                                    business.phone_number = ""

                                try:
                                    html = page.locator(reviews_span_xpath).inner_html(timeout=20)
                                    rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
                                    if rating_match:
                                        business.reviews_average = rating_match.group(1)
                                    else:
                                        business.reviews_average = 0.0

                                    reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
                                    if reviews_match:
                                        business.reviews_count = reviews_match.group(1).replace(',', '')
                                    else:
                                        business.reviews_count = 0

                                except:
                                    business.reviews_count = 0
                                    business.reviews_average = 0.0

                                isitstuck = 0
                                try:
                                    page.wait_for_selector('//button[contains(@data-value, "Share")]', timeout=1000)
                                    page.locator('//button[contains(@data-value, "Share")]').click()
                                    isitstuck = 1
                                    page.wait_for_selector('//button[contains(@data-tooltip, "Embed a map")]',
                                                           timeout=2000)
                                    page.locator('//button[contains(@data-tooltip, "Embed a map")]').click()
                                    page.wait_for_selector(
                                        '//div[@id="modal-dialog"]//input[contains(@class, "yA7sBe")]',
                                        timeout=2000)
                                    copied_text = page.locator(
                                        '//div[@id="modal-dialog"]//input[contains(@class, "yA7sBe")]').get_attribute(
                                        'value')
                                    business.map = copied_text
                                    page.wait_for_selector('//button[contains(@class, "AmPKde")]', timeout=2000)
                                    page.locator(
                                        '//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()

                                except:
                                    if isitstuck == 1:
                                        try:
                                            page.wait_for_selector('//button[contains(@class, "AmPKde")]', timeout=3000)
                                            page.locator(
                                                '//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()
                                        except:
                                            pass

                                    business.map = ""

                                if business.map == '':
                                    query = search_key.replace(' ', '%20').replace(',', '%C')
                                    business.map = f'<iframe width="600" height="450" ' \
                                                   f'src="https://maps.google.com/maps?width=600&amp;height=450&amp;hl=en&amp;q={query}&amp;ie=UTF8&amp;t=&amp;z=10&amp;iwloc=B&amp;output=embed" ' \
                                                   f'frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>'

                                if business.name != "" and len(business.name) < 255 and len(
                                        business.address) < 255 and len(business.website) < 255 and len(
                                    business.phone_number) < 20:
                                    business_listtt.append(business)
                                print(f"add entry {cnx}")
                                cnx += 1

                            print(f"scrapping for {l_l} in {l_j}, {l_i} completed")

                        elif final_s == '//h1[contains(@class, "DUwDvf")]':
                            name_xpath = ' // h1[contains( @class, "DUwDvf")]'
                            address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                            reviews_span_xpath = '//div[@class="F7nice "]'

                            business = Business()
                            business.state = l_i
                            business.city = l_j
                            business.main_business = l_k
                            business.sub_business = l_l
                            business.hash_value = hashed_value

                            try:
                                business.name = page.locator(name_xpath).inner_text(timeout=20)
                            except:
                                business.name = ""
                            try:
                                business.address = page.locator(address_xpath).inner_text(timeout=20)
                            except:
                                business.address = ""
                            try:
                                business.website = page.locator(website_xpath).inner_text(timeout=20)
                            except:
                                business.website = ""
                            try:
                                business.phone_number = page.locator(phone_number_xpath).inner_text(timeout=20)
                            except:
                                business.phone_number = ""
                            try:
                                html = page.locator(reviews_span_xpath).inner_html(timeout=20)

                                rating_match = re.search(r'<span aria-hidden="true">([\d.]+)</span>', html)
                                if rating_match:
                                    business.reviews_average = rating_match.group(1)
                                else:
                                    business.reviews_average = 0.0

                                reviews_match = re.search(r'aria-label="([\d,]+) reviews"', html)
                                if reviews_match:
                                    business.reviews_count = reviews_match.group(1).replace(',',
                                                                                            '')  # Remove commas
                                else:
                                    business.reviews_count = 0

                            except:
                                business.reviews_count = 0  # Default value
                                business.reviews_average = 0.0  # Default value

                            isitstuck = 0
                            try:
                                page.wait_for_selector(' // button[contains( @data-value, "Share")]', timeout=1000)
                                print('share.....')
                                page.locator(' // button[contains( @data-value, "Share")]').click()
                                isitstuck = 1
                                print('share')
                                page.wait_for_selector(' // button[contains( @data-tooltip, "Embed a map")]',
                                                       timeout=2000)
                                page.locator(' // button[contains( @data-tooltip, "Embed a map")]').click()
                                print('Embed a map')

                                page.wait_for_selector(
                                    ' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]', timeout=2000)
                                copied_text = page.locator(
                                    ' //div[@id="modal-dialog"]// input[contains( @class, "yA7sBe")]').get_attribute(
                                    'value')

                                business.map = copied_text
                                page.wait_for_selector(' // button[contains( @class, "AmPKde")]', timeout=2000)
                                page.locator('//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()

                                print('closed...1')

                            except:
                                if isitstuck == 1:
                                    try:
                                        print("worst")
                                        page.wait_for_selector(' // button[contains( @class, "AmPKde")]', timeout=3000)
                                        page.locator(
                                            '//div[@id="modal-dialog"]//button[contains(@class, "AmPKde")]').click()
                                    except:
                                        pass

                                business.map = ""
                            if business.map == '':
                                querry = search_key.replace(' ', '%20').replace(',', '%C')
                                business.map = maps = f'<iframe width="600" height="450" src="https://maps.google.com/maps?width=600&amp;height=450&amp;hl=en&amp;q={querry}&amp;ie=UTF8&amp;t=&amp;z=10&amp;iwloc=B&amp;output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>'

                            if business.name != "" and len(business.name) < 255 and len(business.address) < 255 and len(
                                    business.website) < 255 and len(business.phone_number) < 20:
                                business_listtt.append(business)

                            print(f"add entry {cnx}")
                            cnx += 1
                            print(f"scrapping for {l_l} in {l_j}, {l_i} completed")

                        else:
                            print("page not found")
                            continue

                        if len(business_listtt) > 0:
                            save_businesses(business_listtt)
        browser.close()
