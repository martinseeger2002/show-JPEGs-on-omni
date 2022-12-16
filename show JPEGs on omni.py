import base64
from PIL import Image
from bitcoinrpc.authproxy import AuthServiceProxy

# Set rpc_user and rpc_password in the litecoin.conf file
rpc_user = 'YOUR_RPC_USERNAME'
rpc_password = 'YOUR_RPC_PASSWORD'

# Connect to Bitcoin daemon
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:9332"%(rpc_user, rpc_password))

# Get list of Omni Layer token properties
data = rpc_connection.omni_listproperties()

# Create a set to store the names that have already been printed
printed_names = set()

# Loop through the properties and print the property ID and name
for prop in data:  
    # Check if the length of the data field is 255
    if len(str(prop['data'])) == 255:
        # Remove the last 5 characters from the name
        name = prop['name'][:-5]
        
        # Check if the name is in the set of printed names
        if name not in printed_names:
            # Check if "JPEG" is in the name
            if "JPEG" in name:

                # Add the name to the set of printed names
                printed_names.add(name)

# list names of properties avalable
print(printed_names)

# Filter list for user-defined property name and add property data to dictionary
user_def_name = input('Enter prop name:\n')
token_dict = {}
for prop in data:
    if prop['name'][:-5] == user_def_name:
        num = prop['name'][-5:]
        d1 = prop['category']
        d2 = prop['subcategory']
        d3 = prop['url']
        d4 = prop['data']
        
        # Add property data to dictionary, handling cases where data is longer than 255 characters
        if len(d1) == 255:
            token_dict[num+'d1'] = d1
        if len(d1) >= 1 and d1[-1] == '=':
            token_dict[num+'d1'] = d1
        if len(d1) >= 2 and d1[-2] == '=':
            token_dict[num+'d1'] = d1

        if len(d2) == 255:
            token_dict[num+'d2'] = d2
        if len(d2) >= 1 and d2[-1] == '=':
            token_dict[num+'d2'] = d2
        if len(d2) >= 2 and d2[-2] == '=':
            token_dict[num+'d2'] = d2

        if len(d3) == 255:
            token_dict[num+'d3'] = d3
        if len(d3) >= 1 and d3[-1] == '=':
            token_dict[num+'d3'] = d3
        if len(d3) >= 2 and d3[-2] == '=':
            token_dict[num+'d3'] = d3

        if len(d4) == 255:
            token_dict[num+'d4'] = d4
        if len(d4) >= 1 and d4[-1] == '=':
            token_dict[num+'d4'] = d4
        if len(d4) >= 2 and d4[-2] == '=':
            token_dict[num+'d4'] = d4

# Sort dictionary by keys and concatenate values
sorted_token = dict(sorted(token_dict.items()))
data = ''.join(sorted_token.values())

# Decode base64 encoded data and write to file
decodeit = open('out.jpeg', 'wb')
decodeit.write(base64.b64decode(data))
decodeit.close()

# Open image file and display using PIL
im = Image.open('out.jpeg')
im.show()

