import os
from rich.console import Console
from rich.table import Table


def main(dir_path):

    # Setup table
    table = Table(show_header=True, header_style="bold red")
    table.add_column("venv Name", width=15)
    table.add_column("Location")
    table.add_column("Folder Size")

    # Use Rich styles to show progress is being worked on
    # return the table as on object so we do the work here and output on the main thread instead
    with console.status("[bold green]Scanning for Virtual Environments...", spinner='bouncingBar') as status:
        for root, _, _ in os.walk(dir_path):
            if os.path.isdir(root):
                # this is the check pattern for windows only
                checks = ["Lib", "Scripts/activate.ps1", "Scripts/activate.bat"]
                # will update the check pattern for Linux soon...
                check_flag = True
                for locs in checks:
                    path = os.path.realpath(os.path.join(root, locs))
                    if not os.path.exists(path):
                        check_flag = False  # if any of the path is missing, then discard the folder
                if check_flag:
                    foldersize = get_dir_size(root)
                    table.add_row(os.path.basename(root), root, str(foldersize))
    
    return table


def get_dir_size(dir_path):
    """Get directory size of venv apps."""
    dir_size = 0
    for root, _, files in os.walk(dir_path):
        dir_size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return f"{round(dir_size/1024/1024, 2)} MB"



console = Console()
vpath = os.getcwd()

console.print(main(vpath))
console.print("Visit claytonerrington.com for more tools")