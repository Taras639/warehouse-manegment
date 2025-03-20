from tabulate import tabulate




class Product:
   """Клас, що представляє продукт з основними атрибутами."""

   def __init__(self, name, cost, quantity, producer):
       self.name = name
       self.cost = cost
       self.quantity = quantity
       self.producer = producer




class FoodProduct(Product):
   """Клас, що представляє харчовий продукт, з додатковим атрибутом для дати терміну придатності."""

   def __init__(self, name, cost, quantity, producer, expiry_date):
       super().__init__(name, cost, quantity, producer)
       self.expiry_date = expiry_date


   def decrease_cost(self):
       """Метод для зменшення вартості продукту, якщо термін придатності майже закінчився."""
       # Перевіряємо, чи термін придатності майже закінчився (менше ніж 20% залишилося)
       if self.expiry_date <= 0.2:
           self.cost *= 0.9  # Зменшуємо вартість на 10%




class NonFoodProduct(Product):
   """Клас, що представляє непродовольчий продукт, з додатковими атрибутами для розмірів і призначення."""


   def __init__(self, name, cost, quantity, producer, dimensions, purpose):
       super().__init__(name, cost, quantity, producer)
       self.dimensions = dimensions
       self.purpose = purpose


   def decrease_cost(self):
       """Метод для збільшення вартості продукту, якщо його розміри перевищують 100 см."""
       # Перевірка перевищення розмірів
       if self.dimensions > 100:
           self.cost *= 1.1  # Додаємо 10% надбавки




