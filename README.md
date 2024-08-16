# Command Line Task Manager

## Overview
This task manager is a command-line tool that allows you to manage tasks efficiently without the need for a graphical interface. You can add, list, complete, delete, and query tasks directly from the terminal.

## Setup Instructions

### 1. Make the Script Executable
To run the task manager from any location on your computer, you need to make the script executable. Add the following shebang line at the top of `todo.py`:

```bash
#!/usr/bin/env python3

1.Ensure you're in the correct directory where todo.py is located (/Users/desktop/*.
2.Use chmod +x todo.py after navigating to the correct directory.
3.Move the script to a directory in your $PATH (e.g., /usr/local/bin). (sudo mv todo.py /usr/local/bin/todo)
4.Run the script from any terminal session using todo. (todo --add "Complete task 1")
