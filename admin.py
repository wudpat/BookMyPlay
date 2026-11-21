from account import Account
from sport_facility import SportFacility

class Admin(Account):
    def __init__(self, username, password, facilities_data, booking_data):
        super().__init__(username, password, booking_data)
        self.facilities = facilities_data

    def addFacilities(self, name, image, abbrev, description, opening_hours, hourly_rate):
        self.facilities.append(SportFacility(name, image, abbrev, description, opening_hours, hourly_rate))

    def approve(self, booking_id):
        self.booking_data[booking_id].setStatus("Approved")

    def reject(self, booking_id):
        self.booking_data[booking_id].setStatus("Rejected")

    def cancel(self, booking_id):
        self.booking_data[booking_id].setStatus("Cancelled")

    def getBookings(self):
        return self.booking_data

    def getPending(self):
        return {id: booking for id, booking in self.booking_data.items() if booking.getStatus() == "Pending"}

    def getApproved(self):
        return {id: booking for id, booking in self.booking_data.items() if booking.getStatus() == "Approved"}