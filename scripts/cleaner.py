import os
import datetime
import time
import logging
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YAML configuration file
with open('../config.yml') as f:
    config = yaml.safe_load(f)


def remove_old_and_big_files(directory, max_age_days, max_size_bytes):
    print(f'Starting file cleanup in directory: {directory}')
    removed_files = 0

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f'Error: Directory not found: {directory}')
        logging.error(f'Directory not found: {directory}')
        return

    # Get the current date
    current_date = datetime.datetime.now()

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            # Get the file's last modification time
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            age_days = (current_date - file_mtime).days

            # Check if the file is both old and exceeds the specified size
            if age_days > max_age_days and os.path.getsize(file_path) > max_size_bytes:
                try:
                    # Delete the file
                    os.remove(file_path)
                    print(f'Removed file: {file_path}')
                    logging.info(f'Removed file: {file_path}')
                    removed_files += 1
                except Exception as e:
                    print(f'Error occurred while removing file {file_path}: {str(e)}')
                    logging.error(f'Error occurred while removing file {file_path}: {str(e)}')
                    raise  # Raise the exception for further handling or debugging

    if removed_files > 0:
        print(f'Removed {removed_files} files.')
    else:
        print('No files met the cleanup criteria.')

    print(f'File cleanup completed in directory: {directory}')


# Example usage:
if __name__ == "__main__":
    while True:
        try:
            directory_path = config.get('directory_path', '/path/to/default/directory')
            max_age = config.get('max_age_days', 30)  # Maximum age in days
            max_size = config.get('max_size_bytes', 1024 * 1024)  # Maximum size in bytes (1 MB)

            remove_old_and_big_files(directory_path, max_age, max_size)
        except KeyboardInterrupt:
            print('Script interrupted by user')
            logging.info('Script interrupted by user')
            break
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            logging.error(f'An error occurred: {str(e)}')

        time.sleep(10)  # Sleep for 10 seconds before the next check
