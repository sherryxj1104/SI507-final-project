import requests
import json

yes_answer = ["yes","yeah","sure","yup","y"]

init_q = input(f"Do you want to search restaurant or hotel? ")


def getYelpData():
    location = str(input('Please enter a city you want to search: '))
    API_KEY = "zyOfVdA0Glovp6wWPDtJr-hKX2QlQck__SmZuf0ZHS8CV7ZK2l1VuHWtaOUnbiesxTFfdh8a7mOr4r5dVDJ4_xo0WH3N4mLxXUUzU08n7ePXQa6ohFXEi3x-ETU5YnYx"
    baseurl = "https://api.yelp.com/v3/businesses/search?location=" + location
    # baseurl = "https://api.yelp.com/v3/businesses/search?location=Seattle"
    header = {'authorization': "Bearer " + API_KEY}
    resp = requests.get(baseurl, headers=header)
    result = resp.json()
    # print(result['businesses'])
    return result['businesses']

yelp_data = getYelpData()

def booking():
	"""
	This is a function for booking API call. There are two steps. First, it will search for the 'dest_i' based on user input.
	Then, it will ask user several question in order to refine the results.
	"""
	user_input = str(input('Please enter a city you want to search: '))
	checkin_date = input(f"what is your check-in date? (format as YYYY-MM-DD)")
	checkout_date = input(f"what is your check-out date? (format as YYYY-MM-DD)")
	adults_number = input(f'How many adults?')
	room_number = input(f"How many rooms do do you need?")

	booking_loc_url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
	hotel_url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
	

	loc_querystring = {"locale":"en-gb","name":user_input}

	headers = {
		"X-RapidAPI-Host": "booking-com.p.rapidapi.com",
		"X-RapidAPI-Key": "7896e64febmshb2158348a449728p17a20fjsne76dbcac9593"
	}

	response = requests.request("GET", booking_loc_url, headers=headers, params=loc_querystring)
	result = response.json()

	# print(result[0]['dest_id'])

	# querystring = {"checkout_date":checkout_date,"units":"metric","dest_id":result[0]['dest_id'],"dest_type":"city","locale":"en-gb","adults_number":str(adults_number),"order_by":"popularity","filter_by_currency":"USD","checkin_date":checkin_date,"room_number":str(room_number)}
	querystring = {"checkout_date":checkout_date,"units":"metric","dest_id":result[0]['dest_id'],"dest_type":"city","locale":"en-gb","adults_number":adults_number,"order_by":"popularity","filter_by_currency":"USD","checkin_date":checkin_date,"room_number":room_number}
	headers = {
		"X-RapidAPI-Host": "booking-com.p.rapidapi.com",
		"X-RapidAPI-Key": "7896e64febmshb2158348a449728p17a20fjsne76dbcac9593"
	}
	response = requests.request("GET", hotel_url, headers=headers, params=querystring)
	hotel_result = response.json()
	hotel_index=0
	# print(hotel_result)
	for hotels in hotel_result['result']:
		print(hotel_index, ". ",hotels['hotel_name'])
		hotel_index +=1


def makeHotel(para):
    global price_id_list
    index = 0
    price_id_list = price_dict[price_key]
    for id in price_id_list:
        print(index,". ",business_dict[id]['name'])
        index += 1

business_dict = {}
for business in yelp_data:
    business_dict[business['id']] = business

price_dict ={
    "$":[],
    "$$":[],
    "$$$":[],
    "$$$$":[]
}
# count = 0

for business in yelp_data:
    try:
        if business['price'] == "$":
            price_dict['$'].append(business['id'])
        elif business['price'] == "$$":
            price_dict['$$'].append(business['id'])
        elif business['price'] == "$$$":
            price_dict['$$$'].append(business['id'])
        elif business['price'] == "$$$$":
            price_dict['$$$$'].append(business['id'])
    except:
        # count+=1
        print(f"Price cannot found in this business id: {business['id']}")
# print(count)
# print(price_dict)


def yes(prompt):

    user_input = input(prompt)
    if user_input.lower() in yes_answer:
        return True
    else:
        return False

price_tree = \
("30",
    ("10",
        ("$", None, None),
        ("$$", None, None)),
    ("60",
        ("$$$", None, None),
        ("$$$$", None, None)
    ))

def play(tree):
    node = tree[0]
    left = tree[1]
    right = tree[2]
    if type(node) is str and left is None and right is None:
        # ask = (f'Is it {node}? ')
        # if yes(ask) is True:
        # print(node)
        return node
            # return tree
    else:
        price_q = f'Is your expected price lower than ${node}?'
        if yes(price_q) is True:
            # return (node, play(left), right)
            return play(left)
        else:
            # return (node, left, play(right))
            return play(right)

# price_key = play(price_tree)
# print(price_key)

def makePrice(para):
    global price_id_list
    index = 0
    price_id_list = price_dict[price_key]
    for id in price_id_list:
        print(index,". ",business_dict[id]['name'])
        index += 1

def furtherInfo():
    fur_input = input(f'Which one do you want to check further info? (type number or bye) ')
    if fur_input.lower() == "bye":
        print("See you next time!")
    else:
        company = business_dict[price_id_list[int(fur_input)]]
        # print(company)
        print("Name: ",company['name'])
        print("Is closed: ",company['is_closed'])
        print("Rating: ",company['rating'])
        print("Address: ", company['location']['display_address'])
        print("Phone: ",company['display_phone'])


if init_q == "restaurant":
    price_key = play(price_tree)
    makePrice(price_key)
    furtherInfo()
    again = input(f"Do you want to have another search? Hotel or restaurant? ")
    if again == "hotel":
        booking()
    elif again == "restaurant":
        price_key = play(price_tree)
        makePrice(price_key)
        furtherInfo()
elif init_q == "hotel" or again == "hotel":
    booking()
    again = input(f"Do you want to have another search? Hotel or restaurant? ")
    if again == "hotel":
        booking()
    elif again == "restaurant":
        price_key_again = play(price_tree)
        makePrice(price_key_again)
        furtherInfo()