class Warehouse:
   """Клас для управління складом та продуктами."""


   def __init__(self):
       self.products = []


   def show_product_groups(self):
       """Відображає групи харчових та непродовольчих продуктів на складі."""
       # Розподіл продуктів за категоріями
       food_products = [product for product in self.products if isinstance(product, FoodProduct)]
       non_food_products = [product for product in self.products if isinstance(product, NonFoodProduct)]


       # Відображення харчових продуктів
       print("Food Products:")
       print(tabulate(
           [(product.name, product.cost, product.quantity, product.producer, product.expiry_date) for product in
            food_products],
           headers=["Name", "Cost ($)", "Quantity", "Producer", "Expiry Date"]))


       # Відображення непродовольчих продуктів
       print("\nNon-Food Products:")
       print(tabulate(
           [(product.name, product.cost, product.quantity, product.producer, product.dimensions, product.purpose) for
            product in non_food_products],
           headers=["Name", "Cost ($)", "Quantity", "Producer", "Dimensions (cm)", "Purpose"]))


       print()  # Виводимо порожній рядок для розділення


   def load_products_from_file(self, file_path):
       """Завантажує продукти зі вказаного файлу."""
       try:
           with open(file_path, 'r', encoding='utf-8') as file:
               lines = file.readlines()


           # Фільтрація порожніх рядків та коментарів
           valid_lines = [line.strip() for line in lines if line.strip() and not line.startswith('#')]


           for line in valid_lines:
               data = line.split(',')
               if len(data) == 5:  # Харчові продукти
                   name, cost, quantity, producer, expiry_date = data
                   product = FoodProduct(name, float(cost), int(quantity), producer, int(expiry_date))
               elif len(data) == 6:  # Непродовольчі продукти
                   name, cost, quantity, producer, dimensions, purpose = data
                   product = NonFoodProduct(name, float(cost), int(quantity), producer, float(dimensions), purpose)
               else:
                   print(f"Invalid data format: {data}")  # Невірний формат даних
                   continue


               self.products.append(product)


           print("Products loaded from file.")
       except FileNotFoundError:
           print("File not found.")
       except Exception as e:
           print(f"Error loading products from file: {e}")


   def sort_products(self):
       """Сортує продукти на складі за кількістю."""
       # Запитуємо користувача, чи сортувати за зростанням чи спаданням
       order = input("Enter sorting order (asc/desc): ").lower()


       if order not in ["asc", "desc"]:
           print("Invalid sorting order. Please enter 'asc' for ascending or 'desc' for descending.")
           return


       # Сортування харчових продуктів
       food_products = [product for product in self.products if isinstance(product, FoodProduct)]
       food_products_sorted = sorted(food_products, key=lambda x: x.quantity, reverse=(order == "desc"))


       # Сортування непродовольчих продуктів
       non_food_products = [product for product in self.products if isinstance(product, NonFoodProduct)]
       non_food_products_sorted = sorted(non_food_products, key=lambda x: x.quantity, reverse=(order == "desc"))


       # Оновлюємо список продуктів у складі
       self.products = food_products_sorted + non_food_products_sorted


       print(f"Products sorted in {order}ending order based on quantity.")


   def add_product(self):
       """Додає новий продукт до складу."""
       # Запитуємо ім'я продукту
       name = self.get_valid_input("Enter product name: ", str, invalid_chars="#@!",
                                   invalid_chars_msg="Invalid product name. Product name must contain letters and must not include #, @, or !, and cannot consist solely of numbers.")


       # Запитуємо вартість продукту
       cost = self.get_valid_input("Enter product cost: ", float, invalid_range=(0, 2_000_000),
                                   invalid_range_msg="Invalid cost. Cost must be between 0 and 2,000,000.")


       # Запитуємо кількість продукту
       quantity = self.get_valid_input("Enter product quantity: ", int, invalid_range=(0, 50_000),
                                       invalid_range_msg="Invalid quantity. Quantity must be between 0 and 50,000.")


       # Запитуємо ім'я виробника
       producer = self.get_valid_input("Enter product producer: ", str, invalid_chars="#@!",
                                       invalid_chars_msg="Invalid producer name. Producer name must contain letters and must not include #, @, or !, and cannot consist solely of numbers.")


       # Запитуємо, чи є це харчовий продукт
       is_food = self.get_valid_input("Is it a food product? (yes/no): ", str, valid_responses=["yes", "no"],
                                      invalid_response_msg="Invalid input. Please enter 'yes' or 'no'.")


       if is_food == "yes":
           # Запитуємо термін придатності
           expiry_date = self.get_valid_input("Enter expiry date (in days): ", int, invalid_range=(0, None),
                                              invalid_range_msg="Invalid expiry date. Expiry date must be a positive integer.")
           # Додаємо харчовий продукт
           product = FoodProduct(name, cost, quantity, producer, expiry_date)
       else:
           # Запитуємо розміри продукту
           dimensions = self.get_valid_input("Enter product dimensions: ", float, invalid_range=(0, 1000),
                                             invalid_range_msg="Invalid dimensions. Dimensions must be between 0 and 1000.")


           # Запитуємо призначення продукту
           purpose = self.get_valid_input("Enter product purpose: ", str,
                                          invalid_msg="Invalid purpose. Purpose must start with a letter and must not consist solely of numbers.")


           # Додаємо непродовольчий продукт
           product = NonFoodProduct(name, cost, quantity, producer, dimensions, purpose)


       # Додаємо продукт до списку продуктів
       self.products.append(product)
       print(f"Product '{product.name}' added to warehouse.")


   def remove_product(self):
       """Видаляє продукт зі складу за назвою."""
       product_name = input("Enter product name to remove: ")
       product_to_remove = next((product for product in self.products if product.name == product_name), None)


       if product_to_remove:
           self.products.remove(product_to_remove)
           print(f"Product '{product_name}' removed from warehouse.")
       else:
           print(f"Product '{product_name}' not found in warehouse.")


   def find_product_by_name(self):
       """Знаходить продукт за назвою та відображає його деталі."""
       product_name = input("Enter product name to find: ")
       found_products = [product for product in self.products if product.name == product_name]


       if not found_products:
           print(f"Product '{product_name}' not found.")
       else:
           for product in found_products:
               if isinstance(product, FoodProduct):
                   print(
                       f"Name: {product.name}, Cost: {product.cost}, Quantity: {product.quantity}, Producer: {product.producer}, Expiry Date: {product.expiry_date}")
               elif isinstance(product, NonFoodProduct):
                   print(
                       f"Name: {product.name}, Cost: {product.cost}, Quantity: {product.quantity}, Producer: {product.producer}, Dimensions: {product.dimensions}, Purpose: {product.purpose}")


   def update_product(self):
       """Оновлює інформацію про продукт у складі."""
       product_name = input("Enter product name to update: ")
       product_to_update = next((product for product in self.products if product.name == product_name), None)


       if not product_to_update:
           print(f"Product '{product_name}' not found.")
           return


       print(f"Updating product: {product_name}")


       # Оновлення вартості
       new_cost = self.get_valid_input("Enter new cost (leave blank to keep current cost): ", float,
                                       default=product_to_update.cost, invalid_range=(0, 2_000_000),
                                       invalid_range_msg="Invalid cost. Cost must be between 0 and 2,000,000.")
       product_to_update.cost = new_cost


       # Оновлення кількості
       new_quantity = self.get_valid_input("Enter new quantity (leave blank to keep current quantity): ", int,
                                           default=product_to_update.quantity, invalid_range=(0, 50_000),
                                           invalid_range_msg="Invalid quantity. Quantity must be between 0 and 50,000.")
       product_to_update.quantity = new_quantity


       print(f"Product '{product_name}' updated successfully.")


   def get_valid_input(self, prompt, dtype, invalid_chars=None, invalid_chars_msg=None, invalid_range=None,
                       invalid_range_msg=None, valid_responses=None, invalid_response_msg=None, invalid_msg=None,
                       default=None):
       """Універсальний метод для отримання та перевірки введення від користувача."""
       while True:
           value = input(prompt)
           if not value and default is not None:
               return default


           try:
               if dtype == int:
                   value = int(value)
               elif dtype == float:
                   value = float(value)
               elif dtype == str:
                   pass


               # Перевірка наявності невідповідних символів
               if invalid_chars and any(char in value for char in invalid_chars):
                   print(invalid_chars_msg)
                   continue


               # Перевірка діапазону
               if invalid_range:
                   lower, upper = invalid_range
                   if (lower is not None and value < lower) or (upper is not None and value > upper):
                       print(invalid_range_msg)
                       continue


               # Перевірка списку допустимих відповідей
               if valid_responses and value.lower() not in valid_responses:
                   print(invalid_response_msg)
                   continue


               return value


           except ValueError:
               print(invalid_msg)


   def change_quantity_of_product(self):
       """Змінює кількість продукту на складі."""
       product_name = input("Enter product name to change quantity: ")
       product_to_change = next((product for product in self.products if product.name == product_name), None)


       if not product_to_change:
           print(f"Product '{product_name}' not found in warehouse.")
           return


       print(f"\nProduct '{product_name}' details:")
       print(tabulate([[product_to_change.name, product_to_change.cost, product_to_change.quantity,
                        product_to_change.producer, product_to_change.dimensions, product_to_change.purpose]],
                      headers=["Name", "Cost ($)", "Quantity", "Producer", "Dimensions (cm)", "Purpose"]))


       change_amount = self.get_valid_input("Enter quantity change (positive for increase, negative for decrease): ",
                                            int, invalid_msg="Invalid quantity change. Please enter a valid integer.")
       product_to_change.quantity += change_amount
       print(f"Quantity of '{product_name}' changed by {change_amount}.")


   def take_product_from_warehouse(self):
       """Бере певну кількість продуктів зі складу."""
       product_name = input("Enter product name taken from warehouse: ")
       product_to_take = next((product for product in self.products if product.name == product_name), None)


       if not product_to_take:
           print(f"Product '{product_name}' not found in warehouse.")
           return


       print(f"\nProduct '{product_name}' details:")
       print(tabulate([[product_to_take.name, product_to_take.cost, product_to_take.quantity, product_to_take.producer,
                        product_to_take.dimensions, product_to_take.purpose]],
                      headers=["Name", "Cost ($)", "Quantity", "Producer", "Dimensions (cm)", "Purpose"]))


       taken_quantity = self.get_valid_input(
           f"Enter quantity taken from warehouse (up to {product_to_take.quantity}): ", int,
           invalid_range=(1, product_to_take.quantity),
           invalid_range_msg=f"Invalid quantity. Please enter a number between 1 and {product_to_take.quantity}.")
       product_to_take.quantity -= taken_quantity
       print(f"{taken_quantity} units of '{product_name}' taken from warehouse.")


   def get_total_quantity_of_product(self):
       """Показує загальну кількість певного продукту на складі."""
       product_name = input("Enter product name to get total quantity: ")
       total_quantity = sum(product.quantity for product in self.products if product.name == product_name)
       print(f"Total quantity of '{product_name}' in warehouse: {total_quantity}")


