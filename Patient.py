class Patient:
    def __init__(self, id1, category, load, start, destination, end, rdvTime, rdvDuration, srvDuration):

        """
        Parameters:
            “id” which contains the id of the request.
            “category” which indicates the category of the patient
            “load” which indicates the number of places required in the vehicle during the transport.
            “start”, “destination” and “end” which indicate the ids of respectfully the starting location, medical center and return location for the patient. “start” or “end” can have a -1 value in case of single trip.
            “rdvTime” and “rdvDuration” indicate the start of the appointment and its duration as strings under the format “HHhMM”. In terms of constraints, the patient must be picked up at its starting location for its forward trip at or after rdvTime - maxWaitTime. They must be dropped at their destination before or at rdvTime. They must be picked up for their backward trip at the medical center after or at rdvTime + rdvDuration and must be dropped at their end location before or at rdvTime + rdvDuration + maxWaitTime.
            “srvDuration” indicates the time needed for the patient to embark/disembark the vehicle. It is encoded as a string under the format “HHhMM”.
        """
        self.id = id1
        self.category = category
        self.load = load
        self.start = start
        self.destination = destination
        self.end = end
        self.rdvTime = rdvTime
        self.rdvDuration = rdvDuration
        self.srvDuration = srvDuration

