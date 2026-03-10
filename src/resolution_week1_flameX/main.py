import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    if os.path.getsize(TASKS_FILE) == 0:
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("task", type=str, nargs="?", help="Task to add")

    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")

    parser.add_argument("-c", "--complete", type=int, help="Mark task complete by ID")

    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")

    parser.add_argument(
        "-p",
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Priority level of the task"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="TaskCLI 0.0.1"
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list:
        tasks = load_tasks()

        if len(tasks) == 0:
            print("No tasks yet. Add one using: python main.py \"your task\"")
            sys.exit(0)

        priority_order = {"high": 3, "medium": 2, "low": 1}

        tasks.sort(key=lambda t: priority_order.get(t["priority"], 2), reverse=True)

        for task in tasks:
            status = "x" if task["done"] else " "
            print(f"[{status}] {task['id']}: {task['task']} ({task['priority']})")

    elif args.complete:
        tasks = load_tasks()

        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                save_task(tasks)
                print(f"Task {args.complete} marked as complete")
                break

    elif args.delete:
        tasks = load_tasks()
        new_tasks = []

        for task in tasks:
            if task["id"] != args.delete:
                new_tasks.append(task)

        save_task(new_tasks)

        print(f"Task {args.delete} deleted")

    elif args.task:
        tasks = load_tasks()

        if len(tasks) == 0:
            new_id = 1
        else:
            new_id = tasks[-1]["id"] + 1

        tasks.append({
            "id": new_id,
            "task": args.task,
            "done": False,
            "priority": args.priority
        })

        save_task(tasks)

        print(f"Task '{args.task}' added with ID {new_id} and priority {args.priority}")
if __name__ == "__main__":
    main()