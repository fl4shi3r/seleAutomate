from selenium import webdriver
import textract
import csv
import unicodedata
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
from bs4 import BeautifulSoup
from fpdf import FPDF

codes = {'PB': '28', 'JH': '16', 'UP': '34', 'BH': '6', 'RJ': '29'}


def unicode_normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')


def convert_csv_to_pdf(input_data, outputfileName, panchayat):
    reader = input_data

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times', 'B', 14.0)
    pdf.cell(page_width, 0.0,
             '--Snipped--- : [ ' + panchayat + ' ]', align='C')
    pdf.ln(10)

    pdf.set_font('Arial', '', 11)

    pdf.ln(1)

    for row in reader:
        pdf.set_font('Arial', '', 11)
        pdf.cell(w=30, h=5, txt=unicode_normalize(row[0]), border=1, align='C')
        pdf.cell(w=70, h=5, txt=unicode_normalize(row[1]), border=1, align='C')
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=50, h=5, txt=unicode_normalize(row[2]), border=1, align='C')
        pdf.cell(w=25,  h=5, txt=unicode_normalize(
            row[3]), border=1, align='C')
        pdf.cell(w=45,  h=5, txt=unicode_normalize(
            row[4]), border=1, align='C')
        pdf.cell(w=20,  h=5, txt=unicode_normalize(
            row[5]), border=1, align='C')
        pdf.ln(5)
    pdf.ln(10)

    pdf.set_font('Times', '', 10.0)
    pdf.cell(page_width, 0.0, '- end of report -', align='C')

    pdf.output(outputfileName, 'F')


url = '-----Confidential-----'
driver = webdriver.Chrome('/home/driver/chromedriver')
driver.get(url)
path = ''

temp_2 = path
for block in os.listdir('./'):
    path = temp_2
    if os.path.isdir(block):
        path = path + block + '/'
        temp_4 = path
        for panchayat in os.listdir(path):
            if not os.path.exists('done_panchayat.txt'):
                cmd = 'touch done_panchayat.txt'
                os.system(cmd)
            fileObj = open('done_panchayat.txt', 'r')
            done_district = []
            for line in fileObj.readlines():
                done_district.append(line.strip())
            fileObj.close()
            if panchayat in done_district:
                continue
            path = temp_4
            path = path + panchayat

            for fname in os.listdir(path):
                if fname.endswith('.pdf') and len(fname) > 50:
                    print(fname)
                    try:  # -----------------------
                        filePath = path+'/'+fname
                        text = textract.process(filePath).decode("utf-8")
                        regx = '[A-Za-z]{2}[0-9]{7,12}'
                        all_reg_no = re.findall(regx, text)

                        current_panchayat_data = []
                        current_panchayat_data.append(
                            ['Registration No', 'AHL_TIN', 'Name', 'DOB', 'Relation', 'Status'])

                        for reg_no in all_reg_no:
                            if len(reg_no) > 9:
                                current_panchayat_data.append(
                                    [reg_no, 'NA', 'NA', 'NA', 'NA', 'NA'])
                                continue

                            state_code = codes[reg_no[:2]]
                            xpath = '/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/select/option[' + state_code + ']'
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, xpath))
                            )
                            element.click()

                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.NAME, 'ctl00$ContentPlaceHolder1$txtPMAYID'))
                            )
                            element.send_keys(Keys.CONTROL + "a")
                            element.send_keys(Keys.DELETE)
                            new_reg_no = reg_no[-7:]
                            time.sleep(0.2)
                            element.send_keys(new_reg_no)

                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located(
                                    (By.NAME, 'ctl00$ContentPlaceHolder1$btnSubmit'))
                            )
                            element.click()
                            if 'Object reference not set to an instance of an object' in driver.page_source:
                                current_panchayat_data.append(
                                    [reg_no, 'NA', 'NA', 'NA', 'NA', 'NA'])
                                element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/a'))
                                )
                                element.click()
                                continue
                            if 'The remote server returned an error: (502) Bad Gateway' in driver.page_source:
                                current_panchayat_data.append(
                                    [reg_no, 'NA', 'NA', 'NA', 'NA', 'NA'])
                                element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/a'))
                                )
                                element.click()
                                continue
                            if 'Something Went Wrong' in driver.page_source:
                                current_panchayat_data.append(
                                    [reg_no, 'NA', 'NA', 'NA', 'NA', 'NA'])
                                element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.XPATH, '/html/body/form/div[3]/div[3]/div/div/div[2]/div[1]/div/div/div/div[2]/div[1]/a'))
                                )
                                element.click()
                                continue

                            html_text = driver.page_source
                            soup = BeautifulSoup(html_text, "lxml")
                            table = soup.find(
                                'table', id='ctl00_ContentPlaceHolder1_gdvfamilydetails')
                            table_body = table.find('tbody')
                            rows = table_body.find_all('tr')
                            for i in range(1, len(rows)):
                                data_to_add = []
                                data_to_add.append(reg_no)

                                cols = rows[i].find_all('td')
                                cols = [ele.text.strip() for ele in cols]
                                data_to_add.append(cols[0])
                                data_to_add.append(cols[1])
                                data_to_add.append(cols[4])
                                data_to_add.append(cols[5])
                                data_to_add.append('status [    ]')
                                current_panchayat_data.append(data_to_add)
                                if i == len(rows) - 1:
                                    current_panchayat_data.append(
                                        ['-'*12, '-'*53, '-'*45, '-'*20, '-'*38, '-'*17])

                        outputfileName = path + '/' + panchayat + '.pdf'
                        convert_csv_to_pdf(
                            current_panchayat_data, outputfileName, 'panchayat')
                        cmd = 'echo "' + panchayat + '" >> done_panchayat.txt'
                        os.system(cmd)
                    except:
                        cmd = 'echo "' + panchayat + '" >> error_panchayat.txt'
                        os.system(cmd)


dis_name = os.path.abspath(os.path.join('.', os.pardir))
cmd = 'notify-send DONE "' + dis_name + '"'
cmd = 'echo ' + dis_name + ' >> /home/final_done_district.txt'
