# import re
# import time
# import random
# from bots.factory import broadcast_log
# from datetime import datetime
# from selenium.webdriver.common.keys import Keys



def gettinglogs(entry):
    logs = []
    now = datetime.now()
    logs.append("{0}-{1}".format(now, entry))
    broadcast_log(
        "<div class=\"c-feed__item c-feed__item--success\"><p><strong>{0}</strong> - {1}</p></div>".format(
            now.strftime("%m/%d/%Y %H:%M:%S"), entry))


def check(finance):
    type_one_financing = [
        'Bai-Muazzal (Instalment Payment)',
        'Bai-Muazzal (Real Estate)',
        'Demand Loan (Instalment repayment)',
        'Financial Leasing',
        'Hire-Purchase',
        'Hire-Purchase under shirkatul Meelk',
        'Ijara (Lease Finance)',
        'Mortgage loan',
        'Operational Leasing',
        'Other instalment contract',
        'Partially Secured Term Loan',
        'Term Loan',
        'Packing Credit (Instalment repayment)',
    ]

    if finance in type_one_financing:
        return True
    else:
        return False


def format_date(dob):
    # 1994/12/25 to 25/12/1994
    day, month, year = dob.split('/')
    if len(year) < 4:
        year = "19" + year
    new_dob = day + '/' + month + '/' + year
    return new_dob


def format_dob(dob):
    # 1994/12/25 to 25/12/1994
    year, month, day = dob.split('/')
    if len(year) < 4:
        year = "19" + year
    new_dob = day + '/' + month + '/' + year
    return new_dob


def cib_login(driver):
    # gettinglogs("GETTING LOGS!")
    username, password = 'XGK044824', 'Cbl%10011'
    # driver.get(r'file:///C:\Users\Lenovo\Downloads\CITY_BANK_POC\CITY_BANK_POC\Bangladesh_Bank_Credit_Information_Bureau_Login.htm')
    # driver.get(r'file:///rpa/CITY_BANK_POC/Bangladesh_Bank_Credit_Information_Bureau_Login.htm')
    driver.get(r'https://cib.bb.org.bd/login')
    # el_username = driver.find_element_by_xpath(r'/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/div/input')
    el_username = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[1]/div/div/input')
    el_username.clear()
    el_password = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[2]/div/div/input')
    el_password.clear()
    el_captcha_ans = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[3]/div/div/input')
    el_captcha_ans.clear()
    # el_login_btn = driver.find_element_by_xpath(r'//*[@id="loginForm"]/a')

    el_username.send_keys(username)
    # gettinglogs("CIB Login: username")
    el_password.send_keys(password)
    # gettinglogs("CIB Login: password")

    el_question = driver.find_element_by_xpath(r'//*[@id="loginForm"]/div[3]/label')
    text = el_question.text
    num1, num2 = re.findall(r'\d+', text)
    num1, num2 = int(num1), int(num2)
    ans = 0
    if "Addition" in text or "Sum" in text:
        ans = num1 + num2
    elif "Substraction" in text or "Subtraction" in text:
        ans = num1 - num2
    elif "Multiplication" in text:
        ans = num1 * num2
    elif "Division" in text:
        ans = num1 / num2

    el_captcha_ans.send_keys(str(ans))
    # driver.refresh()
    # gettinglogs("CIB Login: Captcha")

    # el_login_btn.click()
    # driver.execute_script("arguments[0].click();", el_login_btn)

    # el_btn_login.click()
    el_captcha_ans.send_keys(Keys.RETURN)

    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[2]/a').click()
    # gettinglogs("CIB Login SUCCESS")

    return True



