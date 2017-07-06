import mikr_api




def id_item(router, question):
    logging.debug('Отправляю запрос {}'.format(question))
    with io.StringIO() as buf, redirect_stdout(buf):
        router.writeSentence(question)
        router.readall()
        answer = buf.getvalue()
    logging.debug('Получен ответ {}'.format(answer))
    if '>>> =message=failure: item with such name already exists' in answer.split('\n'):
        logging.warning('Указанный item уже существует!!!')
        return
    for line in answer.split('\n'):
        if match('^.*=ret=.*$', line):
            ID_ITEM = match('^.*=ret=(.*)$', line).group(1)
            return ID_ITEM
        if match('^.*=.id=.*$', line):
            ID_ITEM = match('^.*=.id=(.*)$', line).group(1)
            return ID_ITEM




id_script1 = id_item(router, ['/system/script/add', '=name={}'.format(name_script), '=policy={}'.format(choosed_policy)])
if not id_script1:
    logging.warning('ID item не был возвращен!!!')
    id_script1 = id_item(router, ['/system/script/print', '?name={}'.format(name_script)])
    logging.debug('Получен ID item {}....'.format(id_script1))
else:
    logging.debug('Получен ID item {}....'.format(id_script1))


re


