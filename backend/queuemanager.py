import threading
import queue

from database import dbmanager
from CodeTesting.runBash import exec_bash

# Queue to hold submissions for processing
submission_queue = queue.Queue()

# Flag to control the worker thread's execution
should_continue = True

# Function to process a single submission
def process_submission(user_id, question_id):
    try:
        db = dbmanager('professeur.db')

        question = db.get_question(question_id)

        input_json = question['input']
        output_json = question['output']

        # Execute the bash script and get the result
        result = exec_bash(input_json, output_json, "./CodeTesting/src/sample.json")

        # #Add the result to the database
        # dbm = dbmanager("professeur.db")
        # dbm.add_docker_result_to_database(path, 1, user_id, question_id)
        # dbm.close()

        # # Log the result to a file
        f = open("log.txt", "a")
        f.write(result)
        f.close()

    except Exception as e:
        # Handle any exceptions silently
        print(e)

# Worker thread function to process submissions from the queue
def worker_thread():
    print("Submission worker thread started")

    while should_continue:
        try:
            # Get a submission from the queue with a timeout
            submission = submission_queue.get(timeout=1)
            process_submission(
                submission['path'],
                submission['user_id'],
                submission['question_id']
            )

            # Mark the task as done
            submission_queue.task_done()
        
        except queue.Empty:
            # Continue if the queue is empty (timeout handled above)
            continue
        except Exception as e:
            # Log any errors that occur in the worker thread
            print(f"Error in worker thread: {str(e)}")

    print("Submission worker thread stopped")

# Function to start the worker thread
def start_worker():
    global should_continue
    should_continue = True

    thread = threading.Thread(target=worker_thread, daemon=True)
    thread.start()
    return thread

# Function to stop the worker thread
def stop_worker():
    global should_continue
    should_continue = False

# Function to add a submission to the queue
def add_submission(path, user_id, question_id):
    submission_queue.put({
        'path': path,
        'user_id': user_id,
        'question_id': question_id
    })

if __name__ == '__main__':
    worker = start_worker()
    add_submission("alex.pison.24@ucl.ac.uk", "1")
    stop_worker()