from enum import Enum


class RunMode(Enum):
    read = READ = 1
    write = WRITE = 2


class ExecutionMode(Enum):
    stream = STREAM = 1
    batch = BATCH = 2