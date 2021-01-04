import os
import sys
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
    with console.status("[bold green]Scanning for Virtual Environments...", spinner='bouncingBar') as status: # skipcq: PYL-W0612
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Script to Locate Virtual Environments")
    parser.add_argument("-s", "--source", help="Source directory")

    args = parser.parse_args()
    vpath = args.source

    console = Console()

    if vpath:
        if os.path.isfile(vpath):
            console.print(f"[red] Path cannot be a file: {vpath}")
            sys.exit()

        if os.path.isdir(vpath):
            console.print(main(vpath))
            console.print("Visit claytonerrington.com for more tools")
        else:
            console.print(f"[red] Path not found: {vpath}")
    else:
        parser.print_help()
