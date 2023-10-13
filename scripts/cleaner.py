import os
import datetime
import time
import logging
import yaml

# Configure logging to display messages on the console (stdout)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YAML configuration file
with open('../config.yml') as f:
    config = yaml.safe_load(f)

def remove_old_and_big_files(directory, max_age_days, max_size_bytes):
    # Get the current date
    current_date = datetime.datetime.now()

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file and not a directory
        if os.path.isfile(file_path):
            # Get the file's last modification time
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            # Calculate the age of the file in days
            age_days = (current_date - file_mtime).days

            # Check if the file is both old and exceeds the specified size
            if age_days > max_age_days and os.path.getsize(file_path) > max_size_bytes:
                try:
                    # Delete the file
                    os.remove(file_path)
                    logging.info(f'Removed file: {file_path}')
                except Exception as e:
                    logging.error(f'Error occurred while removing file {file_path}: {str(e)}')
                    print(f'Error occurred: {str(e)}')  # Print error for debugging
                    raise  # Raise the exception for further handling or debugging

    print('remove_old_and_big_files function execution completed')  # Debugging print statement

# Example usage:
if __name__ == "__main__":
    directory_path = config['directory_path']
    max_age = config['max_age_days']  # Maximum age in days
    max_size = config['max_size_bytes']  # Maximum size in bytes

    while True:
        try:
            remove_old_and_big_files(directory_path, max_age, max_size)
            # Sleep for 5 seconds before the next check
            time.sleep(5)
        except KeyboardInterrupt:
            logging.info('Script interrupted by user')
            break
        except Exception as e:
            logging.error(f'An error occurred: {str(e)}')
            print(f'An error occurred: {str(e)}')  # Print error for debugging
            raise  # Raise the exception for further handling or debugging

    print('Script execution completed')  # Debugging print statement
