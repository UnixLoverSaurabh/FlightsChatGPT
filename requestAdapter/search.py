import json
import re
from common.httpClient import NewClientRequest
import uuid
import time
from datetime import datetime
from common.utils import constants

headers = {
    "Accept": "application/json",
    "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "https://www.makemytrip.com",
    "Pragma": "no-cache",
    "Referer": "https://www.makemytrip.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
    "ab": json.dumps({"INSGHT":0,"STP":0,"SimpF":0,"BFFL":0,"MMTFF":0,"BSG":0,"LFT":0,"MFEP":0,"DGF":0,"BCG":1,"flightInfoOptionSequenceKey":"FNO","IFFLK":1,"DGT":3,"IFFLKOWRT":0,"SED":0,"RTSC":0,"ZCA":0,"ZCD":1,"SEM":0,"ZCE":1,"NLA":0,"FLK":1,"dgi":0,"IRR":0,"RTM":0,"ZCS":1,"HPR":0,"FLS":1,"RTS":0,"FFBEN":0,"SFN":0,"QBK":0,"myPUAE":False,"meff":1,"QCO":4,"TP":0,"PRB":0,"PRE":2,"PRG":0,"mbrta":0,"IFFLKMC":0,"pwa_login_type":0,"NDAST":0,"ITT":1,"PRO":0,"FLKT":0,"PBC":0,"mstp":0,"SHR":0,"CYT":0,"CID":1,"bottomsheet_onetap_pwa":"1","mras":1,"mbrt":0,"FFPers":0,"mctw":0,"INSBTM":0,"UMF":0,"HCP":0,"SIM":0,"PTA":0,"INSV3":0,"PTF":0,"AFI":0,"mctwb":1,"IFSort":0,"mrtp":0,"LLS":0,"PDF":0,"MFMD":1,"BIRT":0,"IFS":0,"flightPageLoadTracking":0,"GSF":0,"msfn":0,"QFT":1,"MOB":0,"INSTP":0,"BII":0,"ADDONM":0,"FAA":0,"IFFLKOW":0,"TMI":0,"FAO":0,"marc":0,"FAT":0,"PET":0,"WCM":0,"REUSABLE":0,"PCRDF":0,"PFA":1,"OTP":0,"mnthn":False,"CLS":1,"PFI":1,"ZC_Server_Side_experiment1":1,"CHMRK":0,"FSA":3,"PFL":0,"PWA":1,"PFP":1,"DDDF":0,"mema":0,"NSF":0,"mbfc":0,"LISTN":1,"FCN":False,"CABS":1,"myPartner_b2b_homepage":False,"CABF":1,"mqc":0,"mics":0,"travellerScan":0,"NTD":0,"wsmn":0,"SNH":0,"LPS":0,"MRT":0,"ffmove":0,"ZCDS":0,"IFMC":0,"IFFLKRT":0,"BNPL":1,"mal":1,"MICROSOFTFES":0,"mgsf":0,"ZC_Client_Side_exp":False,"NUG":0,"ALTFLT":0,"FUS":1,"CURDT":0,"COU":0,"USF":0,"MCC":1,"PIF":0,"CYTN":0,"ALTFLTCORP":0,"BAGR":1,"CPA":0,"SOR":0,"msa":1,"ALF":0,"MCS":1,"REUSABLERT":0,"msf":1,"testAB":0,"SPA":0,"CPS":0,"cnpn":1,"dd_exp_myp":"peshkash","RNP":4,"AMD":0,"AME":0,"IMB":0,"BNTD":1,"WNTI":0,"TSC":0,"trvlr":True,"CAD":1,"GI_PLK":0,"bntdp":0,"IMS":0,"mbfsme":0,"mbit":0,"mdl":1,"DTD":0,"ANC":0,"IFPLK":1,"HLD":0,"ANP":1,"ALTF":0,"cheaperFlightsDesktopDom":1,"ANU":0,"MFA":0,"INP":0,"MFD":0,"MFC":1,"CFAR":1,"mecj":1,"INT":1,"PLK":1,"INS":0,"MFEA":0,"MFI":0,"AOA":0,"SRT":1,"AOD":0,"PLS":1,"MFP":0,"NHP":0,"MFEI":0,"AOI":0,"MFED":0,"mntf":0,"AOP":0,"BAA":0,"AGGRNEW":0,"MYPRTA":0,"CFBR":0,"MFTD":0,"BAN":0,"CANCT":0,"INSNEW":0,"GYOLO":0,"APD":0,"dd_exp_name":"pluto","EMI":0,"IPS":0,"BRB":0}),
    "app-ver": "8.0.0",
    "currency": "inr",
    "device-id": "11765c19-a9a7-436d-bfed-cad4404372f7",
    "domain": "in",
    "language": "eng",
    "lob": "B2C",
    "mcid": "11765c19-a9a7-436d-bfed-cad4404372f7",
    "mmt-auth": "MAT1c1384a6644ad51bc2e22c121fa260659267b444c4d04041ababcdb64bcd2c245b96b7e7dde8e188f690c264ccd76860dP",
    "os": "Android",
    "pfm": "PWA",
    "region": "in",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "Android",
    "source": "null",
    "src": "mmt",
    "x-user-cc": "IN",
    "x-user-ip": "2406:7400:56:8ea6:6de6:9e0a:fff1:bdc1",
    "x-user-rc": "BANGALORE",
}


def getMMTSearchResponse(parameter: dict):
    dep_date = parameter.get(constants.DEPARTURE_DATE)
    dep_date_formatted = datetime.strptime(dep_date, '%d-%m-%Y').strftime("%Y%m%d")
    url = f'https://flights-cb.makemytrip.com/api/search?pfm=PWA&lob=B2C&crId={uuid.uuid4()}&cur=INR&lcl=en&shd=true&cc=E&pax=A-1_C-0_I-0&it={parameter.get(constants.SOURCE)}-{parameter.get(constants.DESTINATION)}-{dep_date_formatted}&forwardFlowRequired=true&apiTimeStamp={int(time.time() * 1000)}&region=in&currency=inr&language=eng&cmpId='

    response = NewClientRequest(url, headers, "", "GET").get_response()

    no_of_flights = 0
    flightsCard = {constants.COLUMN_AIRLINE: [], constants.COLUMN_DEP_TIME: [], constants.COLUMN_ARRIVAL_TIME: [], constants.COLUMN_TOTAL_FARE: []}
    if response.status_code == 200:
        resp = json.loads(response.content.decode('utf8'))
        for cardList in resp['cardList'][0]:
            no_of_flights += 1
            if no_of_flights == 50:
                break
            flightsCard[constants.COLUMN_AIRLINE].append(re.sub(r'<[^<]+?>', '', cardList['airlineHeading']))
            flightsCard[constants.COLUMN_TOTAL_FARE].append(cardList['fare'])

            dep_time = ""
            arrival_time = ""
            for journeyKey in cardList['journeyKeys']:
                if dep_time == "":
                    dep_time = resp['journeyMap'][journeyKey]['depTime']
                arrival_time = resp['journeyMap'][journeyKey]['arrTime']
            flightsCard[constants.COLUMN_DEP_TIME].append(dep_time)
            flightsCard[constants.COLUMN_ARRIVAL_TIME].append(arrival_time)
    else:
        print(f'url: {url}, status_code: {response.status_code}, content: {response.content}')
    return json.dumps(flightsCard), no_of_flights

# getMMTSearchResponse({constants.SOURCE: "DEL", constants.DESTINATION: "DXB", constants.DEPARTURE_DATE: "25-01-2023"})