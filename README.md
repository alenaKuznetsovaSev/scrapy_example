Это мой переписанный проект питоновского парсера(отсюда -> https://github.com/alenaKuznetsovaSev/python_parser).
Программу нужно запускать в терминале командой:
  scrapy crawl tastemade
для начала парсига сайта https://www.tastemade.com/food в глубину.
Перед этим в scrapy_ex/__init__.py будет создан как прокси менеджер(для добычи прокси, используемых в процессу парсинга), так и saver - класс для записи данных в базу данных, используя sql алхимию.

 
