import requests
import os

from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    """ Проверка того, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter = ""):
    """ Проверка, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем, что запрос возвращает статус 200 и, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key,filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name = "Вася", animal_type="Сиамская", age='6',
    pet_photo='images/adorable-looking-kitten-with-yarn.jpg'):
    """Проверка, что можно добавить питомца с корректными данными. Проверяем , что запрос возвращает статус 200 и ,
     что имя добавленного питомца есть в теле ответа от сервера"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_pet():
    """Проверка возможности удаления питомца. Запрашиваем список своих питомцев. Проверяем - если список своих питомцев пустой, то добавляем нового
     и опять запрашиваем список своих питомцев. Далее берём id первого питомца из списка и отправляем запрос на удаление.
     Проверяем, что статус ответа равен 200 и в списке питомцев нет pet_id удалённого питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Тузик", "Боксер", "5")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_info_pet(name = "Мурзик", animal_type = "Персидская", age = "1"):
    """Проверка возможности обновления информации о питомце. Запрашиваем список своих питомцев. Если список не пустой,
     то пробуем обновить его имя, тип и возраст, далее проверяем , что статус ответа = 200 и имя питомца соответствует заданному.
     Если спиок питомцев пустой, то печатаем исключение с текстом об отсутствии своих питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"])> 0:
        status, result = pf.update_info_pet(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)
        assert status == 200
        assert result["name"] == name
    else:
        raise Exception ("There is no my pets")

def test_get_api_key_for_invalid_user(email = invalid_email, password = invalid_password):
    """1 test. Проверка того, что при вводе невалидных email и password, возвращается статус 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_all_pets_with_valid_key_filter_my_pets(filter = "my_pets"):
    """ 2 test.Проверка того, что запрос собственных питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список собственных питомцев и проверяем, что запрос возвращает статус 200 и, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key,filter)
    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet_without_name(name = None, animal_type="Мейн кун", age='7',
    pet_photo='images/adorable-looking-kitten-with-yarn.jpg'):
    """3 test.Проверка того, что при передаче пустого поля name, запрос возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

def test_add_new_pet_with_invalid_auth_key(name = "Горох", animal_type="Шиншила", age='4',
    pet_photo='images/adorable-looking-kitten-with-yarn.jpg'):
    """4 test. Проверка того, что при передаче несуществующего ключа auth_key в запрос на добавление питомца,
    возвращается статус 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key["key"] = auth_key["key"] + "qwerty1234"
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403

def test_unsuccessful_delete_pet_with_invalid_auth_key():
    """5 test. Проверка того, что при передаче несуществующего ключа auth_key в запрос на удаление питомца,
    возвращается статус 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Тузик", "Боксер", "5")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    auth_key["key"] = auth_key["key"] + "qwerty1234"
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status == 403

def test_unsuccessful_delete_pet_with_invalid_pet_id():
    """6 test. Проверка того, что при передаче несуществующего pet_id_inv в запрос на удаление питомца,
    не возвращается статуса 200.
    Баг - При попытке передачи несуществующего pet_id_inv в запрос на удаление питомца, возвращается статус 200."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Тузик", "Боксер", "5")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    pet_id_inv = pet_id + "qwerty123"
    status, result = pf.delete_pet(auth_key, pet_id_inv)
    assert status != 200

def test_unsuccessful_update_info_pet_with_invalid_auth_key(name = "Инокентий", animal_type = "Ара", age = "13"):
    """7 test.Проверка того, что при передаче несуществующего ключа auth_key в запрос на обновление данных питомца,
    возвращается статус 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key["key"] = auth_key["key"] + "qwerty1234"
    if len(my_pets["pets"])> 0:
        status, result = pf.update_info_pet(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)
        assert status == 403
    else:
        raise Exception ("There is no my pets")

def test_add_new_pet_without_photo_valid_data(name = "Пурга", animal_type="Хаски", age='2'):
    """8 test. Проверка того, что можно добавить питомца с корректными данными (без фото). Проверяем , что запрос возвращает
    статус 200 и , что имя добавленного питомца есть в теле ответа от сервера"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_invalid_data(name="Гендальф", animal_type= None, age='4'):
    """9 test. Проверка того , что можно добавить питомца (без фото) с неуказанным значением animal_type. Проверяем , что
    запрос возвращает статус 400."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400


def test_add_new_pet_without_photo_with_invalid_auth_key(name="Гендальф", animal_type= "Мопс", age='4'):
    """10 test. Проверка того, что при передаче несуществующего ключа auth_key в запрос на добавление питомца (без фото),
    возвращается статус 403."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403

def test_successful_add_pet_photo(pet_photo='images/beautiful-white-cat-with-balls-indoors.jpg'):
    """11 test. Проверка того, что при передаче несуществующего ключа auth_key в запрос на добавление фото питомцу,
    возвращается статус 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert "pet_photo" in result

def test_unsuccessful_add_pet_photo_with_format_file_mp3(pet_photo= "images/deti-online.com_-_pesnya-mamontenka.mp3"):
    """12 test. Проверка того, что при загрузке файла отличного от формата изображения, возвращается
    статус 500"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 500

def test_unsuccessful_add_pet_photo_with_invalid_auth_key(pet_photo='images/beautiful-white-cat-with-balls-indoors.jpg'):
    """13 test. Проверка того, что можно добавить фото собственному питомцу. Проверяем , что запрос возвращает
    статус 200 и , что  название фото питомца есть в теле ответа от сервера"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    auth_key["key"] = auth_key["key"] + "qwerty1234"
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 403





