from bs4 import BeautifulSoup
from urllib import request
import ssl,csv,re,time

restaurants = []
restaurants.append([
    "restaurantID",
    "name",
    "location",
    "reviewCount",
    "rating", 
    "categories", 
    "address", 
    "Hours", 
    "GoodforKids", 
    "AcceptsCreditCards", 
    "Parking", 
    "Attire", 
    "GoodforGroups", 
    "PriceRange", 
    "TakesReservations", 
    "Delivery", 
    "Takeout", 
    "WaiterService", 
    "OutdoorSeating", 
    "WiFi", 
    "GoodFor",
    "Alcohol", 
    "NoiseLevel", 
    "Ambience", 
    "HasTV", 
    "Caters", 
    "WheelchairAccessible", 
    "webSite", 
    "phoneNumber"
])
reviews = []
reviews.append(
[
    "reviewID",
    "businessID",
    "reviewerID",
    "date",
    "reviewContent",
    "rating", 
    "usefulCount", 
    "coolCount", 
    "funnyCount"
]
)

authors = []
authors.append(
[
   "authorID", 
   "name", 
   "location", 
   "reviewCount", 
   "friendCount", 
   "photoCount"
]
)

zipcode = 60626
i = 0
while len(restaurants) < 101:
    page = i * 10
    i = i+1
    res = request.urlopen('https://www.yelp.com/search?find_loc='+str(zipcode)+'&cflt=restaurants', context=ssl.SSLContext(ssl.PROTOCOL_TLSv1) )
    soup = BeautifulSoup(res.read(), 'html.parser')
    divs = soup.findAll("div", {"class": "biz-listing-large"})
    for d in divs:
        print(len(restaurants))
        time.sleep(5)
        #-------------RESTAURANTS------------
        r = ["N/A"] * len(restaurants[0])
        restuarant = d.find("a", {"class": "biz-name"}) 
        response_restaurant = request.urlopen('https://www.yelp.com'+restuarant["href"], context=ssl.SSLContext(ssl.PROTOCOL_TLSv1) )        
        soup_restaurant = BeautifulSoup(response_restaurant.read(), 'html.parser')

        #RestaurantID
        restaurant_id = soup_restaurant.findAll("div", {"class": "lightbox-map"})
        if len(restaurant_id) > 0:
            r[0] = restaurant_id[0]["data-business-id"]
        name = soup_restaurant.findAll("h1", {"class": "biz-page-title"})

        #Address and Location
        if len(name) > 0:
            r[1] = name[0].text.strip()
        address = soup_restaurant.findChildren('address')
        if len(address) > 0:
            if str(zipcode) not in address[0].text.strip():
                continue
            parts = address[0].text.strip().split("Chicago")
            r[2] = r[6] = parts[0]+", Chicago"+parts[1]

        #Review Count
        review_count = soup_restaurant(attrs={"name":"description"})
        if len(review_count) > 0:
            parts = review_count[0]["content"].split(" ")
            if len(parts) > 0:
                r[3] = parts[0]
            if int(r[3]) < 20:
                continue

        #Rating
        ratings = soup_restaurant.findAll("div", {"class": "i-stars"})
        if len(ratings) > 0:
            parts = ratings[0]["title"].split(" ")
            if len(parts) > 0:
                r[4] = parts[0]

        #Categories
        categories = soup_restaurant.findAll("span", {"class": "category-str-list"})
        if len(categories) > 0:
            category_links = categories[0].findAll("a")
            for cl in range(0,len(category_links)):
                if cl > 0:
                    r[5] = r[5] + "|" + category_links[cl].text.strip()
                else:
                    r[5] = category_links[cl].text.strip()

        #Features(18)               
        features_section = soup_restaurant.findAll("div", {"class": "short-def-list"})
        if len(features_section) > 0:
            features = features_section[0].findAll("dl")
            for f in features:
                feature_key = f.findAll("dt")
                feature_value = f.findAll("dd")
                if len(feature_key) > 0 and len(feature_value) > 0:
                    key = feature_key[0].text.strip()
                    value = feature_value[0].text.strip()
                    if key == "Good for Kids":
                        r[8] = value
                    elif key == "Accepts Credit Cards":
                        r[9] = value
                    elif key == "Parking":
                        r[10] = value
                    elif key == "Attire":
                        r[11] = value
                    elif key == "Good for Groups":
                        r[12] = value
                    elif key == "Takes Reservations":
                        r[14] = value
                    elif key == "Delivery":
                        r[15] = value
                    elif key == "Take-out":
                        r[16] = value
                    elif key == "Waiter Service":
                        r[17] = value
                    elif key == "Outdoor Seating":
                        r[18] = value
                    elif key == "Wi-Fi":
                        r[19] = value
                    elif key == "Good For":
                        r[20] = value
                    elif key == "Alcohol":
                        r[21] = value
                    elif key == "Noise Level":
                        r[22] = value
                    elif key == "Ambience":
                        r[23] = value
                    elif key == "Has TV":
                        r[24] = value
                    elif key == "Caters":
                        r[25] = value
                    elif key == "Wheelchair Accessible":
                        r[26] = value
            

        #price range
        price_range = soup_restaurant.findAll("dd", {"class": "nowrap price-description"})
        if len(price_range) > 0:
            r[13] = price_range[0].text.strip()

        #website
        website = soup_restaurant.findAll("span", {"class": "biz-website"})
        if len(website) > 0:
            web_link = website[0].findAll("a")
            if len(web_link) > 0:
                r[27] = web_link[0].text.strip()

        #phone
        phone = soup_restaurant.findAll("span", {"class": "biz-phone"})
        if len(phone) > 0:
            r[28] = phone[0].text.strip()

        #hours
        hours_sec = soup_restaurant.findAll("table", {"class": "hours-table"}) 
        if len(hours_sec) > 0:
            hours = hours_sec[0].findAll("td") 
            for hi in range(0,len(hours)): 
                h = hours[hi].text.strip()
                if h != "" and h != "Open now":
                    if hi > 0:
                        r[7]= r[7] + "|" + h
                    else:
                        r[7]= h
        if r[0] != "N/A":
            restaurants.append(r)

        
        rev_sec = soup_restaurant.findAll("div", {"class": "review--with-sidebar"}) 
        for rs in rev_sec:

            #-------------REVIEWS-------------
            rv = ["N/A"] * len(reviews[0])
            rv[6] = rv[7] = rv[8] = 0
            if "data-review-id" not in rs.attrs:
                continue
            
            #reviewid
            rv[0] = rs["data-review-id"]
            rv[1] = r[0]
            
            #date
            date = rs.findAll("span", {"class": "rating-qualifier"}) 
            if len(date) > 0 :
                rv[3] = date[0].text.strip()
            
            #votes(3)
            features = rs.findAll("li", {"class": "vote-item"})
            for f in features:
                feature_key = f.findAll("span", {"class": "vote-type"})
                feature_value = f.findAll("span", {"class": "count"})
                if len(feature_key) > 0 and len(feature_value) > 0:
                    key = feature_key[0].text.strip()
                    value = feature_value[0].text.strip()
                    if value != "":
                        if key == "Funny":
                            rv[8] = value
                        elif key == "Cool":
                            rv[7] = value
                        elif key == "Useful":
                            rv[6] = value
            
            #review content and ratings(2)
            review_rating = rs.findAll("div", {"class": "i-stars"})
            if len(review_rating ) > 0:
                parts = review_rating[0]["title"].split(" ")
                if len(parts) > 0:
                    rv[5] = parts[0]
            review_content = rs.findAll("div", {"class": "review-content"})
            if len(review_content) > 0:
                review_msg = review_content[0].findAll("p")
                if len(review_msg) > 0:
                    rv[4] = review_msg[0].text.strip()
            reviews.append(rv)

            #-------------AUTHORS-------------
            a = ["N/A", "N/A", "N/A", 0,0,0]
            #name
            user_name = rs.findAll("a", {"class": "user-display-name"})
            if len(user_name) > 0:
                a[1] = user_name[0].text.strip()
                parts = user_name[0]["href"].split("=")
                if len(parts) > 0:
                    a[0] = parts[1] 
                    rv[2] = parts[1] 

            #location
            user_location = rs.findAll("li", {"class": "user-location"})
            if len(user_location) > 0 :
                loc = user_location[0].findAll("b")
                if len(loc) > 0:
                    a[2] = loc[0].text.strip()
            
            #friends
            friend_count = rs.findAll("li", {"class": "friend-count"})
            if len(friend_count) > 0 :
                friends = friend_count[0].findAll("b")
                if len(friends) > 0:
                    a[4] = friends[0].text.strip()

            #review-count
            review_count = rs.findAll("li", {"class": "review-count"})
            if len(review_count) > 0 :
                review = review_count[0].findAll("b")
                if len(review) > 0:
                    a[3] = review[0].text.strip()
            

            #friends
            photo_count = rs.findAll("li", {"class": "photo-count"})
            if len(photo_count) > 0 :
                photos = photo_count[0].findAll("b")
                if len(photos) > 0:
                    a[5] = photos[0].text.strip()
            
            authors.append(a)



with open("restaurant.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(restaurants)



with open("review.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(reviews)

with open("author.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(authors)