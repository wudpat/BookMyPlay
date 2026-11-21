class SportFacility(object):
    def __init__(self, name, image, abbrev, description, opening_hours, hourly_rate):
        self.name = name
        self.image = image
        self.abbrev = abbrev
        self.description = description
        self.__opening_hours = opening_hours
        self.__hourly_rate = hourly_rate

    def getOpeningHours(self):
        return self.__opening_hours

    def setOpeningHours(self, opening_hours):
        self.__opening_hours = opening_hours

    def getHourlyRate(self):
        return self.__hourly_rate

    def setHourlyRate(self, hourly_rate):
        self.__hourly_rate = hourly_rate