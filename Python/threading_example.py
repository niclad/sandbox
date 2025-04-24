import threading

def thread_function(name):
    print(f"Thread {name}: starting")
    
    if threading.current_thread() == threading.main_thread():
        print(f"Thread {name}: I'm the main thread")
    else:
        print(f"Thread {name}: I'm a worker thread")

if __name__ == '__main__':
    print(f"Main thread: starting")
    
    threads = []
    for index in range(3):
        print(f"Main thread: creating thread {index}")
        x = threading.Thread(target=thread_function, args=(f"thread{index}",))
        threads.append(x)
        x.start()
    
    thread_function('main')

    # Wait for the thread to finish
    for thread in threads:
        thread.join()
        print(f"Main thread: thread {thread.name} has finished")
    
    print(f"Main thread: all done")
