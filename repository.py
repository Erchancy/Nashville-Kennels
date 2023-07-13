
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
