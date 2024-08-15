from datetime import datetime
import pickle
import os

# Task class to represent individual tasks
class Task:
    def __init__(self, name, priority=1, due_date=None):
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.created = datetime.now()
        self.completed = None
        self.id = None  # Unique ID assigned when the task is added to the task list

    def mark_complete(self):
        """Marks the task as completed by setting the completed date."""
        self.completed = datetime.now()

    def is_completed(self):
        """Returns True if the task is completed, otherwise False."""
        return self.completed is not None

    def __repr__(self):
        return (f"Task(id={self.id}, name='{self.name}', priority={self.priority}, "
                f"due_date={self.due_date}, created={self.created}, completed={self.completed})")


# Tasks class to manage a collection of Task objects
class Tasks:
    def __init__(self, file_path='.todo.pickle'):
        self.file_path = os.path.expanduser(file_path)
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """Loads tasks from the pickle file if it exists, otherwise returns an empty list."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'rb') as file:
                return pickle.load(file)
        return []

    def _save_tasks(self):
        """Saves the current list of tasks to the pickle file."""
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.tasks, file)

    def add_task(self, name, priority=1, due_date=None):
        """Adds a new task and assigns it a unique ID."""
        task = Task(name, priority, due_date)
        task.id = len(self.tasks) + 1
        self.tasks.append(task)
        self._save_tasks()
        return task.id

    def list_tasks(self, show_all=False):
        """Lists tasks, optionally including completed ones."""
        tasks = [task for task in self.tasks if show_all or not task.is_completed()]
        return sorted(tasks, key=lambda task: (task.due_date or datetime.max, -task.priority))

    def complete_task(self, task_id):
        """Marks a task as complete by its unique ID."""
        for task in self.tasks:
            if task.id == task_id and not task.is_completed():
                task.mark_complete()
                self._save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Deletes a task by its unique ID."""
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self._save_tasks()
                return True
        return False

    def query_tasks(self, search_terms):
        """Finds tasks matching all search terms and not completed."""
        return [task for task in self.tasks if all(term.lower() in task.name.lower() for term in search_terms) and not task.is_completed()]

    def generate_report(self):
        """Generates a report of all tasks, including completed ones."""
        return self.list_tasks(show_all=True)


# Example usage or extension with a command-line interface using argparse
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Command Line Task Manager")
    
    # Define commands and options
    parser.add_argument('--add', type=str, help="Add a new task with a description")
    parser.add_argument('--due', type=str, help="Due date for the task (optional)")
    parser.add_argument('--priority', type=int, choices=[1, 2, 3], default=1, help="Priority of the task (1-3, with 1 being default)")
    parser.add_argument('--list', action='store_true', help="List all incomplete tasks")
    parser.add_argument('--done', type=int, help="Mark a task as complete by ID")
    parser.add_argument('--delete', type=int, help="Delete a task by ID")
    parser.add_argument('--query', type=str, nargs='+', help="Search tasks by keywords")
    parser.add_argument('--report', action='store_true', help="Generate a report of all tasks, including completed")

    args = parser.parse_args()
    tasks = Tasks()

    if args.add:
        task_id = tasks.add_task(name=args.add, priority=args.priority, due_date=args.due)
        print(f"Task {task_id} created.")

    elif args.list:
        task_list = tasks.list_tasks()
        print("ID  | Age | Due Date  | Priority | Task")
        print("--- | --- | --------- | -------- | ----")
        for task in task_list:
            due_date = task.due_date or '-'
            age = (datetime.now() - task.created).days
            print(f"{task.id:<3} | {age:<3} | {due_date:<9} | {task.priority:<8} | {task.name}")

    elif args.done:
        if tasks.complete_task(task_id=args.done):
            print(f"Task {args.done} marked as complete.")
        else:
            print(f"Task {args.done} not found or already completed.")

    elif args.delete:
        if tasks.delete_task(task_id=args.delete):
            print(f"Task {args.delete} deleted.")
        else:
            print(f"Task {args.delete} not found.")

    elif args.query:
        search_results = tasks.query_tasks(search_terms=args.query)
        if search_results:
            print("ID  | Age | Due Date  | Priority | Task")
            print("--- | --- | --------- | -------- | ----")
            for task in search_results:
                due_date = task.due_date or '-'
                age = (datetime.now() - task.created).days
                print(f"{task.id:<3} | {age:<3} | {due_date:<9} | {task.priority:<8} | {task.name}")
        else:
            print("No tasks match the search criteria.")

    elif args.report:
        report = tasks.generate_report()
        print("ID  | Age | Due Date  | Priority | Task                  | Created               | Completed")
        print("--- | --- | --------- | -------- | --------------------- | --------------------- | ---------------------")
        for task in report:
            due_date = task.due_date or '-'
            age = (datetime.now() - task.created).days
            created_str = task.created.strftime('%Y-%m-%d %H:%M:%S')
            completed_str = task.completed.strftime('%Y-%m-%d %H:%M:%S') if task.completed else '-'
            print(f"{task.id:<3} | {age:<3} | {due_date:<9} | {task.priority:<8} | {task.name:<21} | {created_str:<21} | {completed_str}")
