from interface import Interface
import json


class InMemoryStorage(Interface):

    def __init__(self):
        self.__setup_json()

    def __setup_json(self):
        try:
            with open('books.json') as book_db:
                self.book_db = json.load(book_db)
        except:
            book_db = {"books": {}}
            with open('books.json', 'w') as db:
                json.dump(book_db, db)
        finally:
            with open('books.json') as book_db:
                self.book_db = json.load(book_db)

    def create(self, **kwargs):
        try:
            val = str(kwargs['id'])
            if val in self.book_db['books']:
                self.book_db['books'][val]['title'].append(kwargs['title'])
                self.__database()
                return f"Book added to {self.book_db['books'][val]['author']} book list"
            else:
                record = self.book_db['books'][val] = {'author': kwargs['author'], 'title': [kwargs['title']]}
                self.__database()
                return record
        except KeyError:
            self.__error_message()

    def fetch(self, rem=None, **kwargs,):
        key = [key for key in kwargs]
        try:
            if len(kwargs) > 1:
                if 'title' and 'author' in key:
                    data = self.__database(key, [kwargs['author'], kwargs['title']], rem)
                    return data
            else:
                if 'id' in key:
                    data = self.__database(key, [kwargs['id']], rem)
                    return data
                elif 'author' in key:
                    data = self.__database(key, [kwargs['author']], rem)
                    return data

        except KeyError:
            self.__error_message()

    def __database(self, identifier=None, command=None, rem=None):
        data = []
        if isinstance(command, str):
            for x in self.book_db['books'].items():
                data.append(x)
            return data

        elif isinstance(command, list):
            if len(command) > 1:
                if rem:
                    try:
                        for x in self.book_db['books'].values():
                            if x['author'] == command[0] and command[1] in x['title']:
                                val = x['title'].index(command[1])
                                n_val = x['title'].pop(val)
                                data.append(n_val)
                        return data
                    except:
                        return 'No such record'
                else:
                    for x in self.book_db['books'].values():
                        if x['author'] == command[0] and command[1] in x['title']:
                            data.append(x)

                    return data

            else:
                key = str(command[0])
                if identifier[0] == 'id':
                    if rem:
                        try:
                            for x in self.book_db.values():
                                self.book_db['books'].pop(key)
                                data.append(x)
                            return data
                        except:
                            return 'No such record'
                    else:
                        for x in self.book_db.values():
                            data.append(x[key])

                        return data if data else 'No Book Found!'

                if identifier[0] == 'author':
                    if rem:
                        try:
                            for _id in self.book_db['books'].keys():
                                if self.book_db['books'][_id]['author'] == key:
                                    val = self.book_db['books'].pop(_id)
                                    data.append(val)
                                return data
                        except:
                            return 'No such record'
                    else:
                        for x in self.book_db['books'].values():
                            if x['author'] == key:
                                data.append(x)
                        return data if data else 'No Book Found!'

        with open('books.json', 'w') as db:
            json.dump(self.book_db, db)

    def all(self):
        return self.__database('', 'all')

    def __error_message(self, error='key'):
        if error == 'key':
            raise KeyError('use: id="value", author="author", title="title"')
        else:
            raise Exception

    def delete(self, **kwargs):
        val = self.fetch(True, **kwargs)
        self.__database()
        return val
