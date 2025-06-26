import requests

url = "https://www.trt10.jus.br/certidao_online/jsf/publico/certidaoOnline.jsf"

headers = {
    "Accept": "application/xml, text/xml, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt;q=0.7",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Faces-Request": "partial/ajax",
    "Origin": "https://www.trt10.jus.br",
    "Referer": "https://www.trt10.jus.br/certidao_online/jsf/publico/certidaoOnline.jsf?idTRT10M=77",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "JSESSIONID=6MAp5AjltDpBAQwMqSPMAOgm.prd; PHPSESSID=psm55ts0ol5u8f4meiq8g1338f"
}

payload = {
    "javax.faces.partial.ajax": "true",
    "javax.faces.source": "tvPrincipal:frmEmitirCertidaoOnline:btnConsultar",
    "javax.faces.partial.execute": "@all",
    "javax.faces.partial.render": "tvPrincipal:frmEmitirCertidaoOnline:gridNome tvPrincipal:frmEmitirCertidaoOnline:btnGerarCertidao",
    "tvPrincipal:frmEmitirCertidaoOnline:btnConsultar": "tvPrincipal:frmEmitirCertidaoOnline:btnConsultar",
    "tvPrincipal:frmEmitirCertidaoOnline": "tvPrincipal:frmEmitirCertidaoOnline",
    "tvPrincipal:frmEmitirCertidaoOnline:radioTipoPessoa": "CPF",
    "tvPrincipal:frmEmitirCertidaoOnline:mskCpfCnpj": "092.350.251-33",
    "g-recaptcha-response": "0.08iZuTV2vBQ5DiCbfIOKicrWH_u8FyMIAF7E5cEp4DGX4us2SWZopdqRKEV_5CkXF8stBgDrC_tW1eoiWePbJEHiATCspj50KEl8OXaprqEAxp4beW2befmWt2ZoC2GXmIbJSaIB_1LIoi7ZOUPCsqIMnPkrqkvZxOf9mOQfy740GvEDxY0PlsYxDsI4icCxKwBv91raImQxagz6Nez8hDf5le49TgSGBK3aKlhDkn4CpipyP9wY_Ds7eS_HUg7_DDgBHS7eruJWRJ-d7feBkTazC1_LF48zHFLmp6mJG9n73kqy0LarHX4-KONPrT6cknPfvj0P8duKupwPIlQbyxJkHb6rIsqvsL3RuvCKrobG8EYrwdgn_rYLuBgw2PQJNa623dmnCjpL-v3brOh2kSEoYTcRA6QBjBNpo-RNTHhV9DqNsxx4vJZO9PGU3IXmNNp3gNH2c-bobKKgmXh89CLQJfnabkLC2XwBQM81BVD_79kGUmNqT0_5BIjGHsvTfSvtS7lLj93fmmMFE2hOHVb2ElH3cLOgSWIBNOzLBynA_oKyV6_r_YoXAuUHPUG-wbbE2EuAXvrmH1uO6d03BDf8fLAIl8UgoFA6HQ0IvmYR_76E2gc4Ywd57zTXAxI5_8c-WBUdUOcmD2KJACu2_eDKkZgw4MXPlDwDjp5_ZyoUTYWip3fl6NFfedtrGl-LKbdh_b1NMM9JLLihaasbQZ3sUqZiru_O4ZHqIloYQ5S-nTt2gnTMcaMAtD22VALO5_fe-eBJG7tcj290FDjC_EOx-eYEtbh2uXXx2nj86-mO_2uC9FbsX_uUVqKkpSmclokohwynGzcD4HEimoJCtOJLdWGe-xHi0iqIKzgkrNp24Mrav8-dnIJw6Hd5v424yo6NnMQ8phr98PxA9Mfevw.DN4bCn_pBStEJcyRNfx2Dg.8ba661a995d399a9fcc9d2983801a4743a32ecf1586d78a00974f93fc1ddf950",
    "javax.faces.ViewState": "-1117770872599531985:4836472457166145076"
}

response = requests.post(url, headers=headers, data=payload)

print("Status Code:", response.status_code)
print("Response Body:", response.text)

# Exibir informações detalhadas sobre a resposta
print("Headers:", response.headers)
print("Encoding:", response.encoding)
print("URL Final:", response.url)
print("Histórico:", response.history)

# Exibir o conteúdo da resposta
if 'application/json' in response.headers.get('Content-Type', ''):
    print("JSON Response:", response.json())
else:
    print("Text Response:", response.text)