class Server:
    def __init__(self, processing_frequency: float, data_transmission_rate: float, number_of_cores: int,
                 productivity: float):
        self.processing_frequency = processing_frequency
        self.data_transmission_rate = data_transmission_rate
        self.number_of_cores = number_of_cores
        self.productivity = productivity
