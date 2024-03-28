# Altadefinizione Film Downloader

This Python script allows you to download films from Altadefinizione, an Italian website known for providing streaming and downloading services for movies and TV shows. The script automates the process of extracting video URLs, handling JavaScript execution, and downloading the films to your local machine.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Configuration](#configuration)
- [License](#license)

## Requirements

Before using the script, ensure you have the following dependencies installed:

- Python 3.6+
- Node.js
- ffmpeg (for video processing)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/altadefinizione-downloader.git
    ```

2. Navigate to the project directory:

    ```bash
    cd altadefinizione-downloader
    ```

3. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Node.js if not already installed:

   Visit the [Node.js website](https://nodejs.org) and follow the installation instructions.

5. Ensure `ffmpeg` is installed on your system:

   - **Windows**: Download the executable from the [official website](https://ffmpeg.org/download.html) and add it to your PATH.
   - **MacOS**: Install `ffmpeg` via Homebrew: `brew install ffmpeg`.
   - **Linux**: Install `ffmpeg` using your package manager: `sudo apt-get install ffmpeg`.

## Usage

Run the script `altadefinizione_downloader.py`:

```bash
python altadefinizione_downloader.py
```

Follow the prompts to input the URL of the film you want to download. The script will then attempt to extract and download the film.

## Features

- Video URL Extraction: The script can extract video URLs from HTML content, including iframes, enabling the download of films embedded within web pages.

- JavaScript Execution: It is capable of executing JavaScript code embedded within HTML pages to obtain the final video URL, providing flexibility in handling dynamically generated content.

- Subtitles Download: Option to download subtitles in multiple languages if availab


## Configuration

The script offers various configuration options, including options specific to M3U8 format (used for video streaming). You can adjust these settings in the config.json file.

```json
{
    "M3U8": {
        "tdqm_workers": 20,
        "tqdm_progress_timeout": 10,
        "minium_ts_files_in_folder": 15,
        "donwload_percentage": 0.995,
        "tqdm_show_progress": false,
        "cleanup_tmp_folder": true
    },
    "M3U8_OPTIONS": {
        "download_audio": true,
        "download_subtitles": true,
        "specific_list_audio": [
            "ita"
        ],
        "specific_list_subtitles": [
            "eng"
        ]
    }
}
```

You can modify these options as needed.

```sql
| Key                        | Default Value | Description                                                                                                                   | Example Value            |
| -------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| `tdqm_workers`             | 20            | Number of workers that cooperate to download .ts files. **A high value may slow down your PC**                                | 30                       |
| `tqdm_progress_timeout`    | 10            | Timeout in seconds to update the progress bar                                                                                 | 15                       |
| `minium_ts_files_in_folder`| 15            | Minimum number of .ts files required in a folder before starting to concatenate files                                         | 20                       |
| `donwload_percentage`      | 0.995         | Percentage of the video to download (ex: 0.995 -> 99.5%)                                                                      | 0.99                     |
| `tqdm_show_progress`       | false         | Whether to display the progress bar during download                                                                           | true                     |
| `cleanup_tmp_folder`       | true          | Whether to clean up temporary files after downloading                                                                         | false                    |
| `download_audio`           | true          | Whether to download audio tracks if available                                                                                 | false                    |
| `download_subtitles`       | true          | Whether to download subtitles if available                                                                                    | true                     |
| `specific_list_audio`      | ["ita"]       | List of specific audio languages to download, if available                                                                    | ["eng", "ita"]           |
| `specific_list_subtitles`  | ["eng"]       | List of specific subtitle languages to download, if available                                                                 | ["ita", "esp"]           |
```