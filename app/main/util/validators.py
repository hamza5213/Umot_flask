import re
import json
import datetime

class Validator:
    def validateEmail(email):
        if re.fullmatch('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email):
            return True
        else:
            return False

    def validateGender(gender):
        if gender == "male" or gender == "female" or gender == "other":
            return True
        else:
            return False

    def validateJSON(jsonString):
        try:
            json.loads(jsonString)
            return True
        except Exception as e:
            return False

    def validateDOB(dob):
        try:
            datetime.datetime.strptime(dob, '%Y-%m-%d')
            return True
        except Exception as e:
            return False

    def validateMovieRating(rating):
        if int(rating) >= 0 and int(rating) <=5:
            return True
        else:
            return False