def cib_fill_form(driver, row, a_nid):
    # print('Title: ', row['full_name'])
    # driver.get(r'file:///rpa/CITY_BANK_POC/Bangladesh_Bank_Credit_Information_Bureau_New_Contract_Inquiry.htm')

    gettinglogs("Filling Up CIB Form for " + str(row['nid']))
    print('BEFORE FILL UP')
    # LAYER ONE::Subject Role & Finance Type
    # try:
    #     el_subject_role_l1_1 = driver.find_element_by_xpath(
    #         r'//*[@id="individualInquiryForm"]/div[2]/div[1]/div/div/div/button')
    #     el_subject_role_l1_1.send_keys(row['subject_role_1'])
    #     gettinglogs("Filling Up Subject Role 1")
    # except Exception as ex:
    #     print("Exception in Subject Role 1")
    #     gettinglogs("Exception in Subject Role 1")
    #     # print(ex)
    #
    # try:
    #     el_subject_role_l1_2 = driver.find_element_by_xpath(
    #         r'//*[@id="individualInquiryForm"]/div[2]/div[1]/div/div/div[2]/button')
    #     el_subject_role_l1_2.send_keys(row['subject_role_2'])
    #     gettinglogs("Filling Up Subject Role 2")
    # except Exception as ex:
    #     print("Subject Role 2")
    #     gettinglogs("Exception in Subject Role 2 Exception")
    #     # print(ex)

    try:
        el_type_of_financing_l1_1 = driver.find_element_by_xpath(
            r'//*[@id="individualInquiryForm"]/div[2]/div[2]/div/div/div/button').click()

        type_of_finance = row['type_of_financing_1']
        driver.find_element_by_link_text(type_of_finance).click()
        # type_of_finance = row['Type_of_financing']
        # el_type_of_financing_l1_1.send_keys(type_of_finance)
        # el_type_of_financing_l1_1.click()
        gettinglogs("Filling Up Type of Financing 1")

        if check(type_of_finance):
            # have those four fields
            # LAYER TWO::Installment Data
            try:
                el_number_of_installment_l2 = driver.find_element_by_xpath(
                    r'//*[@id="individualInquiryForm"]/div[3]/div[1]/div[2]/div/div/input')
                el_number_of_installment_l2.clear()
                el_number_of_installment_l2.send_keys(row['no_of_installment'])
                # el_number_of_installment_l2.send_keys(row['Number_Of_Installment'])
                gettinglogs("Filling Up No of Installment")
            except Exception as ex:
                print("No of Installment")
                # gettinglogs("Exception in No of Installment")
                # print(ex)

            installment_amount = row['installment_amount']
            print('Installment Amount: '+str(installment_amount))
            # el_installment_amount_l2 = driver.find_element_by_css_selector('#individualInquiryForm > div.install_form > div:nth-child(1) > div.col-sm-8 > div > div > input')
            el_installment_amount_l2 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[3]/div[1]/div[3]/div/div/input')
            el_installment_amount_l2.clear()
            el_installment_amount_l2.send_keys(str(int(installment_amount)))
            gettinglogs("Filling Up Installment Amount")


            try:
                el_total_requested_amount_l2 = driver.find_element_by_xpath(
                    r'//*[@id="individualInquiryForm"]/div[3]/div[2]/div[1]/div/div/input')
                el_total_requested_amount_l2.clear()
                # el_total_requested_amount_l2.send_keys(row['Total_requested_amount'])
                el_total_requested_amount_l2.send_keys(row['total_request_amount'])
                gettinglogs("Filling Up Total Requested Amount")
            except Exception as ex:
                print("Requested Amount")


            try:
                el_periodicity_of_payment_l2_1 = driver.find_element_by_xpath(
                    r'//*[@id="individualInquiryForm"]/div[3]/div[2]/div[2]/div/div/div/button').click()

                # el_periodicity_of_payment_l2_1.send_keys(row['periodicity_of_payment_1'])
                driver.find_element_by_link_text(row['periodicity_of_payment_1']).click()
                # driver.find_element_by_link_text(type_of_finance).click()
                # el_periodicity_of_payment_l2_1.send_keys(row['Periodicity_of_payment'])
                # time.sleep(1)
                el_periodicity_of_payment_l2_1.click()
                gettinglogs("Filling Up Periodicity of Payment 1")
            except Exception as ex:
                print("Periodicity of Payment 1")
                # gettinglogs("Exception in Periodicity of Payment 1 Exception")
                # print(ex)

            # try:
            #     el_periodicity_of_payment_l2_2 = driver.find_element_by_xpath(
            #         r'//*[@id="individualInquiryForm"]/div[3]/div[2]/div[2]/div/div/div[2]/button')
            #     el_periodicity_of_payment_l2_2.send_keys(row['periodicity_of_payment_2'])
            #     time.sleep(1)
            #     el_periodicity_of_payment_l2_2.click()
            #     gettinglogs("Filling Up Periodicity of Payment 2")
            # except Exception as ex:
            #     print("Periodicity of Payment 2")
                # gettinglogs("Exception in Periodicity of Payment 2 Exception")
                # print(ex)

        else:
            # have credit limits only
            # LAYER TWO::Installment Data :: credit limits
            try:
                el_credit_limit_l2 = driver.find_element_by_xpath(
                    r'//*[@id="individualInquiryForm"]/div[4]/div/div[2]/div/div/input')
                el_credit_limit_l2.clear()
                # el_credit_limit_l2.send_keys(row['credit_limit'])
                el_credit_limit_l2.send_keys(row['Credit_Limit'])
                gettinglogs("Filling Up Credit Limit")
            except Exception as ex:
                print("Credit Limit")
                gettinglogs("Exception in Credit Limit Exception")
                # print(ex)

    except Exception as ex:
        print("Type of Finance 1")
        # gettinglogs("Exception in Type of Financing 1")
        # print(ex)

    # try:
    # // *[ @ id = "individualInquiryForm"]/div[2]/div[2]/div/div/div/button
    #     el_type_of_financing_l1_2 = driver.find_element_by_xpath(
    #         r'//*[@id="individualInquiryForm"]/div[2]/div[2]/div/div/div[2]/button')
    #     el_type_of_financing_l1_2.send_keys(row['type_of_financing_2'])
    #     el_type_of_financing_l1_2.click()
    #     gettinglogs("Filling Up Type of Financing 2")
    # except Exception as ex:
    #     print("Type of Finance 2")
    #     # gettinglogs("Exception in Type of Financing 2")
    #     # print(ex)


    # LAYER THREE::Individual Subject Data
    # el_title_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[7]/div[1]/div/div/input')
    # el_title_l3.clear()
    # el_fathers_title_l3 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[8]/div[1]/div/div/input')
    # el_fathers_title_l3.clear()
    # el_mothers_title_l3 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[9]/div[1]/div/div/input')
    # el_mothers_title_l3.clear()
    # el_spouse_title_l3 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[10]/div[1]/div/div/input')
    # el_spouse_title_l3.clear()
    el_nid_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[11]/div[1]/div/div/input')
    el_nid_l3.clear()
    el_date_of_birth_l3 = driver.find_element_by_xpath(r'//*[@id="datetimepicker-ind"]/input')
    el_date_of_birth_l3.clear()
    el_district_of_birth_l3 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[13]/div[1]/div/div/input')
    el_district_of_birth_l3.clear()

    el_name_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[7]/div[2]/div/div/div/input')
    el_name_l3.clear()
    el_fathers_name_l3 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[8]/div[2]/div/div/div/input')
    el_fathers_name_l3.clear()
    el_mothers_name_l3 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[9]/div[2]/div/div/div/input')
    el_mothers_name_l3.clear()
    # el_spouse_name_l3 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[10]/div[2]/div/div/div/input')
    # el_spouse_name_l3.clear()
    # el_tin_l3 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[11]/div[2]/div/div/input')
    # el_tin_l3.clear()
    el_male_l3 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[12]/div[2]/div/div/label[1]/input[@name="gender" and @type="radio" and @value="M"]')
    el_female_l3 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[12]/div[2]/div/div/label[2]/input[@name="gender" and @type="radio" and @value="F"]')
    el_country_of_birth_l3_1 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[13]/div[2]/div/div/div/button')

    # el_country_of_birth_l3_2 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[13]/div[2]/div/div/div[2]/button')

    # LAYER FOUR::Permanent address data
    el_district_l4 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[15]/div[1]/div/div/input')
    el_district_l4.clear()
    el_postal_code_l4 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[16]/div[1]/div/div/input')
    el_postal_code_l4.clear()
    el_street_name_and_number_l4 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[15]/div[2]/div/div/input')
    el_street_name_and_number_l4.clear()
    el_country_l4_1 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[16]/div[2]/div/div/div/button')
    # el_country_l4_2 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[16]/div[2]/div/div/div[2]/button')

    # LAYER FIVE::Present address data
    # el_district_l5 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[18]/div[1]/div/div/input')
    # el_district_l5.clear()
    # el_postal_code_l5 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[19]/div[1]/div/div/input')
    # el_postal_code_l5.clear()
    # el_street_name_and_number_l5 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[18]/div[2]/div/div/input')
    # el_street_name_and_number_l5.clear()
    # el_country_l5 = driver.find_element_by_xpath(r'//*[@id="add_addr_country_of_birth"]')

    # LAYER SIX::Identification document data
    # el_id_type_l6 = driver.find_element_by_xpath(r'//*[@id="individual_id_type"]')
    # # el_id_type_l6.clear()
    # el_id_issue_date_l6 = driver.find_element_by_xpath(r'//*[@id="id_issue_datetimepicker_ind"]/input')
    # el_id_issue_date_l6.clear()
    # el_id_number_l6 = driver.find_element_by_xpath(r'//*[@id="individualInquiryForm"]/div[21]/div[2]/div/div/input')
    # el_id_number_l6.clear()
    # el_id_issue_country_l6 = driver.find_element_by_xpath(r'//*[@id="id_issue_country"]')

    # LAYER SEVEN::Sector Data
    # el_sector_type_public_l7 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[1]/input[@type="radio" and @name="sector_type" and @value="1"]')
    el_sector_type_public_l7 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[1]/input')
    el_sector_type_private_l7 = driver.find_element_by_xpath(
        r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[2]/input')
    el_sector_code_l7 = driver.find_element_by_xpath(r'/html/body/div[2]/div[4]/div/div/div/div[2]/div/div[1]/form/div[24]/div[2]/div/div/select')
    # el_sector_code_l7.clear()

    # LAYER EIGHT::Telephonic Data
    # el_telephone_number_l8 = driver.find_element_by_xpath(
    #     r'//*[@id="individualInquiryForm"]/div[26]/div/div/div/div/input')
    # el_telephone_number_l8.clear()
    el_contract_history_12_l8 = driver.find_element_by_xpath('//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[1]')
        # r'//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[1]/input[@type="radio" and @name="contracthistory" and @value="12"]')
        # r'//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[1]/input[@type="radio" and @value="12"]')
        # r'//*[@id="individualInquiryForm"]/div[24]/div[1]/div/div/label[1]/input')
    el_contract_history_24_l8 = driver.find_element_by_xpath('//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[2]')
        # r'//*[@id="individualInquiryForm"]/div[27]/div/div/div/div/div/label[2]/input[@type="radio" and @value="24"]')

    el_new_person_inquiry = driver.find_element_by_xpath(
        r'/html/body/div[2]/div[4]/div/div/div/div[2]/div/div[1]/form/div[28]/div/div/div/button')


    # FILL UP FORM
    # el_title_l3.send_keys(row['title'])
    # gettinglogs("Filling up Title")
    # el_fathers_title_l3.send_keys(row['father_title'])
    # gettinglogs("Filling up Father's Title")
    # el_mothers_title_l3.send_keys(row['mother_title'])
    # gettinglogs("Filling up Mother's Title")
    # el_spouse_title_l3.send_keys(row['spouse_title'])
    # gettinglogs("Filling up Spouse Title")
    # print('BEFORE NID: ', str(row['nid']))
    # nid = str(int(row['nid']))
    nid = a_nid

    # while '.' in nid:
    #     nid = nid[:-1]
    #
    # while len(nid) < 13:
    #     nid = int(nid)
    #     nid = nid * 10 + random.randint(0, 9)
    #     nid = str(nid)

    # print('AFTER NID: ', nid)

    el_nid_l3.send_keys(nid)
    gettinglogs("Filling up NID")
    el_date_of_birth_l3.send_keys(format_date(format_dob(row['date_of_birth'])))
    gettinglogs("Filling up Date of Birth")
    el_district_of_birth_l3.send_keys(row['district_of_birthl1'])
    gettinglogs("Filling up Distric of Birth")
    el_name_l3.send_keys(row['full_name'])
    gettinglogs("Filling up Full Name")
    el_fathers_name_l3.send_keys(row['father_name'])
    gettinglogs("Filling up Father's Name")
    el_mothers_name_l3.send_keys(row['mother_name'])
    gettinglogs("Filling up Mother's Name")
    # el_spouse_name_l3.send_keys(row['spouse_name'])
    # gettinglogs("Filling up Spouse Name")

    # tin = str(row['tin'])
    # print('TIN: ', tin)
    # while '.' in tin:
    #     tin = tin[:-1]
    # el_tin_l3.send_keys(int(row['tin']))
    # gettinglogs("Filling up TIN")

    try:
        gender = row['gender']
        print('GENDER: ' + gender)

        if gender == 'Male':
            # el_male_l3.click()
            driver.execute_script("arguments[0].click();", el_male_l3)
            gettinglogs("Filling up Gender: Male")
            # print('Male')
        elif gender == 'Female':
            # el_female_l3.click()
            driver.execute_script("arguments[0].click();", el_female_l3)
            # print('Female')
            gettinglogs("Filling up Gender: Female")
    except Exception as ex:
        gettinglogs("Exception in Gender")
        print(ex)

    # el_country_of_birth_l3_1.send_keys(row['country_of_birthl2'].upper())
    el_country_of_birth_l3_1.click()
    driver.find_element_by_link_text(row['country_of_birthl2'].upper()).click()
    gettinglogs("Filling up Country of Birth 1")
    # el_country_of_birth_l3_1.click()
    # el_country_of_birth_l3_2.send_keys(row['country_of_birthl2'].upper())
    gettinglogs("Filling up Country of Birth 2")
    # el_country_of_birth_l3_2.click()

    el_district_l4.send_keys(row['districtl2'])
    gettinglogs("Filling up District")
    el_street_name_and_number_l4.send_keys(row['street_name_and_numberl2'])
    gettinglogs("Filling up Street Name and Number")
    el_postal_code_l4.send_keys(row['postal_code'])
    gettinglogs("Filling up Postal Code")
    # el_country_l4_1.send_keys(row['country_of_birthll3'].upper())
    el_country_l4_1.click()
    driver.find_element_by_link_text(row['country_of_birthl2'].upper()).click()
    gettinglogs("Filling up Country of Birth 3")
    # el_country_l4_1.click()
    # el_country_l4_2.send_keys(row['country_of_birthll3'].upper())
    # gettinglogs("Filling up Country of Birth 4")
    # el_country_l4_2.click()

    # el_district_l5.send_keys(row['districtl3'])
    # gettinglogs("Filling up District")
    # el_street_name_and_number_l5.send_keys(row['street_name_and_numberl3'])
    # gettinglogs("Filling up Street Name and Number")
    # el_postal_code_l5.send_keys(row['postal_code'])
    # gettinglogs("Filling up Postal Code")
    # el_country_l5.send_keys(row['country_of_birthl4'])
    # gettinglogs("Filling up Country of Birth")

    # el_country_l5.click()

    # el_id_type_l6.send_keys(row['id_type'].upper())
    # gettinglogs("Filling up ID Type")

    # el_id_type_l6.click()
    # el_id_number_l6.send_keys(int(row['id_number']))
    # gettinglogs("Filling up ID Number")
    # el_id_issue_date_l6.send_keys(format_date(row['date_of_issue']))
    # gettinglogs("Filling up Date of Issue")
    # el_id_issue_country_l6.send_keys(row['issue_country'])
    # gettinglogs("Filling up Issue Country")
    # # el_id_issue_country_l6.click()
    # el_sector_code_l7.click()

    sector_type = row['sector_type']

    if sector_type == 'public':
        driver.execute_script("arguments[0].click();", el_sector_type_public_l7)
        gettinglogs("Filling up Sector Type: Public")
    else:
        # el_sector_type_private_l7.click()
        driver.execute_script("arguments[0].click();", el_sector_type_private_l7)
        gettinglogs("Filling up Sector Type: Private")


    from selenium.webdriver.support.ui import Select
    driver.execute_script("arguments[0].click();", el_sector_code_l7)
    select = Select(driver.find_element_by_id('individual_sector_code'))
    select.select_by_visible_text(row['sector_code'])


    contract_history = int(row['contract_history'])

    if contract_history == 12:
        driver.execute_script("arguments[0].click();", el_contract_history_12_l8)
        gettinglogs("Filling up Contract History: 12")
    elif contract_history == 24:
        driver.execute_script("arguments[0].click();", el_contract_history_24_l8)

        gettinglogs("Filling up Contract History: 24")


    time.sleep(1)
    print('CIB FORM END')
    gettinglogs("Form Fill Completed for NID:"+str(row['nid']))
    # el_new_person_inquiry.click()
    driver.execute_script("arguments[0].click();", el_new_person_inquiry)
    time.sleep(25)
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a"))

    # from selenium import webdriver
    url = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a").get_attribute("href")
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--test-type")
    # options.binary_location = "docker/Downloads"
    image_url = url
    img_name = image_url.split('/')[-1]
    img_name = img_name[:-4]
    img_name = img_name[9:]
    # driver.get(url)
    # driver.save_screenshot("docker/Downloads{}.png".format(img_name))

    from pathlib import Path
    import requests
    filename = Path("docker/Downloads{}.pdf".format(img_name))
    url = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/a").get_attribute("href")
    response = requests.get(url)
    filename.write_bytes(response.content)


    driver.get("https://cib.bb.org.bd/new_inquiry")







