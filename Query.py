from Result import Result
class Query():
    def __init__(self, query):
        self.query = query
        self.results = []
        self.minx = 0
        self.maxx = 0

    def add_result(self, res_obj):
        self.results.append(res_obj)

    def get_result(self, index):
        return self.results[index]

    def set_x(self, minx, maxx):
        self.minx = minx
        self.maxx = maxx

    def get_min(self):
        return self.minx

    def get_max(self):
        return self.maxx

    def get_query(self):
        return self.query
