import csv
import os
import sys


class CarBase:

    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = str(car_type)
        self.brand = str(brand)
        self.photo_file_name = str(photo_file_name)
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        extension = os.path.splitext(self.photo_file_name)[1]
        return extension


class Car(CarBase):

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.car_type = "car"
        self.passengers_seats_count = int(passenger_seats_count)
        super().__init__(car_type=self.car_type, brand=brand,
                         photo_file_name=photo_file_name, carrying=carrying)


class Truck(CarBase):

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = "truck"
        self.body_whl = str(body_whl)
        temp_mas = body_whl.split('x')

        try:
            self.body_length = float(temp_mas[0])
            self.body_width = float(temp_mas[1])
            self.body_height = float(temp_mas[2])
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0

        super().__init__(car_type=self.car_type, brand=brand,
                         photo_file_name=photo_file_name, carrying=carrying)

    def get_body_volume(self):
        volume = self.body_length * self.body_width * self.body_height
        return volume


class SpecMachine(CarBase):

    def __init__(self, brand, photo_file_name, carrying, extra):
        self.extra = str(extra)
        self.car_type = "spec_machine"
        super().__init__(car_type=self.car_type, brand=brand,
                         photo_file_name=photo_file_name, carrying=carrying)


def get_car_list(csv_filename):
    car_list = []

    try:
        with open(csv_filename) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)
            for row in reader:
                try:
                    if row_check(row) and not create_car(row[0], row)==False:
                        car_list.append(create_car(row[0], row))
                except IndexError:
                    continue
    except IOError as err:
        print("Ошибка чтения файла: {}".format(err.args[1]))

    return car_list


def row_check(row):
    def check_car_type():
        return str(row[0]) == "car" or str(row[0]) == "truck" or \
               str(row[0]) == "spec_machine"

    def check_photo():
        return not str(row[3]) == "." and not str(row[3]).find(".") == -1\
               and not str(row[3]).rfind(".") == 0

    def check_brand():
        return not str(row[1]) == ""

    def check_carrying():
        try:
            float(row[5])
            return True
        except ValueError:
            return False

    if check_car_type() and check_photo() and check_brand() and check_carrying():
        return True
    else:
        return False


def create_car(car_type, row):
    car_type = str(car_type)

    def check_car():
        try:
            int(row[2])
            return str(row[4]) == "" and str(row[6]) == ""
        except ValueError:
            return False

    def check_truck():
        return str(row[2]) == "" and str(row[6]) == "" and \
               (str(row[4]).count("x") == 2 or str(row[4]) == "")

    def check_spec_machine():
        return not str(row[6]) == "" and str(row[2]) == "" and str(row[4]) == ""

    if car_type == "car" and check_car():
        return Car(row[1], row[3], row[5], row[2])

    if car_type == "truck" and check_truck():
        return Truck(row[1], row[3], row[5], row[4])

    if car_type == "spec_machine" and check_spec_machine():
        return SpecMachine(row[1], row[3], row[5], row[6])

    return False


if __name__ == "__main__":
    print(get_car_list(sys.argv[1]))
    print(Car)