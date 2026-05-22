import os
import shutil
import zipfile
import datetime
import threading
import schedule
import time

from tkinter import *
from tkinter import filedialog, messagebox
from plyer import notification

# ---------------- VARIABLES ---------------- #

source_dir = ""
destination_dir = ""

# ---------------- BACKUP FUNCTION ---------------- #

def backup_files():

    global source_dir, destination_dir

    if not source_dir or not destination_dir:
        messagebox.showerror(
            "Error",
            "Please select both folders"
        )
        return

    # Current Date & Time
    today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create Backup Folder
    backup_folder = os.path.join(destination_dir, today)

    os.makedirs(backup_folder, exist_ok=True)

    # ZIP File Path
    zip_path = os.path.join(
        destination_dir,
        f"{today}.zip"
    )

    try:

        # Copy Files
        for file_name in os.listdir(source_dir):

            source_file = os.path.join(
                source_dir,
                file_name
            )

            dest_file = os.path.join(
                backup_folder,
                file_name
            )

            # Only Files
            if os.path.isfile(source_file):

                try:
                    shutil.copy2(
                        source_file,
                        dest_file
                    )

                    status_label.config(
                        text=f"Copied: {file_name}"
                    )

                    root.update()

                except Exception as e:
                    print(f"Skipped {file_name}: {e}")

        # Create ZIP Backup
        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for foldername, subfolders, filenames in os.walk(backup_folder):

                for filename in filenames:

                    file_path = os.path.join(
                        foldername,
                        filename
                    )

                    zipf.write(
                        file_path,
                        os.path.relpath(
                            file_path,
                            backup_folder
                        )
                    )

        # Log File
        with open("logs.txt", "a") as log:

            log.write(
                f"{today} : Backup Successful\n"
            )

        status_label.config(
            text="Backup Completed Successfully"
        )

        # Desktop Notification
        notification.notify(
            title="Backup Completed",
            message="Files backed up successfully",
            timeout=5
        )

        messagebox.showinfo(
            "Success",
            "Backup Completed Successfully"
        )

    except Exception as e:

        status_label.config(
            text=f"Error: {e}"
        )

        messagebox.showerror(
            "Error",
            str(e)
        )

# ---------------- SELECT SOURCE ---------------- #

def select_source():

    global source_dir

    source_dir = filedialog.askdirectory()

    source_label.config(
        text=source_dir
    )

# ---------------- SELECT DESTINATION ---------------- #

def select_destination():

    global destination_dir

    destination_dir = filedialog.askdirectory()

    destination_label.config(
        text=destination_dir
    )

# ---------------- SCHEDULER ---------------- #

def run_scheduler():

    # Daily Backup Time
    schedule.every().day.at("19:00").do(
        backup_files
    )

    while True:

        schedule.run_pending()

        time.sleep(60)

# ---------------- GUI ---------------- #

root = Tk()

root.title("Advanced Automated Backup System")

root.geometry("750x500")

root.config(bg="#1e1e1e")

# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="Advanced Automated Backup System",
    font=("Arial", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=20)

# ---------------- SOURCE BUTTON ---------------- #

Button(
    root,
    text="Select Source Folder",
    command=select_source,
    width=25,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)

source_label = Label(
    root,
    text="No Source Folder Selected",
    bg="#1e1e1e",
    fg="lightgreen",
    wraplength=700
)

source_label.pack()

# ---------------- DESTINATION BUTTON ---------------- #

Button(
    root,
    text="Select Backup Folder",
    command=select_destination,
    width=25,
    height=2,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold")
).pack(pady=10)

destination_label = Label(
    root,
    text="No Backup Folder Selected",
    bg="#1e1e1e",
    fg="lightblue",
    wraplength=700
)

destination_label.pack()

# ---------------- BACKUP BUTTON ---------------- #

Button(
    root,
    text="Backup Now",
    command=backup_files,
    width=20,
    height=2,
    bg="orange",
    fg="black",
    font=("Arial", 12, "bold")
).pack(pady=30)

# ---------------- STATUS ---------------- #

status_label = Label(
    root,
    text="Waiting...",
    bg="#1e1e1e",
    fg="yellow",
    font=("Arial", 11)
)

status_label.pack()

# ---------------- FOOTER ---------------- #

footer = Label(
    root,
    text="Created by Kalki Kumar",
    bg="#1e1e1e",
    fg="gray"
)

footer.pack(side=BOTTOM, pady=10)

# ---------------- THREAD ---------------- #

threading.Thread(
    target=run_scheduler,
    daemon=True
).start()

# ---------------- MAINLOOP ---------------- #

root.mainloop()