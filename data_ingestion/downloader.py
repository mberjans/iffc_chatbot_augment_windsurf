import requests
import os

def download_data(url, save_path):
    """
    Downloads data from a specified URL and saves it to a local file.

    Args:
        url (str): The URL to download data from.
        save_path (str): The local path (including filename) to save the data to.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Ensure the directory for save_path exists
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)

        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        print(f"Data downloaded successfully to {save_path}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading data from {url}: {e}")
        return False
    except IOError as e:
        print(f"Error saving data to {save_path}: {e}")
        return False

if __name__ == '__main__':
    # Example usage:
    # Create a dummy file on a local server or use a public URL for testing.
    # For local testing, you can run a simple HTTP server in a directory with a test file:
    # python -m http.server 8000
    # Then access a file like http://localhost:8000/test_file.txt

    # Example with a public file (replace with a real URL for actual testing)
    # test_url = "https://raw.githubusercontent.com/datasets/gdp/master/data/gdp.csv"
    # test_save_path = "data/downloaded_gdp.csv"

    # Create a dummy file for testing if no server is available
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/sample_test_file.txt"):
        with open("data/sample_test_file.txt", "w") as f:
            f.write("This is a test file for the downloader.")

    # To test this, you would typically run a local HTTP server
    # For example, in the project root directory, run: python3 -m http.server
    # Then the URL would be http://localhost:8000/data/sample_test_file.txt
    print("Please run 'python3 -m http.server' in the project root directory in another terminal.")
    test_url = "http://localhost:8000/data/sample_test_file.txt"
    test_save_path = "data/downloaded_sample_test_file.txt"

    print(f"Attempting to download from {test_url} to {test_save_path}")
    success = download_data(test_url, test_save_path)

    if success:
        print("Download function test completed successfully.")
        # You can add checks here to see if the file content is as expected
        if os.path.exists(test_save_path):
            print(f"File {test_save_path} exists.")
            # os.remove(test_save_path) # Clean up test file
            # if os.path.exists("data/sample_test_file.txt"):
            #     os.remove("data/sample_test_file.txt")
            # if os.path.exists("data") and not os.listdir("data"):
            #     os.rmdir("data")
        else:
            print(f"File {test_save_path} was NOT created.")
    else:
        print("Download function test failed.")
