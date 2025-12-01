# AVISO+ Universal Data Downloader

A small interactive Python script to browse and download AVISO+ files (e.g., DUACS, SWOT) over FTP.

Features
- Browse any folder on the AVISO+ FTP server (`ftp-access.aviso.altimetry.fr`).
- Interactive selection of folders and .nc files.
- Optional recursive search across subfolders.
- Skips files that already exist locally to avoid re-downloading.

Author
- Cristina Martí-Solana

## Quickstart
1. Clone this repository (or download the single script):

   ```bash
   git clone <repo-url>
   cd AVISO_download
   ```

2. (Optional) Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Run the downloader:

   ```bash
   python data_downloader.py
   ```

## What to expect
- The script prompts for a download directory (default: `downloads`).
- You will be asked to enter your AVISO+ username and password (credentials are required to access the FTP server).
- The script lists top-level folders on the FTP server. Choose one by number.
- The script navigates folders, lists `.nc` files (or subfolders) and allows:
  - Selecting individual files by index (comma-separated).
  - Typing `all` to select all files in the current folder.
  - Typing `all` when prompted for subfolder choice to perform a recursive search and select all `.nc` files under the current path.

## Notes on dependencies
- The script uses only Python standard library modules (`ftplib`, `getpass`, `os`). No external packages are required.

## Examples (interactive session)

1) Run and pick a folder

   - Enter the download directory when prompted (or press Enter for `downloads`).
   - Enter AVISO+ credentials when prompted.
   - Choose a top-level folder by its index.
   - If the selected folder contains subfolders, you can either drill down or type `all` to find all `.nc` files recursively.

2) Select files to download

   - When `.nc` files are listed: enter `all` to download them all, or a comma-separated list of indices (e.g. `0,2,5`) to download specific files.

3) The script will download files into the download directory and skip files already present locally.

## Project layout
- `data_downloader.py` — main interactive downloader script.

## Security & credentials
- The script requests your AVISO+ username and password at runtime and uses them only to authenticate to the FTP server. Credentials are not stored by the script.

## License
- This project is licensed under the MIT License — see the `LICENSE` file for details.
