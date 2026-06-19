import requests

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "cookie": "UBT_VID=1767756775502.9a63IvuYRcpY; GUID=09031128217407423959; MKT_CKID=1767756775815.nlr2p.cr92; _RGUID=28f6e07b-db7b-475b-89b7-90b4852ab1fc; ibulocale=zh_cn; cookiePricesDisplayed=CNY; _abtest_userid=7ce9399d-d29f-4412-96ee-d77bd5e0bc57; Session=smartlinkcode=U130727&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; appFloatCnt=1; StartCity_Pkg=PkgStartCity=1094; ibulanguage=CN; Hm_lvt_a8d6737197d542432f4ff4abc6e06384=1767756776,1769045097; Hm_lpvt_a8d6737197d542432f4ff4abc6e06384=1769045097; HMACCOUNT=92BD66EA4027F296; Union=OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1769045098&Expires=1769649898391; MKT_OrderClick=ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1769045098397&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3D84b848780d7f16bc071321097131108e%26keywordid%3D82327006001866&VAL={\"pc_vid\":\"1767756775502.9a63IvuYRcpY\"}; _ga=GA1.1.1517630657.1767756776; MKT_Pagesource=PC; _ga_9BZF483VNQ=GS2.1.s1769045098$o2$g0$t1769046460$j60$l0$h0; _ga_5DVRDQD429=GS2.1.s1769045098$o2$g0$t1769046460$j60$l0$h1631207566; _ga_B77BES1Z8Z=GS2.1.s1769045099$o2$g0$t1769046460$j60$l0$h0; nfes_isSupportWebP=1; cticket=0B5E3A04C1A4941BA2FAFB12E428738B5286351DBD509AF8D67E1D4BB6A10F77; login_type=0; login_uid=BD02293A5B23F3C0C1266D23A8EDA98A; DUID=u=5AA623EBA217154D4FE9F0A01BD01DA1&v=0; IsNonUser=F; AHeadUserInfo=VipGrade=5&VipGradeName=%B0%D7%D2%F8%B9%F3%B1%F6&UserName=&NoReadMessageCount=0; _udl=708D70C2B179E2F91CC5ED1C2CCE362D; _jzqco=%7C%7C%7C%7C1769045099474%7C1.1299349819.1767756775818.1769076134314.1769076238465.1769076134314.1769076238465.undefined.0.0.17.17; _bfa=1.1767756775502.9a63IvuYRcpY.1.1769076237704.1769076276087.3.12.0",
    "referer": "https://you.ctrip.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "x-ctx-currency": "CNY",
    "x-ctx-locale": "zh-CN",
    "x-ctx-ubt-pvid": "12",
    "x-ctx-ubt-sid": "3",
    "x-ctx-ubt-vid": "1767756775502.9a63IvuYRcpY"
}
url = "https://m.ctrip.com/restapi/soa2/22670/getRecommendTravel?_fxpcqlniredt=09031128217407423959&x-traceID=09031128217407423959-1769075463358-2716609"
# 1.发送请求
response = requests.post(url=url,headers=headers)
print(response)
print('*'*30)
print(response.text)
print('*'*30)
travelInfoList = response.json()['travelInfoList']
print(travelInfoList)