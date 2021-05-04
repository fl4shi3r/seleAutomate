from selenium import webdriver
import pyscreenshot as ImageGrab
import re
import os
import time
import sys
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyscreenshot as ImageGrab
import pytesseract


def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 50:
        time.sleep(0.5)
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
            else:
                dl_wait = False
        seconds += 1
#     return seconds


timers = [0.5]
driver = webdriver.Chrome('./driver/chromedriver')
driver.get("---snipped---")

done = []

states = ['--snipped--']
districts = ['--snipped--']

for state in states:
    path = './new-data/' + ''.join(e for e in state if e.isalnum())
    # path = './'
    if os.path.isdir(path) == False:
        os.mkdir(path)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.NAME, 'ctl00$ContentPlaceHolder1$ddlState'))
    )
    html = element.get_attribute("innerHTML")
    # print(html)
    reg_str = '>(.*?)<'
    all_states = re.findall(reg_str, html)
    index_state = 0
    for state_index in range(len(all_states)):
        if state == all_states[state_index]:
            index_state = state_index + 1
    # print(len(all_states))

    xPath = '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/select/option[' + str(
        index_state) + ']'
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xPath))
    )
    # time.sleep(0.5)
    element.click()
# ------------------------------------------------------------------------------------------------------------------------------
# code for district
# ------------------------------------------------------------------------------------------------------------------------------
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.NAME, 'ctl00$ContentPlaceHolder1$ddlDistrict'))
    )
    html = element.get_attribute("innerHTML")
    # print(html)
    reg_str = '>(.*?)<'
    all_district = re.findall(reg_str, html)

    t_path_1 = path
    for district in districts:
        fileObj = open('done-district_1.txt', 'r')
        done_district = []
        for line in fileObj.readlines():
            done_district.append(line.strip())
        fileObj.close()
        if ''.join(e for e in district if e.isalnum()) in done_district:
            continue
        # new done district
        path = t_path_1
        path = path + '/' + ''.join(e for e in district if e.isalnum())
        if os.path.isdir(path) == False:
            os.mkdir(path)
        # print(all_district)
        if district in all_district:
            index_district = 0
            for district_index in range(len(all_district)):
                if district == all_district[district_index]:
                    index_district = district_index + 1
            # time.sleep(2)
            #        /html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/select/option[2]
            xPath = '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[2]/select/option[' + str(
                index_district) + ']'
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xPath))
            )
            # time.sleep(random.choice(timers))
            element.click()

# ------------------------------------------------------------------------------------------------------------------------------
# code for Block
# ------------------------------------------------------------------------------------------------------------------------------
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.NAME, 'ctl00$ContentPlaceHolder1$ddlBlock'))
            )
            html = element.get_attribute("innerHTML")
            reg_str = '>(.*?)<'
            all_blocks = re.findall(reg_str, html)
            # print(all_blocks)
            index_block = 1
            t_path_2 = path
            for block_index in range(len(all_blocks)):
                fileObj = open('done-block.txt', 'r')
                done_block = []
                for line in fileObj.readlines():
                    done_block.append(line.strip())
                fileObj.close()
                # print(done_block)
                # print('test1')
                if index_block >= len(all_blocks):
                    continue
                index_block = index_block + 1
                if ''.join(e for e in all_blocks[index_block-1] if e.isalnum()) in done_block:
                    continue
                path = t_path_2

                path = path + '/' + \
                    ''.join(
                        e for e in all_blocks[index_block-1] if e.isalnum())
                if os.path.isdir(path) == False:
                    os.mkdir(path)
                # index_block = index_block + 1
                #         /html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/select/option[2]
                xPath = '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[3]/select/option[' + str(
                    index_block) + ']'
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, xPath))
                )
                # time.sleep(random.choice(timers))
                element.click()
# ------------------------------------------------------------------------------------------------------------------------------
# code for each p
# ------------------------------------------------------------------------------------------------------------------------------
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.NAME, 'ctl00$ContentPlaceHolder1$ddlPanchayat'))
                )
                html = element.get_attribute("innerHTML")
                reg_str = '>(.*?)<'
                all_panchayat = re.findall(reg_str, html)
                index_panchayat = 1
                t_path_3 = path
                for district_index in range(len(all_panchayat)):

                    if (index_panchayat >= len(all_panchayat)):
                        continue
                        continue

                    path = t_path_3
                    path = path + '/' + \
                        ''.join(
                            e for e in all_panchayat[index_panchayat] if e.isalnum())
                    if os.path.isdir(path) == False:
                        os.mkdir(path)
                    index_panchayat = index_panchayat + 1
                    xPath = '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[4]/select/option[' + str(
                        index_panchayat) + ']'
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xPath))
                    )
                    element.click()
