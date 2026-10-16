
import json
import xml.etree.ElementTree as ET


# Класс должности
class Position:
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary


# Класс отдела
class Department:
    def __init__(self, name: str):
        self.name = name


# Класс сотрудника
class Employee:
    def __init__(
        self,
        employee_id: int,
        full_name: str,
        position: Position,
        department: Department
    ):
        self.employee_id = employee_id
        self.full_name = full_name
        self.position = position
        self.department = department

    def show_info(self) -> None:
        print(
            f"ID: {self.employee_id}, "
            f"ФИО: {self.full_name}, "
            f"Должность: {self.position.name}, "
            f"Отдел: {self.department.name}, "
            f"Зарплата: {self.position.salary}"
        )


# Класс компании
class Company:
    def __init__(self, name: str):
        self.name = name
        self.employees: list[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        if any(
            item.employee_id == employee.employee_id
            for item in self.employees
        ):
            raise ValueError("Сотрудник с таким ID уже существует.")

        self.employees.append(employee)

    def get_employee(self, employee_id: int) -> Employee:
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

        raise ValueError("Сотрудник не найден.")

    def show_employees(self) -> None:
        if not self.employees:
            print("Список сотрудников пуст.")
            return

        for employee in self.employees:
            employee.show_info()

    def update_employee(
        self,
        employee_id: int,
        full_name: str,
        position: Position,
        department: Department
    ) -> None:
        employee = self.get_employee(employee_id)
        employee.full_name = full_name
        employee.position = position
        employee.department = department

    def delete_employee(self, employee_id: int) -> None:
        employee = self.get_employee(employee_id)
        self.employees.remove(employee)


# Класс для сохранения и загрузки данных
class EmployeeFile:
    @staticmethod
    def save_json(company: Company, filename: str) -> None:
        data = []

        for employee in company.employees:
            data.append({
                "employee_id": employee.employee_id,
                "full_name": employee.full_name,
                "position": employee.position.name,
                "salary": employee.position.salary,
                "department": employee.department.name
            })

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_json(company: Company, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        employees = []

        for item in data:
            employee = Employee(
                int(item["employee_id"]),
                item["full_name"],
                Position(item["position"], float(item["salary"])),
                Department(item["department"])
            )
            employees.append(employee)

        company.employees = employees

    @staticmethod
    def save_xml(company: Company, filename: str) -> None:
        root = ET.Element("employees")

        for employee in company.employees:
            item = ET.SubElement(root, "employee")

            ET.SubElement(
                item, "employee_id"
            ).text = str(employee.employee_id)

            ET.SubElement(
                item, "full_name"
            ).text = employee.full_name

            ET.SubElement(
                item, "position"
            ).text = employee.position.name

            ET.SubElement(
                item, "salary"
            ).text = str(employee.position.salary)

            ET.SubElement(
                item, "department"
            ).text = employee.department.name

        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ")
        tree.write(
            filename,
            encoding="utf-8",
            xml_declaration=True
        )

    @staticmethod
    def load_xml(company: Company, filename: str) -> None:
        tree = ET.parse(filename)
        root = tree.getroot()

        employees = []

        for item in root.findall("employee"):
            employee = Employee(
                int(item.findtext("employee_id")),
                item.findtext("full_name"),
                Position(
                    item.findtext("position"),
                    float(item.findtext("salary"))
                ),
                Department(item.findtext("department"))
            )
            employees.append(employee)

        company.employees = employees


# Основная программа
def main() -> None:
    company = Company("Моя компания")

    while True:
        print("\n--- Учет сотрудников компании ---")
        print("1. Добавить сотрудника")
        print("2. Показать всех сотрудников")
        print("3. Найти сотрудника")
        print("4. Изменить сотрудника")
        print("5. Удалить сотрудника")
        print("6. Сохранить в JSON")
        print("7. Загрузить из JSON")
        print("8. Сохранить в XML")
        print("9. Загрузить из XML")
        print("0. Выход")

        try:
            choice = input("Выберите действие: ")

            if choice == "1":
                employee_id = int(input("ID сотрудника: "))
                full_name = input("ФИО: ")
                position_name = input("Должность: ")
                salary = float(input("Зарплата: "))
                department_name = input("Отдел: ")

                if not full_name.strip():
                    raise ValueError("ФИО не может быть пустым.")

                if salary < 0:
                    raise ValueError("Зарплата не может быть отрицательной.")

                employee = Employee(
                    employee_id,
                    full_name,
                    Position(position_name, salary),
                    Department(department_name)
                )

                company.add_employee(employee)
                print("Сотрудник добавлен.")

            elif choice == "2":
                company.show_employees()

            elif choice == "3":
                employee_id = int(input("Введите ID: "))
                company.get_employee(employee_id).show_info()

            elif choice == "4":
                employee_id = int(input("Введите ID сотрудника: "))
                full_name = input("Новое ФИО: ")
                position_name = input("Новая должность: ")
                salary = float(input("Новая зарплата: "))
                department_name = input("Новый отдел: ")

                if not full_name.strip() or salary < 0:
                    raise ValueError("Проверьте введенные данные.")

                company.update_employee(
                    employee_id,
                    full_name,
                    Position(position_name, salary),
                    Department(department_name)
                )
                print("Данные изменены.")

            elif choice == "5":
                employee_id = int(input("Введите ID: "))
                company.delete_employee(employee_id)
                print("Сотрудник удален.")

            elif choice == "6":
                EmployeeFile.save_json(company, "employees.json")
                print("Данные сохранены в JSON.")

            elif choice == "7":
                EmployeeFile.load_json(company, "employees.json")
                print("Данные загружены из JSON.")

            elif choice == "8":
                EmployeeFile.save_xml(company, "employees.xml")
                print("Данные сохранены в XML.")

            elif choice == "9":
                EmployeeFile.load_xml(company, "employees.xml")
                print("Данные загружены из XML.")

            elif choice == "0":
                break

            else:
                print("Неизвестная команда.")

        except ValueError as error:
            print(f"Ошибка: {error}")
        except FileNotFoundError:
            print("Файл не найден. Сначала сохраните данные.")
        except (json.JSONDecodeError, ET.ParseError):
            print("Ошибка чтения файла: неверный формат данных.")
        except OSError as error:
            print(f"Ошибка работы с файлом: {error}")


if __name__ == "__main__":
    main()
