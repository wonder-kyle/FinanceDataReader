# coding: utf-8

import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
from pandas.tseries.offsets import BDay

class PriceCrossSection:
    def __init__(self, date=None):
        if date == None:
             self.date = datetime.today() - 0*BDay()
        else:  self.date = pd.to_datetime(date) - 0*BDay()
        
    def read(self):
        # STEP 01: Generate OTP
        gen_otp_url = 'http://marketdata.krx.co.kr/contents/COM/GenerateOTP.jspx'
        gen_otp_data = {
            'name':'fileDown',
            'filetype':'xls',
            'url':'MKD/04/0404/04040200/mkd04040200_01',
            'market_gubun':'ALL',
            'indx_ind_cd':'',
            'sect_tp_cd':'',
            'schdate': self.date.strftime('%Y%m%d'),
            'pagePath':'/contents/MKD/04/0404/04040200/MKD04040200.jsp',
        }    
        r = requests.get(gen_otp_url, gen_otp_data)
        code = r.content
    
        # STEP 02: download
        down_url = 'http://file.krx.co.kr/download.jspx'
        down_data = {
            'code': code,
        }    
        r = requests.get(down_url, down_data)
        df = pd.read_excel(BytesIO(r.content), header=0, thousands=',')
        
        return df

# retrieved from https://woosa7.github.io/krx_stock_master/