# ------------------------------------------------------------------------------------------------------------------------------
# code for each years
# ------------------------------------------------------------------------------------------------------------------------------
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.NAME, 'ctl00$ContentPlaceHolder1$ddlFinYear'))
                    )
                    html = element.get_attribute("innerHTML")
                    reg_str = '>(.*?)<'
                    all_year = re.findall(reg_str, html)
                    index_year = 7
                    t_path_4 = path
                    for i in range(len(all_year)-7):
                        fileObj = open('done-panchayat-year.txt', 'r')
                        done_panc_year = []
                        for line in fileObj.readlines():
                            done_panc_year.append(line.strip())
                        fileObj.close()
                        path = t_path_4
                        path = path + '/' + \
                            ''.join(
                                e for e in all_year[index_year] if e.isalnum())
                        if os.path.isdir(path) == False:
                            os.mkdir(path)

                        if (index_year >= len(all_year)):
                            continue
                        index_year = index_year + 1
                        name = ''.join(e for e in all_panchayat[index_panchayat-1] if e.isalnum(
                        )) + '-' + ''.join(e for e in all_year[index_year-1] if e.isalnum())
                        if (name in done_panc_year):
                            continue

                        flag = 0
                        for j in range(3):
                            if flag == 1:
                                break
                            else:

                                try:
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[6]/select/option[' + str(index_year) + ']'))
                                    )
                                    element.click()

                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[7]/select/option[2]'))
                                    )
                                    element.click()

                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.NAME, 'ctl00$ContentPlaceHolder1$txtCaptcha'))
                                    )
                                    im = ImageGrab.grab(
                                        bbox=(420, 760, 520, 790))  # X1,Y1,X2,Y2
                                    import uuid
                                    filename = str(uuid.uuid4()) + '.png'
                                    im.save(filename)

                                    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
                                    string = pytesseract.image_to_string(
                                        filename)
                                    all_num = string.strip()
                                    print(all_num)
                                    if '+' in all_num:
                                        num_1 = int(
                                            (all_num.split('+')[0]).strip())
                                        num_2 = int(
                                            (all_num.split('+')[1]).strip())
                                        result = num_1 + num_2
                                        element.send_keys(result)
                                    elif '-' in all_num:
                                        num_1 = int(
                                            (all_num.split('-')[0]).strip())
                                        num_2 = int(
                                            (all_num.split('-')[1]).strip())
                                        result = num_1 - num_2
                                        element.send_keys(result)
                                    else:
                                        cmd = "notify-send 'Different operand' 'Fill Manually'"
                                        print(
                                            "Error in this panchayat : " + path)
                                        os.system(cmd)
                                        time.sleep(10)

                                    if os.path.isfile(filename):
                                        cmd_1 = 'rm *.png'
                                        os.system(cmd_1)
                                    xPath = '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[9]/input'
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, xPath))
                                    )
                                    element.click()

                                    html_source_code = driver.execute_script(
                                        "return document.body.innerHTML;")
                                    if 'Data Not Found' in html_source_code:
                                        cmd = 'touch ' + path+'/data-not-available.txt'
                                        name = ''.join(e for e in all_panchayat[index_panchayat-1] if e.isalnum(
                                        )) + '-' + ''.join(e for e in all_year[index_year-1] if e.isalnum())
                                        cmd_2 = 'echo ' + name + ' >> done-panchayat-year.txt '
                                        os.system(cmd)
                                        os.system(cmd_2)
                                        flag = 1
                                        continue
                                    else:

                                        element = WebDriverWait(driver, 5).until(
                                            EC.presence_of_element_located(
                                                (By.ID, 'ContentPlaceHolder1_btnExportPdf'))
                                        )

                                        element.click()
                                        download_wait('/root/Downloads/')
                                        arr = os.listdir('/root/Downloads/')[0]
                                        cmd = 'mv /root/Downloads/' + arr + ' ' + path + '/'
                                        os.system(cmd)
                                        cmd_2 = 'echo "Done: ' + path + '" >> new-done.txt'
                                        os.system(cmd_2)

                                        fileObj = open(
                                            'done-panchayat-year.txt', 'r')
                                        panch = []
                                        for line in fileObj.readlines():
                                            panch.append(line.strip())
                                        name = ''.join(e for e in all_panchayat[index_panchayat-1] if e.isalnum(
                                        )) + '-' + ''.join(e for e in all_year[index_year-1] if e.isalnum())
                                        panch.append(name)
                                        fileObj.close()
                                        fileObj = open(
                                            'done-panchayat-year.txt', 'w+')
                                        for pan in panch:
                                            fileObj.write(pan+'\n')
                                        fileObj.close()
                                        flag = 1
                                except:
                                    print("Retrying")
                                    element = WebDriverWait(driver, 10).until(
                                        EC.presence_of_element_located(
                                            (By.XPATH, '/html/body/form/div[3]/div[3]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/div[6]/select/option[' + str(index_year-1) + ']'))
                                    )
                                    element.click()

                        if flag == 0:
                            cmd = 'echo "Error in: ' + path + '" >> new-error.txt'
                            os.system(cmd)
                            print("Error in this panchayat : " + path)

                        arr = os.listdir('/root/Downloads/')
                        if len(arr) > 0:
                            cmd = 'rm /root/Downloads/*'
                            os.system(cmd)
                block_name = ''.join(
                    e for e in all_blocks[index_block-1] if e.isalnum())
                cmd = 'echo ' + block_name + ' >> done-block.txt'
                os.system(cmd)
        cmd = 'echo ' + \
            ''.join(e for e in district if e.isalnum()) + \
            ' >> done-district.txt'
        os.system(cmd)
