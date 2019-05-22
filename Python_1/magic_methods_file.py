import tempfile
import os.path
import random


class File:

    content = ""

    def __init__(self, file_directory):
        self.file_directory = file_directory
        if not os.path.exists(self.file_directory):
            self.content = ""
            open(self.file_directory, "w").close()
        else:
            self.content = self.get_content()

    def get_content(self):
        content = ""
        with open(self.file_directory) as r:
            try:
                for line in r:
                    content += line
            except IndexError:
                raise StopIteration
        return content

    def __str__(self):
        return self.file_directory

    def write(self, string):
        self.content += string
        try:
            with open(self.file_directory, "w") as w:
                w.write(self.content)
        except IOError as err:
            print("Ошибка записи в файл: {}".format(err.args[1]))

    def __add__(self, obj):
        new_file = File(os.path.join(tempfile.gettempdir(),
                                     "{}.txt".format(random.randint(1, 1000000))))
        new_file.content = self.content + obj.content
        with open(new_file.file_directory, "w") as w:
            w.write(new_file.content)
        return new_file

    def __getitem__(self, index):
        temp_mas = self.content.split('\n')
        return temp_mas[index]