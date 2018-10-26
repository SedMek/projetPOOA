class tmdbException(Exception):
    def __init__(self,value):
        self.value=value
    def __str__(self):
        return repr(self.value)

try: raise tmdbException("Test")
except tmdbException as e: print(e.value)