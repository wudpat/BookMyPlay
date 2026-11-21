import abc

class Account(metaclass=abc.ABCMeta):
    def __init__(self, username, password, booking_data):
        self.username = username
        self.__password = password
        self.booking_data = booking_data

    def getPassword(self):
        return self.__password

    def setPassword(self, password):
        self.__password = password

    def checkAvailability(self, sport_facility, input_timeslot):
        for booking in self.booking_data.values():
            if booking.site == sport_facility and booking.getTimeSlot()[0] == input_timeslot[0] and input_timeslot[1][0] < booking.getTimeSlot()[1][1] and booking.getTimeSlot()[1][0] < input_timeslot[1][1] and booking.getStatus() == "Approved":
                return False
        return True

    @abc.abstractmethod
    def getBookings(self):
        pass