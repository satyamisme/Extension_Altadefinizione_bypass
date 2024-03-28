# 28.03.24

import requests
import re, sys
import subprocess
import os
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Class import
from Src.Util.console import console, msg
from Src.Util.message import start_message
from Src.Util.config import config_manager

# Variable
DEBUG_MODE = config_manager.get_bool('GENERAL', 'debug')
ROOT_PATH = config_manager.get('GENERAL', 'root_path')
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.ERROR)


class VideoDownloader:
    def __init__(self):
        self.user_agent = UserAgent(use_external_data=True)
        self.headers = {'User-Agent': self.user_agent.firefox}

    def generate_path(self, url: str) -> str:
        """
        Get film of the name and return the path

        Args:
            url (str): The URL to make the request to.

        Returns:
            str: The path
        """

        title_name = url.split("/")[-1]
        title_name = title_name.split(".")[0] + ".mp4"
        return os.path.join(ROOT_PATH, title_name)

    def make_request(self, url: str) -> str:
        """
        Make an HTTP GET request to the provided URL.

        Args:
            url (str): The URL to make the request to.

        Returns:
            str: The response content if successful, None otherwise.
        """

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            console.print(f"[bold red]Request failed:[/] {e}")
            return None

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parse the provided HTML content using BeautifulSoup.

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            BeautifulSoup: Parsed HTML content if successful, None otherwise.
        """

        try:
            soup = BeautifulSoup(html_content, "lxml")
            return soup
        
        except Exception as e:
            logging.error(f"Failed to parse HTML content: {e}")
            console.print(f"[bold red]Failed to parse HTML content:[/] {e}")
            return None

    def download_video(self, url: str) -> str:
        """
        Download a video from the provided URL.

        Args:
            url (str): The URL of the video to download.

        Returns:
            str: The URL of the downloaded video if successful, None otherwise.
        """

        try:
            html_content = self.make_request(url)

            if html_content is not None:
                soup = self.parse_html(html_content)

                if soup is not None:
                    iframes = soup.find_all("iframe")
                    down_page = iframes[1].get("src")
                    down_page_content = self.make_request(down_page)

                    if down_page_content is not None:
                        pattern = r'data-link="(//supervideo[^"]+)"'
                        match = re.search(pattern, down_page_content)

                        if match:
                            supervideo_url = "https:" + match.group(1)
                            supervideo_content = self.make_request(supervideo_url)

                            if supervideo_content is not None:
                                soup = self.parse_html(supervideo_content)

                                if soup is not None:
                                    new_script = None

                                    for script in soup.find_all("script"):
                                        if "eval" in str(script):
                                            new_script = str(script.text).replace("eval", "var a = ")
                                            new_script = new_script.replace(")))", ")));console.log(a);")

                                    if new_script:
                                        with open('script.js', 'w') as file:
                                            file.write(str(new_script))

                                        result = subprocess.run(['node', 'script.js'], capture_output=True)
                                        mater = str(result.stdout).split(":")[3].split('"}')[0]
                                        video_url = f"https:{mater}"
                                        return video_url
                                    
                                    else:
                                        logging.error("No video URL found in script.")
                                        console.print("[bold red]No video URL found in script.[/]")
                                else:
                                    logging.error("Failed to parse supervideo content.")
                                    console.print("[bold red]Failed to parse supervideo content.[/]")
                            else:
                                logging.error("Failed to fetch supervideo content.")
                                console.print("[bold red]Failed to fetch supervideo content.[/]")
                        else:
                            logging.error("No match found for supervideo URL.")
                            console.print("[bold red]No match found for supervideo URL.[/]")
                    else:
                        logging.error("Failed to fetch down page content.")
                        console.print("[bold red]Failed to fetch down page content.[/]")
                else:
                    logging.error("Failed to parse HTML content.")
                    console.print("[bold red]Failed to parse HTML content.[/]")
            else:
                logging.error("Failed to fetch HTML content.")
                console.print("[bold red]Failed to fetch HTML content.[/]")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            console.print(f"[bold red]An error occurred:[/] {e}")
        return None

    def clean_up(self):
        if os.path.exists('script.js'):

            os.remove('script.js')
            logging.info("Script.js deleted.")

def check_dependencies():
    """
    Check if Node.js is installed on the system.
    """
    try:
        subprocess.run(['node', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info("Node.js is installed.")
        console.print("[bold cyan]Node.js is installed.[/]")
        return True
    except FileNotFoundError:
        logging.error("Node.js is not installed.")
        console.print("[bold red]Node.js is not installed.[/]")
        return False
    except subprocess.CalledProcessError:
        logging.error("Node.js is not installed.")
        console.print("[bold red]Node.js is not installed.[/]")
        return False

def check_python_version():
    """
    Check if Python version is 3.11 or higher.
    """
    if sys.version_info.major == 3 and sys.version_info.minor >= 11:
        logging.info("Python version is 3.11 or higher.")
        console.print("[bold cyan]Python version is 3.11 or higher.[/]")
        return True
    else:
        logging.error("Python version must be 3.11 or higher.")
        console.print("[bold red]Python version must be 3.11 or higher.[/]")

def main():

    os.makedirs(ROOT_PATH, exist_ok=True)
    start_message()

    try:
        if not check_python_version():
            return
        
        console.print("")
        if not check_dependencies():
            return

        # Ask user to input the URL of the video
        console.print("")
        url = msg.ask("[green]Enter the [bold red]URL [green]of the video")

        # Create an instance of VideoDownloader class
        downloader = VideoDownloader()

        # Download the video using the instance
        video_url = downloader.download_video(url)
        start_message()

        if video_url:
            console.print(f"[bold green]Download: [red]{downloader.generate_path(url)} \n")

            arg_1 = f"-p={video_url}"
            arg_2 = f"-o={downloader.generate_path(url)}"
            subprocess.run(["m3u8.exe", arg_1, arg_2], check=True)

        else:
            console.print("[bold yellow]Failed to retrieve the video URL.[/]")
    except KeyboardInterrupt:
        console.print("\nProcess interrupted by the user.")
    except Exception as e:
        console.print(f"[bold red]An error occurred:[/] {e}")
    finally:
        downloader.clean_up()

    console.print("\n[red]END")

main()
