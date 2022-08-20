"""АПИ НН"""
import random
import time
import requests
import json
from flask import current_app
from flask_login import current_user
from finding_work.models import Post, db


user_agent = {'User-agent': 'Mozilla/5.0; Chrome/103.0.0.0 Safari/537.36'}

# без опыта и с опытом 1-3
url = 'https://api.hh.ru/vacancies/?text=python&search_field=name&experience=noExperience&experience=between1And3&employment=full&schedule=remote'
url2 = 'https://api.hh.ru/vacancies/'


def receive_update(vacancy, ids):
    if 'id' in vacancy:  # если вакансия имеет ключ id, т.е. актуальна
        post_item = Post.query.filter(Post.id_hh == vacancy['id']).first()
        # если такой вакансии нет в БД
        if not post_item:
            print(f"Новая вакансия: {vacancy['employer']['name']}")
            if vacancy['salary']:
                vacancy['salary'] = str(vacancy['salary']['from']) + ' - ' + str(
                    vacancy['salary']['to']) + ' ' + vacancy['salary']['currency']
            else:
                vacancy['salary'] = 'Зарплата не указана'
            new_post = Post(id_hh=int(vacancy['id']), href='https://ryazan.hh.ru/vacancy/'+vacancy['id'], title=vacancy['name'], author=vacancy['employer']['name'],
                            salary=vacancy['salary'], experience=vacancy['experience']['name'], type_of_work=vacancy['schedule']['name'], content=vacancy['description'], status='NEW', note=None, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            current_app.logger.warning(
                f'Новая вакансия с ID {int(vacancy["id"])} внесена в базу данных.')
    else:  # вакансия не пришла значит объявление закрыто
        print("Вакансия с", ids, "закрыта.")
        post_item = Post.query.filter(Post.id_hh == ids).first()
        post_item.status = 'CLOSED'
        db.session.commit()
        current_app.logger.warning(
            f'Вакансия с ID {post_item.id} - {post_item.author} была закрыта.')


def receive_all_vacancies(id_list):
    all_id = Post.query.filter(Post.status != 'CLOSED')
    current_id_list = [item.id_hh for item in all_id]
    # получаем новый список текущих ID и новых ID
    id_list.extend(current_id_list)
    new_id_list = set(id_list)
    for ids in new_id_list:
        # запрос на просмотр вакансии только для Heroku делаем задержку
        time.sleep(random.random())
        vacancy = send_request_vacancy(url=url2+str(ids))
        receive_update(vacancy, ids)


def receive_all_id():
    id_list = []
    id_list_temp = send_request(url+'&page=0&per_page=20', first=True)
    if id_list_temp:
        all_id = id_list_temp[0]
        all_pages = id_list_temp[1]
        id_list.extend(id_list_temp[2])
        for i in range(1, all_pages):
            id_list_temp = send_request(url+'&per_page=20&page=' + str(i))
            if id_list_temp:
                id_list.extend(id_list_temp)
            else:
                break
    # если количество вакансий по апи равно количеству полученных id
    if len(id_list) == all_id:
        current_app.logger.info("Список ID получен успешно.")
        print('Список ID получен успешно.')
        receive_all_vacancies(id_list)
        return True
    return False


# отправка запроса на получение списка ID
def send_request(url, headers=user_agent, first=False):
    while True:
        res = requests.get(url, headers)
        if res.status_code == 200:  # если 200
            res_json = json.loads(res.text)
            id_list_temp = [int(id['id']) for id in res_json['items']]
            if first:
                all = res_json['found']
                pages = res_json['pages']
                return all, pages, id_list_temp
            return id_list_temp
        time.sleep(random.randint(1, 3))


# отправка запроса на получение вакансии
def send_request_vacancy(url, headers=user_agent):
    for i in range(100):
        time.sleep(random.random())
        res = requests.get(url, headers)
        if res.status_code != 200 or res.status_code != 404:
            print(
                f"Попытка № {i} получить данные не удалась {res.status_code}")
            continue
        else:
            res_json = json.loads(res.text)
            return res_json
