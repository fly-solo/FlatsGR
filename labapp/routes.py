# -*- coding: utf-8 -*-
# Подключаем объект приложения Flask из __init__.py
from labapp import app
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json
from . import controller  # подключаем controller.py

"""
    Модуль регистрации маршрутов для запросов к серверу, т.е.
    здесь реализуется обработка запросов при переходе пользователя на определенные адреса веб-приложения
"""


# Обработка запроса к индексной странице
@app.route('/')
@app.route('/HOME')
def HOME():
    imgs = ['logo.png', 'кв1.jpg', 'кв2.jpg']
    # Пример вызова метода с выборкой данных из БД и вставка полученных данных в html-шаблон
    processed_files = controller.get_source_files_list()
    # "рендеринг" (т.е. вставка динамически изменяемых данных) в index.html и возвращение готовой страницы
    return render_template('HOME.html', title='FlatsGR', navmenu=controller.navmenu, imgs=imgs, processed_files=processed_files)

@app.route('/Flats')
def Flats():
    imgs = ['logo.png', 'кв1.jpg', 'кв2.jpg']
    processed_files = controller.get_source_files_list()
    sorted_rent_file = controller.get_sort_rent_from_source_files()
    return render_template('Flats.html', title='FlatsGR', imgs=imgs, navmenu=controller.navmenu, processed_files=processed_files, sorted_rent_file=sorted_rent_file)
# Обработка запроса к странице contact.html

@app.route('/AboutUS')
def AboutUS():
    imgs = ['1.jpg', '2.jpg', '3.jpg', '4.jpg']
    return render_template('AboutUS.html', title='О нас', pname='About us', navmenu=controller.navmenu, imgs=imgs)

# Пример обработки POST-запроса для демонстрации подхода AJAX
@app.route('/api/contactrequest', methods=['POST'])
def post_contact():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте нет, например, обязательного поля 'name'
    if not request.json or not 'firstname' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ
    else:
        msg = request.json['firstname'] + ", ваш запрос получен !";
        return json_response({'message': msg})


"""
Реализация response-методов, возвращающих клиенту стандартные коды протокола HTTP
"""

@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={'error': 'Not found', 'code': 404})

# Формирование json-ответа. Если в метод передается только data (dict-объект), то по-умолчанию устанавливаем код возврата code = 200
# В Flask есть встроенный метод jsonify(dict), который также реализует данный метод (см. пример метода not_found())
def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))


# Пример формирования json-ответа с использованием встроенного метода jsonify()
# Обработка ошибки 404 протокола HTTP (Данные/страница не найдены)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


# Обработка ошибки 400 протокола HTTP (Неверный запрос)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)