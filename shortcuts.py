# Вспомогательные функции для проекта Chat
def parser_command(message):
    """
    Если сообщение является командой, парсит его
    :param message: сообщение от сервера
    :return: Команду и значение
    """
    if message[0] == "#":
        command = message[1:message.find(":")]
        value = message[message.find(":")+1:]
        return command, value

    return message

if __name__ == '__main__':
    """Все тесты пишем тут """
    pass