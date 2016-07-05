# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta
from os import environ


def check_balance(residentnumber, bankid, password, accountnumber):
    url = 'https://obank.kbstar.com/quics?asfilecode=524517&_FILE_NAME=KB_거래내역빠른조회.html&USER_TYPE=02&주민사업자번호=000000{residentnumber}&고객식별번호={bankid}&조회구분=2&_LANG_TYPE=KOR&비밀번호={password}&조회시작일={startday}&응답방법=2&다음거래일련번호키=&조회종료일={endday}&다음거래년월일키=&계좌번호={accountnumber}'.format(
        residentnumber= residentnumber, #주민번호 뒷자리
        bankid= bankid.upper(), #인터넷 뱅킹 ID
        password= password, #계좌 비밀번호
        startday= (date.today()-timedelta(1)).strftime("%Y%m%d"), #조회시작일/어제
        endday= date.today().strftime("%Y%m%d"), #조회마감일/오늘
        accountnumber= accountnumber #계좌번호
    )

    res = requests.get(url)

    if res == '':
        raise Exception('반환받은 결과가 없음')

    html = res.text
    #print(html)
    soup = bs(html, 'html.parser')

    infos = soup.select('tr[align:center] > td')

    item_quantitys = int(len(infos)) / 9

    item_seq = 0
    transactions = []
    while item_seq < item_quantitys:
        transaction = []
        seq = infos[item_seq*9:item_seq*9+8]
        for i in seq:
            transaction.append(i.text.strip())
        transactions.append(transaction)
        item_seq += 1
    return transactions


if __name__=='__main__':
    results = check_balance(
        residentnumber= environ['RESIDENTNUMBER'],
        bankid= environ['BANKID'],
        password= environ['BANKPW'],
        accountnumber= environ['ACCOUNTNUMBER']
    )
    for info in results:
        transact_time = info[0].strip()
        transact_by = info[2].strip()
        if info[4] != '0':
            transact_amount = "-" + info[4].strip()
        else:
            transact_amount = "+" + info[5].strip()
        print("거래시기: {}\n​거래처: {}\n거래금액: {}\n---------------".format(
            transact_time, transact_by, transact_amount
         ))