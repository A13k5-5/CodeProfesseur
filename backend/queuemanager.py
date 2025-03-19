import threading
import queue

from database import dbmanager
import runBash

submission_queue = queue.Queue()
should_continue = True

def process_submission(path, user_id, question_id):
    
    try:
        result = runBash.exec_bash(path)

        dbm = dbmanager()
        dbm.add_docker_result_to_database()
        dbm.close()

        f = open("log.txt", "a")
        f.write(result)
        f.close()

    except Exception as e:
        pass

def worker_thread():
    print("Submission worker thread started")

    while should_continue:
        try:
            submission = submission_queue.get(timeout=1)
            process_submission(
                submission['path'],
                submission['user_id'],
                submission['question_id']
            )

            submission_queue.task_done()
        
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in worker thread: {str(e)}")

def start_worker():
    global should_continue
    should_continue = True
    thread = threading.Thread(target=worker_thread, daemon=True)
    thread.start()
    return thread

def stop_worker():
    global should_continue
    should_continue = False
    print("Submission worker thread stopped")

def add_submission(path, user_id, question_id):
    submission_queue.put({
        'path': path,
        'user_id': user_id,
        'question_id': question_id
    })