def choose_language():
       """Функція, що дозволяє користувачу вибрати мову інтерфейсу."""
       print("Choose language / Виберіть мову:")
       print("1. English")
       print("2. Українська")


       choice = input("Enter your choice / Введіть свій вибір (1-2): ")


       if choice == "1":
           return "en"
       elif choice == "2":
           return "ua"
       else:
           print("Invalid choice / Невірний вибір.")
           return choose_language()
translations = {
   "en": {
       "menu": {
           "header": "~~~ Warehouse Management System ~~~",
           "load_from_file": "Load products from file",
           "show_groups": "Show product groups",
           "add_product": "Add new product",
           "remove_product": "Remove product",
           "find_product": "Find product by name",
           "update_product": "Update product",
           "sort_products": "Sort products",
           "exit": "Exit"
       },
       "invalid_choice": "Invalid choice. Please enter a number between 1 and 8.",
       "prompt": {
           "file_path": "Enter file path: ",
           "product_name": "Enter product name: ",
           "product_cost": "Enter product cost: ",
           "product_quantity": "Enter product quantity: ",
           "product_producer": "Enter product producer: ",
           "is_food_product": "Is it a food product? (yes/no): ",
           "expiry_date": "Enter expiry date (in days): ",
           "product_dimensions": "Enter product dimensions: ",
           "product_purpose": "Enter product purpose: ",
           "change_amount": "Enter quantity change (positive for increase, negative for decrease): ",
           "taken_quantity": "Enter quantity taken from warehouse: "
       }
   },
   "ua": {
       "menu": {
           "header": "~~~ Система управління складом ~~~",
           "load_from_file": "Завантажити продукти з файлу",
           "show_groups": "Показати групи продуктів",
           "add_product": "Додати новий продукт",
           "remove_product": "Видалити продукт",
           "find_product": "Знайти продукт за назвою",
           "update_product": "Оновити продукт",
           "sort_products": "Сортувати продукти",
           "exit": "Вийти"
       },
       "invalid_choice": "Невірний вибір. Будь ласка, введіть число від 1 до 8.",
       "prompt": {
           "file_path": "Введіть шлях до файлу: ",
           "product_name": "Введіть назву продукту: ",
           "product_cost": "Введіть вартість продукту: ",
           "product_quantity": "Введіть кількість продукту: ",
           "product_producer": "Введіть назву виробника продукту: ",
           "is_food_product": "Це харчовий продукт? (так/ні): ",
           "expiry_date": "Введіть термін придатності (в днях): ",
           "product_dimensions": "Введіть розміри продукту: ",
           "product_purpose": "Введіть призначення продукту: ",
           "change_amount": "Введіть зміни в кількості (позитивне для збільшення, негативне для зменшення): ",
           "taken_quantity": "Введіть кількість, взяту зі складу: "
       }
   }
}




