import shutil
import os
import re
from collections import Counter

def display_file_contents(contents, show_line_numbers):
    """Displays file contents with or without line numbers."""
    print("\nFile Contents:")
    for index, line in enumerate(contents, start=1):
        if show_line_numbers:
            print(f"{index}: {line.strip()}")
        else:
            print(line.strip())

def count_words(contents):
    """Counts total words and allows counting a specific word."""
    text = ''.join(contents)  # Convert list of lines into a single string
    words = text.split()
    total_words = len(words)

    print(f"\nTotal Word Count: {total_words}")

    specific_word = input("Enter a word to count its occurrences (or press Enter to skip): ").strip()
    if specific_word:
        word_count = text.lower().split().count(specific_word.lower())
        print(f"The word '{specific_word}' appears {word_count} time(s).")

def rename_file(file_name):
    """Allows the user to rename the file."""
    new_name = input("\nEnter the new file name (or press Enter to keep the same): ").strip()
    if new_name:
        if os.path.exists(new_name):
            print("Error: A file with that name already exists.")
        else:
            os.rename(file_name, new_name)
            print(f"File renamed successfully to {new_name}!")
            return new_name  # Return new file name
    return file_name  # Return original file name if not renamed

def undo_changes(original_contents, file_name):
    """Undo the last modification by restoring the original file."""
    with open(file_name, 'w') as file:
        file.writelines(original_contents)
    print("\nLast change undone. The file has been restored to its original state.")

def search_and_highlight(contents):
    """Search for a specific word or phrase and highlight it."""
    search_text = input("Enter the word/phrase to search for: ").strip()
    highlighted_text = []
    for line in contents:
        if search_text.lower() in line.lower():
            highlighted_line = line.replace(search_text, f"\033[1;31m{search_text}\033[0m")  # Red color
            highlighted_text.append(highlighted_line)
        else:
            highlighted_text.append(line)
    print("\nHighlighted occurrences of the search term:")
    display_file_contents(highlighted_text, True)

def backup_file(file_name):
    """Creates a backup of the file with a timestamp."""
    timestamp = str(int(os.path.getmtime(file_name)))
    backup_name = f"{file_name}_backup_{timestamp}.bak"
    shutil.copy(file_name, backup_name)
    print(f"Backup saved as {backup_name}.")
    return backup_name

def restore_file_from_backup(file_name, backup_name):
    """Restores the file from a backup."""
    if os.path.exists(backup_name):
        shutil.copy(backup_name, file_name)
        print(f"File restored from backup: {backup_name}")
    else:
        print(f"Error: Backup file '{backup_name}' does not exist.")

def view_file_metadata(file_name):
    """Shows file metadata such as size, last modified date."""
    if os.path.exists(file_name):
        file_info = os.stat(file_name)
        print(f"\nFile Size: {file_info.st_size} bytes")
        print(f"Last Modified: {time.ctime(file_info.st_mtime)}")
        print(f"Created On: {time.ctime(file_info.st_ctime)}")
    else:
        print(f"Error: File '{file_name}' does not exist.")

def word_frequency_analysis(contents):
    """Analyze word frequencies and show the top 10 frequent words."""
    text = ''.join(contents)
    words = text.split()
    word_counts = Counter(words)
    most_common = word_counts.most_common(10)

    print("\nMost Common Words:")
    for word, count in most_common:
        print(f"{word}: {count} occurrences")

def format_text(contents):
    """Allow the user to format the text to uppercase, lowercase, or title case."""
    format_choice = input("\nChoose text format: [upper/lower/title]: ").strip().lower()
    if format_choice == 'upper':
        contents = [line.upper() for line in contents]
    elif format_choice == 'lower':
        contents = [line.lower() for line in contents]
    elif format_choice == 'title':
        contents = [line.title() for line in contents]
    else:
        print("Invalid choice.")
    return contents

def delete_line(contents):
    """Delete a line from the file."""
    try:
        line_number = int(input("\nEnter the line number to delete: "))
        if line_number < 1 or line_number > len(contents):
            print("Error: Invalid line number.")
        else:
            del contents[line_number - 1]
            print(f"Line {line_number} deleted.")
    except ValueError:
        print("Error: Please enter a valid number.")

def insert_line(contents):
    """Insert a new line into the file."""
    new_line = input("\nEnter the text for the new line: ").strip()
    line_number = int(input("Enter the position to insert the line at: ").strip())
    if line_number < 1 or line_number > len(contents) + 1:
        print("Error: Invalid position.")
    else:
        contents.insert(line_number - 1, new_line + "\n")
        print(f"Line inserted at position {line_number}.")

def check_file_integrity(file_name):
    """Check if the file is a valid text file."""
    try:
        with open(file_name, 'r') as file:
            file.read()
        print(f"The file '{file_name}' is a valid text file.")
    except Exception as e:
        print(f"Error: The file '{file_name}' is corrupted or not a valid text file. {e}")

import time

fileName = input("Enter the File Name: ")

try:
    # Read file contents
    with open(fileName, 'r') as file:
        contents = file.readlines()

    original_contents = contents.copy()  # Make a copy for undo functionality

    # Ask if the user wants line numbers displayed
    show_line_numbers = input("Do you want to show line numbers? (yes/no): ").strip().lower() == 'yes'
    display_file_contents(contents, show_line_numbers)

    count_words(contents)  # Display word count

    # Ask user if they want to rename the file
    fileName = rename_file(fileName)

    # Backup original file before making changes
    backup_file(fileName)

    while True:
        action = input("\nChoose an action: [replace/view/line_numbers/undo/search/backup/restore/metadata/format/delete/insert/word_frequency/integrity/done]: ").strip().lower()

        if action == 'done':
            print("\nAll modifications are complete!")
            break

        elif action == 'view':
            display_file_contents(contents, show_line_numbers)

        elif action == 'line_numbers':
            show_line_numbers = not show_line_numbers
            print(f"\nLine numbers {'enabled' if show_line_numbers else 'disabled'}.")

        elif action == 'replace':
            find_text = input("\nEnter the sentence to find (or type 'cancel' to go back): ")
            if find_text.lower() == 'cancel':
                continue  # Skip to next iteration

            replace_text = input("Enter the new sentence: ")

            # Check if the sentence exists in the file
            if find_text not in ''.join(contents):
                print("Error: The sentence was not found in the file.")
                continue  # Skip to the next loop iteration

            # Create modified content
            contents = [line.replace(find_text, replace_text) for line in contents]

            print("\nPreview of Changes:")
            display_file_contents(contents, show_line_numbers)

            confirm = input("\nDo you want to save these changes? (yes/no): ").strip().lower()
            if confirm == 'yes':
                with open(fileName, 'w') as file:
                    file.writelines(contents)
                print("\nChanges saved successfully!")
            else:
                print("Changes discarded. Try again.")

        elif action == 'undo':
            undo_changes(original_contents, fileName)

        elif action == 'search':
            search_and_highlight(contents)

        elif action == 'backup':
            backup_file(fileName)

        elif action == 'restore':
            backup_name = input("Enter the backup file name to restore from: ").strip()
            restore_file_from_backup(fileName, backup_name)

        elif action == 'metadata':
            view_file_metadata(fileName)

        elif action == 'word_frequency':
            word_frequency_analysis(contents)

        elif action == 'format':
            contents = format_text(contents)

        elif action == 'delete':
            delete_line(contents)

        elif action == 'insert':
            insert_line(contents)

        elif action == 'integrity':
            check_file_integrity(fileName)

except FileNotFoundError:
    print("Error: The file was not found. Please check the file name and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
