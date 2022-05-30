"""
This file contains some function to test the basic functionality of the whole project.
It will be extended by a realy testing framework in the future.
"""

from TelegramBot import TelegramBot
from InstagramBot import InstagramBot
import db

database = db.OrmAbstraction()
telegram = TelegramBot(database)
instagram = InstagramBot(database)


def base_test(func):
    def wrapper():
        print(f"Testing function: {func}")
        try:
            print("--------------------------------")
            func()
            print("--------------------------------")
            return print('--> Test passed!')
        except Exception as e:
            print('\033[31m' + "Test failed" + '\033[0m')
            print(e)

    return wrapper


@base_test
def test_instagram_fetch_updates_method():
    instagram.fetch_updates()


@base_test
def test_instagram_get_all_items_method():
    items = instagram.get_all_items()
    print(f"Value: {items}")


@base_test
def test_telegram_fetch_updates_method():
    telegram.fetch_updates()

@base_test
def test_telegram_get_all_items_method():
    items = telegram.get_all_items()
    print(f"Value: {items}")

@base_test
def test_database_get_ids_by_instagram():
    items = set(map(lambda post: post[0], database.get_ids_by_platform("instagram")))
    print(f"Value: {items}")

@base_test
def test_database_get_ids_by_telegram():
    items = set(map(lambda post: post[0], database.get_ids_by_platform("telegram")))
    print(f"Value: {items}")


test_instagram_fetch_updates_method()
test_instagram_get_all_items_method()
test_telegram_fetch_updates_method()
test_telegram_get_all_items_method()
test_database_get_ids_by_instagram()
test_database_get_ids_by_telegram()