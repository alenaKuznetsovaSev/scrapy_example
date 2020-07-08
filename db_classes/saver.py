import re
import my_log
import csv
from sqlalchemy import create_engine
import config as cfg


class Saver:
    """сохраняет результаты в SQL"""

    def __del__(self):
        self.conn.close()

    def __init__(self):
        self.log = my_log.get_logger(__name__)
        self.log.debug('Saver was created')
        engine = create_engine("sqlite:///"+cfg.dbconfig['database']+".db")
        self.conn = engine.connect()

    def add_item_content_to_sql(self, content):
        # _SQL = "SELECT table_name FROM information_schema.tables WHERE table_name = '" + content['table_name']\
        #        + "' AND table_schema = database();"
        _SQL = "SELECT name FROM sqlite_master WHERE type ='table' AND name LIKE '%s'; " % content['table_name']
        table_exist = self.conn.execute(_SQL).fetchone()
        if table_exist:
            # self.logger.debug("table %s exist " % content['table_name'])
            _SQL = "INSERT INTO "+content['table_name']+" ("
            for k, v in content.items():
                if k != 'table_name':
                    _SQL += k + ", "
            _SQL = _SQL[0: -2] + ") VALUES ("

            for k, v in content.items():
                if k != 'table_name':
                    v = str(v).replace("'", "`")
                    v = v.replace('"', "``")
                    _SQL += "'" + v + "', "

            _SQL = _SQL[0: -2] + """);"""
            # _SQL = re.sub(r'[^\w\s!?.,;:@#$%^&*№><~`\[\]()]', "", _SQL)
            try:
                self.conn.execute(_SQL)
            except Exception as e:
                self.log.warn("we couldn`t insert into %s this SQL - %s, have this error : %s " % (content['table_name'], _SQL, e))
                # self.logger.error('error msg', e)
                return False, e
        else:
            self.log.warn("table %s does not exist " % content['table_name'])
            return False
        return True

    def add_list_of_links_to_sql(self, home_site_page, list_of_links) -> 'SQL execute':
        """generate SQL request for saving list of links items"""
        _SQL = """INSERT INTO links4parse (home_site_page, curr_link) VALUES """
        for i in range(len(list_of_links) - 1):
            _SQL += """("%s", "%s"), """ % (home_site_page, list_of_links[i])
        i = + 1
        _SQL += """("%s", "%s")""" % (home_site_page, list_of_links[i])
        try:
            self.conn.execute(_SQL)
        except Exception as e:
            self.log.error("we couldn`t insert into links4parse this SQL - %s " % _SQL)
            self.log.error('error msg', e)

    def write_row_in_file(self, file_name="database.csv", data=""):
        """функция для дописывания строки в файл"""
        with open(file_name, "a") as file:
            row = ""
            for i in data:
                row += "%s, " % i
            file.write(row[:-2] + "\n")
            file.close()

    def read_file(self, file_name="random_text.csv"):
        """функция для чтения из файла
        file_name - имя файла
        возвращает массив строк"""
        text = []
        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                text += row
        return text

    # % (invoke_attributes.__class__.__name__, invoke_attributes.__dir__()[1], status)

# with UseDatabase(cfg.dbconfig) as cursor:
#     _sql = """show tables"""
#     cursor.execute(_sql)
#     data = cursor.fetchall()
#     main_logger.debug(data)

# main_logger.debug(type(my_get))
# s = Saver()
# s.add_item_content_to_sql(my_get)
