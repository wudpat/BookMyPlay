from account import Account
from booking import Booking
import random
import string

class User(Account):
    def __init__(self, username, password, firstname, surname, booking_data):
        super().__init__(username, password, booking_data)
        self.firstname = firstname
        self.surname = surname

    def calculateFee(self, sport_facility, input_timeslot):
        if self.checkAvailability(sport_facility, input_timeslot):
            if input_timeslot[1][1] == 0:
                return sport_facility.getHourlyRate() * (24 - input_timeslot[1][0])
            else:
                return sport_facility.getHourlyRate() * (input_timeslot[1][1] - input_timeslot[1][0])

    def __generate_booking_id(self, sport_facility):
        suffix_chars = string.ascii_uppercase + string.digits
        random_suffix = "".join(random.choices(suffix_chars, k=8))
        return "-".join([sport_facility.abbrev, random_suffix])
    
    def book(self, sport_facility, input_timeslot):
        if self.checkAvailability(sport_facility, input_timeslot):
            booking_id = self.__generate_booking_id(sport_facility)
            while booking_id in self.booking_data:
                booking_id = self.__generate_booking_id(sport_facility)
            self.booking_data.update({booking_id: Booking(sport_facility, f"{self.firstname} {self.surname}", input_timeslot, self.calculateFee(sport_facility, input_timeslot))})

    def getBookings(self):
        return {id: booking for id, booking in self.booking_data.items() if booking.booker_name == f"{self.firstname} {self.surname}"}

    def cancelBooking(self, booking_id):
        self.booking_data[booking_id].setStatus("Cancelled")