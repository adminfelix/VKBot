#coding:utf8


class Plugin(object):
    __doc__ = '''Плагин предназначен для проверки активности бота
    Использование: ping
    Пример: ping'''

    name = 'ping'
    keywords = (u'пинг', name)
    protection = 0
    argument_required = False

    def respond(self, msg, rsp, *args, **kwargs):
        rsp.forward_id = 0
        rsp.text = 'pong'

        return rsp