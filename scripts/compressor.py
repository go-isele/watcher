import yaml
import os
import datetime
import zipfile
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the YAML configuration file
with open('../config.yml') as f:
    config = yaml.safe_load(f)


# Define a utility function to check if a log file is already archived

# Utility function to check if a log file is already archived
def is_log_archived(log_file_name):
    existing_zip_files = [file for file in os.listdir(output_directory) if file.endswith('.zip')]
    return any(log_file_name in zip_file for zip_file in existing_zip_files)


# Get the log file path, rotation frequency, rotation interval, and max log file size from the configuration file
log_file_path = config['log_file_path']
rotation_frequency = config['log_rotation_type']  # 'daily', 'weekly', 'hourly', 'custom'
rotation_interval = config.get('log_rotation_interval', 5)  # Number of hours, default to 5 if not specified
max_log_file_size = config['max_log_file_size']  # Maximum size of the log file in bytes
output_directory = config.get('output_directory', '')  # Get the output directory from the configuration file
delete_after_compression = config.get('delete_after_compression', False)


# Define the log rotation function
def rotate_log():
    # Check if the log file exists and its size exceeds the maximum allowed size
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_log_file_size:
        # Get the base name of the log file without the directory path
        log_file_name = os.path.basename(log_file_path)

        # Check if a zip file with the same name as the log file exists in the output directory
        if not is_log_archived(log_file_name):
            current_time = datetime.datetime.now().time()

            rotation_needed = False

            if rotation_frequency == 'daily':
                rotation_needed = current_time.hour == 0 and current_time.minute == 0  # Rotate at midnight
            elif rotation_frequency == 'weekly':
                # Get the current date and check if it's Monday (0 represents Monday)
                current_date = datetime.datetime.now().date()
                rotation_needed = current_time.hour == 0 and current_time.minute == 0 and current_date.weekday() == 0
            elif rotation_frequency == 'hourly':
                rotation_needed = current_time.minute == 0  # Rotate at the beginning of each hour
            elif rotation_frequency == 'custom':
                current_hour = current_time.hour
                rotation_needed = current_hour % rotation_interval == 0

            # Determine if compression will be applied and validate the compression pattern
            compression_pattern = config['compression_pattern']  # Compression pattern from config.yml
            if compression_pattern in [zipfile.ZIP_DEFLATED, zipfile.ZIP_STORED]:
                will_be_compressed = compression_pattern == zipfile.ZIP_DEFLATED
            else:
                logging.error(f'Invalid compression pattern: {compression_pattern}. Using ZIP_DEFLATED instead.')
                compression_pattern = zipfile.ZIP_DEFLATED
                will_be_compressed = True

            # Create a timestamp for the archived log file
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

            # Create the zip file name based on the log file name and timestamp
            zip_file_name = f'{log_file_name}_{timestamp}.zip'

            archived_log_file_path = os.path.join(output_directory, zip_file_name)

            # Print information about log file size and compression status
            logging.info(f'Log file size: {os.path.getsize(log_file_path)} bytes')
            logging.info(f'Compression: {"Yes" if will_be_compressed else "No"}')

            # Create a ZIP file for the log file
            with zipfile.ZipFile(
                    archived_log_file_path, 'w',
                    compression=compression_pattern,
                    compresslevel=9, allowZip64=True
            ) as zip_file:
                zip_file.write(log_file_path, log_file_name)

                # Delete the original log file if specified in the configuration
                if delete_after_compression:
                    os.remove(log_file_path)
                    logging.info(f'Original log file deleted after compression.')

            logging.info(f'Log rotated at {timestamp}. Original log file archived as {archived_log_file_path}')

            # Print when the next check will occur
            next_check_time = datetime.datetime.now() + datetime.timedelta(seconds=rotation_interval)
            logging.info(f'Next check at: {next_check_time.strftime("%Y-%m-%d %H:%M:%S")}')
            logging.info('---')  # Separating lines for better readability
        else:
            logging.info(f'Log file {log_file_name} is already archived. Skipping rotation.')
    else:
        logging.info('Log file size is below the maximum allowed size. No rotation needed.')


# Call the log rotation function
while True:
    rotate_log()
    time.sleep(rotation_interval)  # Check every 5 seconds for demonstration purposes; you can adjust this as needed
