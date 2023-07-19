import sqlite3
import json
from models import Animal, Customer, Employee, Location

DATABASE = {
    "animals": [
        {
            "id": 1,
            "name": "Snickers",
            "species": "Dog",
            "locationId": 1,
            "customerId": 4,
            "status": "Admitted"
        },
        {
            "id": 2,
            "name": "Roman",
            "species": "Dog",
            "locationId": 1,
            "customerId": 2,
            "status": "Admitted"
        },
        {
            "id": 3,
            "name": "Blue",
            "species": "Cat",
            "locationId": 2,
            "customerId": 1,
            "status": "Admitted"
        }
    ],
    "locations": [
        {
            "id": 1,
            "name": "Nashville North",
            "address": "8422 Johnson Pike"
        },
        {
            "id": 2,
            "name": "Nashville South",
            "address": "209 Emory Drive"
        }
    ],
    "customers": [
        {
            "id": 1,
            "email": "jjd@funny.com",
            "fullName": "Jonathan VanDuyne"
        },
        {
            "id": 2,
            "email": "belle@belle.com",
            "fullName": "Belle Hollander"
        },
        {
            "id": 3,
            "email": "chesney@fakename.com",
            "fullName": "Chesney Hardin"
        }
    ],
    "employees": [
        {
            "id": 1,
            "name": "Jenna Solis",
            "locationId": 1
        },
        {
            "id": 2,
            "name": "Daniel Myers",
            "locationId": 2
        }
    ]
}


def all(resource):
    """For GET requests to collection"""
    return DATABASE[resource]


def retrieve(resource, id):
    """For GET requests to a single resource"""
    # Variable to hold the found animal, if it exists
    requested_resource = None

    resource_list = DATABASE[resource]

    for single_resource in resource_list:
        if single_resource["id"] == id:
            requested_resource = single_resource

    return requested_resource


def create(resource, post_body):
    """For POST requests to a collection"""
    resource_list = DATABASE[resource]

    max_id = resource_list[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the dictionary
    post_body["id"] = new_id

    # Add the new resource dictionary to the list
    resource_list.append(post_body)

    # Return the dictionary with `id` property added
    return post_body


def update(id, resource, post_body):
    """For PUT requests to a single resource"""
    # Iterate the nested list, but use enumerate() so that
    # you can access the index value of each item.
    resource_list = DATABASE[resource]

    for index, single_resource in enumerate(resource_list):
        if single_resource["id"] == id:
            # Found the single_resource. Update the value.
            resource_list[index] = post_body
            break


def delete(id, resource):
    """For DELETE requests to a single resource"""
    resource_list = DATABASE[resource]

    resource_index = -1

    # Iterate the nested list, but use enumerate() so that you
    # can access the index value of each item
    for index, single_resource in enumerate(resource_list):
        if single_resource["id"] == id:
            # Found the single_resource. Store the current index.
            resource_index = index

    # If the resource was found, use pop(int) to remove it from list
    if resource_index >= 0:
        resource_list.pop(resource_index)


def get_all_animals(resource):
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        if resource == "animals":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.email
            FROM Animal a
            JOIN Location l
                ON l.id = a.location_id
            JOIN Customer c
                ON c.id = a.customer_id
            """)

        elif resource == "customers":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.email,
                a.password
            FROM customer a
            """)

        elif resource == "employees":
            db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.address,
                e.location_id,
                l.name location_name,
                l.address location_address
            FROM Employee e
            JOIN Location l
                ON l.id = e.location_id
            """)

        elif resource == "locations":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address
            FROM location a
            """)

        # Initialize an empty list to hold all animal representations
        response = []
        animals = []
        employees = []
        customers = []
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            if resource == "animals":
                # Create an animal instance from the current row
                animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                                row['location_id'], row['customer_id'])

                # Create a Location instance from the current row
                location = Location(
                    row['id'], row['location_name'], row['location_address'])

                customer = Customer(
                    row['id'], row['customer_name'], row['email'])

                # Add the dictionary representation of the location to the animal
                animal.location = location.__dict__
                animal.customer = customer.__dict__

                # Add the dictionary representation of the animal to the list
                animals.append(animal.__dict__)

                response = animals

            if resource == "employees":
                employee = Employee(
                    row['id'], row['name'], row['address'], row['location_id'])

                # Create a Location instance from the current row
                location = Location(
                    row['id'], row['location_name'], row['location_address'])

                employee.location = location.__dict__

                employees.append(employee.__dict__)

                response = employees

            if resource == "customers":
                customer = Customer(
                    row['id'], row['name'], row['address'], row['email'], row['password'])
                
                customers.append(customer.__dict__)

                response = customers

            if resource == "locations":
                location = Location(
                    row['id'], row['name'], row['address'])
                
                locations.append(location.__dict__)

                response = locations

        return response


def get_single_animal(resource, id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # Write the SQL query to get the information you want
        if resource == "animals":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an animal instance from the current row
            resource_list = Animal(data['id'], data['name'], data['breed'],
                                   data['status'], data['location_id'],
                                   data['customer_id'])

        elif resource == "customers":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.email,
                a.password
            FROM customer a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Customer(data['id'], data['name'], data['address'],
                                     data['email'], data['password'])

        elif resource == "employees":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address,
                a.location_id
            FROM employee a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Employee(data['id'], data['name'], data['address'],
                                     data['location_id'])

        elif resource == "locations":
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.address
            FROM location a
            WHERE a.id = ?
            """, (id, ))

            # Load the single result into memory
            data = db_cursor.fetchone()

            # Create an resource_list instance from the current row
            resource_list = Location(data['id'], data['name'], data['address'])

        return resource_list.__dict__


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, (email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(
                row['id'], row['name'], row['address'], row['email'], row['password'])
            customers.append(customer.__dict__)

    return customers


def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        from employee e
        WHERE e.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees


def get_animals_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals


def get_animals_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, (status, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal
