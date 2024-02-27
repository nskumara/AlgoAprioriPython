import resource

class MemoryLogger:
    # the only instance of this class (this is the "singleton" design pattern)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryLogger, cls).__new__(cls)
            cls._instance._max_memory = 0
        return cls._instance

    def get_max_memory(self):
        return self._max_memory

    def reset(self):
        self._max_memory = 0

    def check_memory(self):
        current_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        if current_memory > self._max_memory:
            self._max_memory = current_memory
        return current_memory
