from dataclasses import dataclass, field

from abc import ABC, abstractmethod

from enum import Enum, auto

from typing import List

import re

class InvalidField(Exception):

    """InvalidFiled"""

class FailedPayment(Exception):

    """FailedPayment"""

def email_validator(email: str) -> bool:

    pattern = r"^\w+\w@((g|e)mail|icloud|marco).com"

    if not re.search(pattern, email):

        raise InvalidField("Email Invalid")

    return True

@dataclass(frozen=True)

class Address:

    city: str

    street: str

    no: int

@dataclass(frozen=True)

class User:

    name: str

    email: str

    address: Address

    def __post_init__(self) -> None:

        email_validator(self.email)

class Product(ABC):

    """ Product """

    @abstractmethod

    def total_price(self) -> int:

        """Calculate total price"""

class PaymentStatus(Enum):

    PENDING = auto()

    PAID = auto()

@dataclass(frozen=True)

class Item(Product):

    label: str

    quantity: int

    price: int

    def total_price(self) -> int:

        return self.quantity * self.price

@dataclass(frozen=False)

class Order(Product):

    user: User

    items: List[Item] = field(default_factory=list)

    _payment_status: PaymentStatus = field(default=PaymentStatus.PENDING)

    def total_price(self) -> int:

        return sum(item.total_price() for item in self.items)

    def log(self) -> None:

        print(f"Username: {self.user_name}", end="\n")

        print("| No\t| Item | Quantity\t| Price\t| Total\t|")

        for i, item in enumerate(self.items):

            print(f"| {i}\t| {item.label} | {item.quantity}\t\t| {item.price}\t| {item.total_price()}\t|")

        print(

            "",

            f"Total: {self.total_price()}",

            f"Payment Status: {self.get_payment_status()}",

            sep="\n"

        )

    @property

    def user_name(self) -> str:

        return self.user.name

    def get_payment_status(self) -> PaymentStatus:

        return self._payment_status

    def set_payment_status(self, status: PaymentStatus) -> None:

        if self._payment_status == PaymentStatus.PAID:

            raise FailedPayment("U can't change the status of an already paid order.")

        self._payment_status = status

def main() -> None:

    address = Address(city="New York", street="Broadway", no=69)

    me = User(name="Marco", email="aunglynn@marco.com", address=address)

    apple = Item(label="Apple", quantity=5, price=1_000)

    cherry = Item(label="Cherry", quantity=2, price=1_500)

    order = Order(user=me, items=[apple, cherry])

    order.set_payment_status(PaymentStatus.PAID)

    

    order.log()

if __name__ == "__main__":

    main()

