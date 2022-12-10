import os
import requests

import config

# Этот скрипт получает расшифрованный текст из отправленных ранее запросов на отложенную расшифровку

# Путь к этому скрипту
app_path = os.path.dirname(__file__)

# Путь откуда берём аудиозаписи формата .ogg
ogg_path = os.path.join(app_path, 'ogg')

# Путь куда кладём текст из результатов распознавания .txt
txt_path = os.path.join(app_path, 'text')

def get_text_from_API(api_key, id, result_file_name):

    # Если вы хотите использовать IAM-токен для аутентификации, замените Api-Key на Bearer.
    header = {'Authorization': 'Api-Key {}'.format(api_key)}

    GET = "https://operation.api.cloud.yandex.net/operations/{id}"
    req = requests.get(GET.format(id=id), headers=header)
    req = req.json()

    # Выходной файл без расширения
    out_file_name = os.path.join(txt_path, result_file_name[:(len(result_file_name) - 4)])

    # Сохранение последнего ответа
    with open(out_file_name + '.ans', 'a', encoding='UTF-8') as answer_file:
        print(req, file = answer_file)

    if req['done'] and req.get('response'):
        # Сохранить текст из результатов распознавания в файл.

        f = open(out_file_name + '.txt', 'w')
        for chunk in req['response']['chunks']:
            if chunk['channelTag'][0] == '1':
                f.write(str(chunk['alternatives'][0]['text']) + '\n')
        f.close()
    else:
        print("Not ready")

if __name__ == '__main__':
    list_req = [line for line in os.listdir(path=txt_path) if '.req' in line]

    for req in list_req:
        print(req)
        id = str(req[:(len(req) - 4)])
        file_path = os.path.join(txt_path, req)
        result_file_name = id + '.txt'
        get_text_from_API(config.API_KEY, id, result_file_name)
    print('Done')
