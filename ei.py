from abc import ABC, abstractmethod
from copy import deepcopy

class Product(ABC):            
    def __init__(self, name, price, available=True):
        self.name = name
        self.price = price
        self.available = available

    @abstractmethod
    def calculate_discount(self, quantity):
        pass

    def clone(self):
        return deepcopy(self)

    def __str__(self):
        return f"{self.name} - Price: ${self.price}{' (Out of stock)' if not self.available else ''}"

class Laptop(Product):
    def calculate_discount(self, quantity):
        return 0  

class Headphones(Product):
    def calculate_discount(self, quantity):
        return self.price * 0.1 if quantity >= 2 else 0


class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, product, quantity):
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, product, quantity):
        return product.price * self.percentage / 100 * quantity

class BuyOneGetOneFree(DiscountStrategy):
    def apply_discount(self, product, quantity):
        return (quantity // 2) * product.price

# Cart class
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity):
        if product.available:
            if product.name in self.items:
                self.items[product.name]["quantity"] += quantity
            else:
                self.items[product.name] = {"product": product, "quantity": quantity}

    def update_quantity(self, product_name, new_quantity):
        if product_name in self.items:
            self.items[product_name]["quantity"] = new_quantity

    def remove_item(self, product_name):
        if product_name in self.items:
            del self.items[product_name]

    def calculate_total(self, discount_strategy=None):
        total = 0
        for item in self.items.values():
            product = item["product"]
            quantity = item["quantity"]
            discount = 0
            if discount_strategy:
                discount = discount_strategy.apply_discount(product, quantity)
            total += (product.price * quantity - discount)
        return total

    def clone(self):
        new_cart = ShoppingCart()
        new_cart.items = deepcopy(self.items)
        return new_cart

    def __str__(self):
        cart_items = [f"{item['quantity']} {item['product'].name}" for item in self.items.values()]
        return f"Cart Items: {' and '.join(cart_items)} in your cart."

def main():
    laptop = Laptop("Laptop", 1000)
    headphones = Headphones("Headphones", 50)

    cart = ShoppingCart()
    
    while True:
        print("\nAvailable Products:")
        print(laptop)
        print(headphones)

        user_input = input("Enter a command (add to cart/update quantity/remove from cart/check_bill/exit): ").strip().lower()

        if user_input == "add to cart":
            product_name = input("Enter the product name to add: ").strip()
            quantity = int(input("Enter the quantity: "))
            if product_name.lower() == "laptop":
                product = laptop.clone()
            elif product_name.lower() == "headphones":
                product = headphones.clone()
            else:
                print("Invalid product name.")
                continue
            cart.add_item(product, quantity)
        elif user_input == "update quantity":
            product_name = input("Enter the product name to update: ").strip()
            new_quantity = int(input("Enter the new quantity: "))
            cart.update_quantity(product_name, new_quantity)
        elif user_input == "remove from cart":
            product_name = input("Enter the product name to remove: ").strip()
            cart.remove_item(product_name)
        elif user_input == "check_bill":
            print(cart)
            print(f"Total Bill: Your total bill is ${cart.calculate_total():.2f}.")
        elif user_input == "exit":
            break
        else:
            print("Invalid command. Please enter a valid command.")

if __name__ == "__main__":
    main()
