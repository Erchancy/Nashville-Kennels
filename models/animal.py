class Animal():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, name, breed, status, location_id, customer_id):
        self.id = id
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id

new_animal = Animal(1, "Snickers", "Dog", "Recreation", 1, 4)
new_animal2 = Animal(2, "Roman", "Dog", "Admitted", 1, 2)
new_animal3 = Animal(3, "Blue", "Cat", "Admitted", 2, 1)