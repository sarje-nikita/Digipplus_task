class Business:
    def __init__(self):
        self.state = ""
        self.city = ""
        self.main_business = ""
        self.sub_business = ""
        self.hash_value = ""
        self.name = ""
        self.address = ""
        self.website = ""
        self.phone_number = ""
        self.reviews_average = 0.0
        self.reviews_count = 0
        self.map = ""

    def __str__(self):
        return f"Business(name={self.name}, state={self.state}, city={self.city}, main_business={self.main_business}, " \
               f"sub_business={self.sub_business}, hash_value={self.hash_value}, address={self.address}, " \
               f"website={self.website}, phone_number={self.phone_number}, reviews_average={self.reviews_average}, " \
               f"reviews_count={self.reviews_count}, map={self.map})"
