# coding:utf8


import time
import traceback

import requests as r

from kivy.app import App

import vk_api as vk
from utils import load_token, save_token, TEMP_IMAGE_FILE


# globals

api = None


def error_handler(request):
    def do_request(*args, **kwargs):
        error = None

        try:
            send_log_line(
                u'Вызов: [b]%s[/b]' % request.__name__, 0, time.time())
            response = request(*args, **kwargs)
        except Exception as raw_error:
            send_log_line(
                u'Возникла ошибка (vkrequests): %s' %
                    traceback.format_exc().decode('utf8'),
                0
            )
            error = str(raw_error).lower()

            if 'timed out' in error:
                send_log_line(
                    u'Ошибка [b]timed out[/b]. Повторяю запрос...', 1)
                return do_request(*args, **kwargs)

            elif '[errno -3]' in error \
                    or '[errno 7]' in error \
                    or '[errno 8]' in error \
                    or '[errno 101]' in error \
                    or '[errno 111]' in error \
                    or '[errno 113]' in error \
                    or 'connection' in error:
                send_log_line(u'Ошибка сети. Жду 10 секунд...', 1)
                time.sleep(10)

                return do_request(*args, **kwargs)

            return False, error
        else:
            return response, error

    return do_request


def _save_token(token=None):
    if token is None:
        token = api._vk.token['access_token']
    save_token(token)


def set_new_logger_function(func):
    global send_log_line
    send_log_line = func
    send_log_line(u'Подключена функция логгирования для vkrequests', 0)


def send_log_line(line, log_importance, t=None):
    pass


@error_handler
def log_in(login=None, password=None,
           twofactor_handler=None, captcha_handler=None,
           logout=False
           ):

    global api

    if logout:
        api = None
        _save_token(token='')
        return False

    token = load_token()

    session_params = {
                        'auth_handler': twofactor_handler,
                        'captcha_handler': captcha_handler,
                        'app_id': '6045412',
                        'scope': '70660',  # messages, status, photos, offline
                        'api_version': '5.69'
                     }

    if login and password:
        session_params['login'] = login
        session_params['password'] = password

        session = vk.VkApi(**session_params)
        session.auth(reauth=True)

        api = session.get_api()

        _save_token()
    else:
        if not token:
            raise Exception('No token')

        session_params['token'] = token

        session = vk.VkApi(**session_params)

        if not session.check_token():
            return False

        api = session.get_api()

    return True


@error_handler
def send_message(text, pid, forward=None, attachments=[], sticker=None
                 ):

    attachments = ','.join(attachments)

    response = api.messages.send(
        peer_id=pid, message=text,
        forward_messages=forward,
        attachment=attachments,
        sticker_id=sticker
    )

    return response


@error_handler
def attach_image(pid, image_url='', image_path=''):
    if image_url:
        image_response, error = http_r_get(image_url)
        image = open(TEMP_IMAGE_FILE, 'w+b')
        image.write(image_response.content)
        image.seek(0)

        if error:
            raise Exception(error)
    else:
        image = open(image_path, 'rb')

    upload_data = api.photos.getMessagesUploadServer(peer_id=pid)

    response, error = \
        http_r_post(upload_data['upload_url'], files={'photo': image})

    image.close()

    if error:
        raise Exception(error)

    json_data = response.json()

    if json_data['photo'] == '[]':
        raise Exception('Could not upload image !')

    save_response = api.photos.saveMessagesPhoto(photo=json_data['photo'],
                                                 server=json_data['server'],
                                                 hash=json_data['hash'])[0]

    image_id = 'photo' + \
        str(save_response['owner_id']) + '_' + str(save_response['id'])

    return image_id


@error_handler
def get_self_id():
    return api.users.get()[0]['id']


@error_handler
def get_message_long_poll_data():
    return api.messages.getLongPollServer(need_pts=1)


@error_handler
def get_message_updates(ts, pts):
    response = api.messages.getLongPollHistory(ts=ts, pts=pts)

    return response['history'], response['new_pts'], response['messages']


@error_handler
def get_album_size(album_id):
    return api.photos.get(count=0, album_id=album_id)['count']


@error_handler
def get_photo_id(album_id, offset=0):
    photo = api.photos.get(offset=offset, album_id=album_id)['items'][0]
    media_id = 'photo%d_%d' % (photo['owner_id'], photo['id'])

    return media_id


@error_handler
def get_status():
    return api.status.get()


@error_handler
def set_status(text):
    api.status.set(text=text)

    return True


@error_handler
def get_name_by_id(object_id=None, name_case='nom'):
    if object_id is not None:
        object_id = int(object_id)

    if object_id is None or 0 < object_id < 2000000000:  # user
        response = api.users.get(user_ids=object_id, name_case=name_case)[0]
        name = ' '.join((response['first_name'], response['last_name']))

    elif int(object_id) > 2000000000:  # chat
        response = api.messages.getChat(chat_id=object_id - 2000000000)
        name = response['title']

    elif int(object_id) < 1:  # group
        response = api.groups.getById(group_id=abs(object_id))[0]
        name = response['name']

    else:
        name = 'Unknown object'

    return name


@error_handler
def get_user_city(user_id=None):
    return api.users.get(user_ids=user_id, fields='city')[0]['city']['title']


@error_handler
def get_real_user_id(user_short_link):
    return api.users.get(user_ids=user_short_link)[0]['id']


@error_handler
def http_r_get(url, **kwargs):
    send_log_line(
        u'Запрос: %s %s [GET]' % (url, str(kwargs).decode('unicode-escape')),
        0, time.time()
    )
    response =  r.get(url, **kwargs)

    return response


@error_handler
def http_r_post(url, **kwargs):
    send_log_line(
        u'Запрос: %s %s [POST]' % (url, str(kwargs).decode('unicode-escape')),
        0, time.time()
    )
    response =  r.post(url, **kwargs)

    return response