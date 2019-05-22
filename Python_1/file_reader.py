class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            with open(self.file_name) as f:
                return f.read()
        except IOError as err:
            print("Ошибка чтения файла: {}".format(err.args[1]))
            return ""


reader = FileReader("")
print(reader.read())