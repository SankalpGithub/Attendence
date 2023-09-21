import threading

def timer_function(arg1,arg2):
    print(f"Timer function called with arguments: arg1={arg1}")

# Create a timer with arguments
timer_thread = threading.Timer(5, timer_function, args=(10,None))

# Start the timer
timer_thread.start()

# Wait for the timer to finish (optional)
timer_thread.join()

print("Main program continues...")
