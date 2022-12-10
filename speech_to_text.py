import boto3
import requests
import os

import config

# Путь к этому скрипту
app_path = os.path.dirname(__file__)

# Путь откуда берём аудиозаписи формата .ogg
ogg_path = os.path.join(app_path, 'ogg')

# Путь куда кладём текст из результатов распознавания .txt
txt_path = os.path.join(app_path, 'text')


def file_to_storage(file_path, bucket_name, result_file_name):
    '''Функция возращает ссылку на аудиофайл из Бакета SpeechKit
      предварительно загрузив его туда из локальной папки'''

    session = boto3.session.Session(region_name=config.REGION_NAME, aws_access_key_id=config.AWS_SECRET_KEY_ID,
                                    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY)

    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    link_head = "https://storage.yandexcloud.net/"

    try:
        s3.upload_file(file_path, bucket_name, result_file_name)
        file_link = link_head + bucket_name + "/" + result_file_name
    except:
        file_link = None

    return file_link


def speech_to_text(api_key, filelink, txt_path):
    '''Функция распознавания аудио и формирования текста аудио,
    сохранив его в файл .txt в локальную папку'''

    POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"

    # Формируем сам текст запроса
    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "model": "deferred-general",
                "literature_text": True
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    # Если вы хотите использовать IAM-токен для аутентификации, замените Api-Key на Bearer.
    header = {'Authorization': 'Api-Key {}'.format(api_key)}

    # Отправить запрос на распознавание.
    req = requests.post(POST, headers=header, json=body)

    data = req.json()
    id = data['id']

    print(data)
    with open(os.path.join(txt_path, id + '.req'), 'w') as j:
        print(data, file = j)

if __name__ == '__main__':
    list_ogg = [line for line in os.listdir(path=ogg_path) if '.ogg' in line]

    for audio in list_ogg:
        print(audio)
        file_path = os.path.join(ogg_path, audio)
#        result_file_name = str(audio[:(len(audio) - 4)] + '.ogg')
        filelink = str(file_to_storage(file_path, config.BUCKET_NAME, audio))
        speech_to_text(config.API_KEY, filelink, txt_path)
    print('Speech recognition completed')
