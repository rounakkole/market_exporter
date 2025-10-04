class export_class:

    entity = ""
    period = "3mo"
    interval = "1d"
    suffix = ""
    
    def __init__(self, _entity):
        self.entity = _entity

    def interface(self):
        from functions import show_additional
        from functions import country_code
        from functions import multi

        entity = self.entity.upper()
        if (entity == "S" or entity == "SETTINGS"):
            self.entity = input("entity name: ")
            self.suffix = country_code()
            self.interval = str(input("interval 1d,5d,1mo: "))
            self.period = str(input("period 3mo,1y,5y: "))
            if(self.period == ""):
                self.period = set_period(self.interval)
            #show_additional(entity)
            self.interface()

        elif (entity == "M" or entity == "MULTI"):
            entity_list = {}
            entity_list = multi()
            for entity_n in entity_list:
                self.entity = entity_n
                self.analyser()

        else:
            self.analyser()


    def analyser(self):
        from yfinance import download as yf_download 
        from functions import console_chart_v2
        itr_fail = 0

        openValue = highValue = lowValue = closeValue = 1
        date = ""
        value0_desc = {}
        
        entity = self.entity + self.suffix
        data = yf_download(tickers=entity,
                           period=self.period,
                           interval=self.interval, auto_adjust=False, progress=False)


        data_len = len(data) - 1
        i = data_len + 1
        while (i > 0 and itr_fail < 7):
            i = i - 1

            try:
            #if (True):
                if (isinstance((data['Open'].iloc[i].item()), float)):
                    openValue = (data['Open'].iloc[i].item())
                    highValue = (data['High'].iloc[i].item())
                    lowValue = (data['Low'].iloc[i].item())
                    closeValue = (data['Close'].iloc[i].item())
                    
                    if ((data_len - i) < (60)):

                        date = data.index[i]
                        #print(data)
                        print(entity, end=",")
                        print(round(closeValue, 2), end=",")
                        print(self.interval, end=",")
                        print(date.strftime('%d-%m-%Y'), end="\n") #Windows
                        #print(date.strftime('%m-%d-%Y'), end="\n") #Linux
                        
                        if ((data_len - i) < (5)):
                            value0_desc[4 - (data_len - i)] = openValue, highValue, lowValue, closeValue
                    else:
                        #print(openValue, highValue, lowValue, closeValue).
                        break

                else:
                    print("error for iteration: ", i, end="        \n")
                    itr_fail = itr_fail + 1

            except Exception as e:
            #else:
                print(entity, i, end="   ")
                print(e)
                itr_fail = itr_fail + 1
                
                
        console_chart_v2(value0_desc)