def main():
   """Основна функція, яка запускає інтерфейс програми."""
   # Створення об'єкту складу
   warehouse = Warehouse()


   # Вибір мови
   language = choose_language()
   translation = translations[language]


   while True:
       # Виведення меню для користувача
       print("------------------------------------------------------------------")
       print("\t\t\t", translation["menu"]["header"], "\t\n")
       print("\t 1.", translation["menu"]["load_from_file"])
       print("\t 2.", translation["menu"]["show_groups"])
       print("\t 3.", translation["menu"]["add_product"])
       print("\t 4.", translation["menu"]["remove_product"])
       print("\t 5.", translation["menu"]["find_product"])
       print("\t 6.", translation["menu"]["update_product"])
       print("\t 7.", translation["menu"]["sort_products"])
       print("\t 8.", translation["menu"]["exit"])


       # Отримання вибору користувача
       choice = input("\n" + translation["invalid_choice"])


       # Обробка вибору користувача
       if choice == "1":
           # Завантаження продуктів з файлу
           file_path = input(translation["prompt"]["file_path"])
           warehouse.load_products_from_file(file_path)
       elif choice == "2":
           # Відображення груп продуктів
           warehouse.show_product_groups()
       elif choice == "3":
           # Додавання нового продукту
           warehouse.add_product()
       elif choice == "4":
           # Видалення продукту
           warehouse.remove_product()
       elif choice == "5":
           # Пошук продукту за назвою
           warehouse.find_product_by_name()
       elif choice == "6":
           # Оновлення продукту
           warehouse.update_product()
       elif choice == "7":
           # Сортування продуктів
           warehouse.sort_products()
       elif choice == "8":
           # Вихід з програми
           print(translation["menu"]["exit"])
           break
       else:
           # Невірний вибір
           print(translation["invalid_choice"])




if __name__ == "__main__":
   main()
