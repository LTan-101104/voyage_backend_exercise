from extractor_core.main import parse_data
import json


# {
# "introduction": {
# "first_name": "User Name",
# "last_name": "User Last Name",
# "title": "user Title",
# "tagline": "Prudent Software Engineer."
# },
# "contact": {
# "email": "abc@woyage.ai",
# "phone": "1111111111",
# "address_line": "abc Dr",
# "address_city": "San Franciso",
# "address_state": "CA",
# "address_zipcode": "00000",
# "address_country": "United States",
# "linkedin": "linkedin.com/user-111"
# },
# "summary": {
# "description": "Highly motivated ....."
# }
# }

def process_parsed_data(parsed_data : str):
    #goal: process data into JSON format as required
    try:
        parsed_data = parsed_data.strip()
        cur = json.loads(parsed_data)
        res = {
            "introduction" : {
                "first_name": "User Name",
                "last_name": "User Last Name",
                "title": "user Title",
                "tagline": "Prudent Software Engineer."
            }, 
            "contact" : {
                "email": "abc@woyage.ai",
                "phone": "1111111111",
                "address_line": "abc Dr",
                "address_city": "San Franciso",
                "address_state": "CA",
                "address_zipcode": "00000",
                "address_country": "United States",
                "linkedin": "linkedin.com/user-111"
            },
            "summary" : {
                "description" : ""
            }
        }
        info_set ={
            "first_name",
            "last_name",
            "title",
            "tagline",
            "email",
            "phone",
            "address_line",
            "address_city",
            "address_state",
            "address_zipcode",
            "address_country",
            "linkedin",
            "description"
        }
        for field, obj in res.items():
            for k in obj:
                if k in info_set:
                    res[field][k] = cur[k]
        return res
    except Exception as e:
        raise RuntimeError(f"Error at process_parsed_data : {e}")



    
