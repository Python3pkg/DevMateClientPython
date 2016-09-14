# DevMateClientPython

This is a simple [DevMate](http://devmate.com/) [Public API](https://docs.devmate.com/docs/api) client written in Python.

* [Getting Started](#getting-started)
* [Usage Example](#usage-example)

## Getting Started
TODO

## Usage Example

```python
# DevMate public API token
# You can generate it in Settings -> API Integration
token = '1234567890abcdef'

# Initialize client with token
dm_client = devmateclient.Client(auth_token=token)

# You still have an access to the token
old_token = dm_client.auth_token

# Or you can change it in runtime
dm_client.auth_token = '0987654321abcdef'

# Get single customer by ID
customer = dm_client.get_customer_by_id(123)

# Create new customer in DevMate (email is required)
customer_details = {
    'email': 'some@email.com',
    'first_name': 'Dead',
    'last_name': 'Beef'
}
created_customer = dm_client.create_customer(customer_details)

# Update existing customer in DevMate (id is required)
customer_update_details = dict(created_customer)
customer_update_details['company'] = 'Some Company'
updated_customer = dm_client.update_customer(customer_update_details)

# Create new license for customer (license_type_id is required)
new_license = dm_client.create_license_for_customer(
    customer_id=123, 
    _license={'license_type_id': 1}
)
# Now you can get created license info, e.g. activation key
activation_key = new_license['activation_key']

# Get list of customers with filter parameters and additional meta data (returns tuple)
# Don't set with_meta to return only customers
customers, meta = dm_client.get_customers(with_email='some@e',
                                          with_key=activation_key,
                                          with_limit=20,
                                          with_licenses=True,
                                          with_meta=True)

# Reset first activation by activation key
dm_client.reset_first_activation(activation_key)

# Close the DevMate client
dm_client.close()
```