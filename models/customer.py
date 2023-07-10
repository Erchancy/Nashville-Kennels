class Customer():

    # Class initializer. It has 3 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.full_name = name

new_customer = Customer(1, "jjd@funny.com", "Jonathan VanDuyne")