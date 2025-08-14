import time

def countdown(start=5):
    print("Starting countdown:")
    for i in range(start, 0, -1):
        print(f"{i}...")
        time.sleep(1)
        print("Liftoff! 🚀")

countdown()


