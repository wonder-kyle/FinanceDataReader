# coding: utf-8
from FinanceDataReader.data import (PriceReader, SheetReader, StockListing, PriceCrossSectionReader)
from FinanceDataReader.sheet.data import (FinanceSheetCrawler)
class strategy:
    def __init__(self):
        self.time = None
        self.strategy = None #function
    
    def get_score(self):
        msg = "which basket would be tested for?"
        raise NotImplementedError(msg)
    
    def fit(self,strategy):
        self.strategy = strategy
        
    def screening(self, basket):
        print('you used without overriding')
        
        price_df=PriceCrossSectionReader().set_index('Symbol').reindex(basket)
        
        for symbol in basket:
            temp_object=FinanceSheetCrawler(symbol=symbol,sheet_typ=-1,freq_typ='Q')
            temp_sheet=pd.DataFrame()
            for i in range(3):
                temp_object.set_sheet_typ(i)
                temp_subsheet=temp_object.read()
                if i==1:
                    averaged=temp_subsheet.iloc[:,2:-1].dropna(how='all').fillna(0)
                    averaged=averaged.mean(axis=1,skipna=False)
                else:
                    averaged=temp_subsheet.iloc[:,2:-1].sum(axis=1,skipna=True, min_count=1)
                averaged.name('avg_yr')
                temp_subsheet=temp_subsheet.iloc[:,:1].join(averaged)
                temp_sheet=pd.concat([temp_sheet,temp_subsheet],axis=0)
            
        return temp_sheet
    
    def backtesting(self, basket, date): #구현 예정
        msg = "which basket would be tested for?"
        raise NotImplementedError(msg)