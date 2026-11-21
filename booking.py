class Booking(object):
    def __init__(self, sport_facility, booker_name, timeslot, total_fee):
        self.site = sport_facility
        self.booker_name = booker_name
        self.__timeslot = timeslot
        self.__total_fee = total_fee
        self.__status = "Pending"

    def getTimeSlot(self):
        return self.__timeslot

    def getTotalFee(self):
        return self.__total_fee

    def getStatus(self):
        return self.__status

    def setStatus(self, status):
        self.__status = status