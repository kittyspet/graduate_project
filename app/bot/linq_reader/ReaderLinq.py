import requests
import json


from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning) # TODO: Изменить на нормальное

# используйте либо логин-пароль, либо токен
# TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
 

token_value = "ecHbw0w0s0qIT169CvbgA" # TODO: from .env
# при необходимости, указывайте протокол https в строке с реальным адресом домена системы. 
# после адреса домена может быть указан еще и каталог размещения системы на домене (например, https://domain.example.ru/Master )
DOMAIN = 'https://advantasrv.yakovlev.ru' 
 
# session = requests.Session()
 
# # авторизация
# # response = session.post(
# #     url = DOMAIN + '/api/auth/login', 
# #     json = {
# #         'Login': LOGIN, 
# #         'Password': PASSWORD,
# #     },
# # )
# #либо авторизуйтесь, используя токен доступа
# response = session.post(
#     url = DOMAIN + '/api/auth/login', 
#     json = {
#         'tokenValue': "ecHbw0w0s0qIT169CvbgA", 
#     }, verify=False
# )
 
# # сохранение полученных после авторизации cookies для последующих запросов  
# cookies = session.cookies.get_dict()
 
# # параметры для обращения к LINQ-запросу (может быть больше, см. выше)
# LINQ = {
#     'DataSourceId': "fa2e78e9-c572-45a9-917d-0e0d8de81f07", # id LINQ-запроса в системе ADVANTA
#     'PageSize': 1000, # максимальное количество возвращаемых записей
#     'Parameters': { "id_veh": "6d9d9529-9aa4-4208-bda3-943d22aec8aa" }
# }
 
# # получение данных из LINQ-запроса
# response = session.post(
#     url = DOMAIN + '/api/queries/get', 
#     cookies = cookies, 
#     json = LINQ,

# )
 
# import json
# data = response.json()

# print(data[-1])

# with open('data.json', 'w', encoding='utf-8') as f:
#     json.dump(data[-1], f, ensure_ascii=False)


class ReaderLinq:
    def  __init__(self):
        pass
        # self.session = requests.Session()
        # response = self.session.post(
        #     url = DOMAIN + '/api/auth/login', 
        #     json = {
        #         'tokenValue': token_value,
        #     }, verify=False)
        # # if (response.status_code != "OK"): TODO: изменить на нормальный
        # #     raise Exception(response.json)
        # self.cookies = self.session.cookies.get_dict()
    
    def getResponseJson(self, idLINQ, pageSize=100, parameters={}):
        pass
        # LINQ = {
        #     'DataSourceId': idLINQ, # id LINQ-запроса в системе ADVANTA
        #     'PageSize': pageSize, # максимальное количество возвращаемых записей
        #     'Parameters': parameters
        # }
        # response = self.session.post(
        #     url = DOMAIN + '/api/queries/get', 
        #     cookies = self.cookies, 
        #     json = LINQ,verify=False
        # )
        # return response.json()
    
    def getResponseJsonFromFile(fileName):
        with open('/media/' + fileName, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data:
                return data
            else:
                return []

