import time

def timer(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        stop_time = time.time()

        # Time in microseconds
        dt_micro = (stop_time - start_time) * 1_000_000

        # Time in milliseconds
        dt_milli = (stop_time - start_time) * 1_000

        # Time in seconds
        dt_sec = stop_time - start_time

        # Displaying in a formatted manner:
        if dt_micro < 1_000:  # If time is less than a millisecond
            print(f"{f.__name__} ran in {dt_micro:.2f} microseconds")
        # If time is less than a second
        elif dt_milli < 1_000:
            print(f"{f.__name__} ran in {dt_milli:.2f} milliseconds")
        else:
            print(f"{f.__name__} ran in {dt_sec:.2f} seconds")

        return result

    return wrapper