#!/usr/bin/env python3
"""
GENERAL AVISO+ DATA DOWNLOADER
------------------------------

Features:
- Browse ANY folder in the AVISO FTP server (SWOT, DUACS, etc.)
- Select files interactively
- Recursively search subfolders
- Avoids re-downloading files already present locally

Author: Cristina Martí-Solana
"""

import os
import ftplib
from getpass import getpass


# ---------------------------------------------------------------------
# DOWNLOADER CLASS
# ---------------------------------------------------------------------
class AvisoDownloader:
    def __init__(self, local_dir="downloads"):
        self.ftp_server = "ftp-access.aviso.altimetry.fr"
        self.local_dir = local_dir
        os.makedirs(local_dir, exist_ok=True)
        self.username = None
        self.password = None

    # ----------------------------------------------------------
    def authenticate(self):
        print("Enter your AVISO+ credentials:")
        self.username = input("Username: ").strip()
        self.password = getpass("Password: ").strip()
        print(f"✅ Auth OK for {self.username}")

    # ----------------------------------------------------------
    # FTP file download
    # ----------------------------------------------------------
    def download_file(self, ftp, folder, filename):
        """
        Download one file from the given folder into self.local_dir.
        If the file already exists locally, it is NOT downloaded again.
        """
        ftp.cwd(folder)
        local_path = os.path.join(self.local_dir, filename)

        if os.path.exists(local_path):
            print(f"📁 Already exists locally: {filename} — skipping download.")
            return local_path

        print(f"⬇️  Downloading {filename} ...")
        with open(local_path, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)

        print(f"✅ Saved: {local_path}")
        return local_path

    # ----------------------------------------------------------
    # Recursive file finder
    # ----------------------------------------------------------
    def recursive_list(self, ftp, root):
        """
        Recursively list all .nc files starting from 'root'.

        Returns:
            List of (folder, filename) tuples.
        """
        files = []
        try:
            ftp.cwd(root)
            items = ftp.nlst()
        except Exception:
            return files

        for item in items:
            full = f"{root}/{item}"
            # Heuristic: if it ends with .nc -> file, otherwise treat as directory
            if item.lower().endswith(".nc"):
                files.append((root, item))
            else:
                # Recurse into subfolder
                files.extend(self.recursive_list(ftp, full))

        return files


# ---------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------
def main():
    print("\n=== AVISO+ UNIVERSAL DOWNLOADER ===\n")
    target_dir = input("Download directory [downloads]: ").strip() or "downloads"
    dl = AvisoDownloader(target_dir)
    dl.authenticate()

    with ftplib.FTP(dl.ftp_server) as ftp:
        ftp.login(dl.username, dl.password)

        print("\nTop-level directories available:")
        root_dirs = ftp.nlst()
        for i, d in enumerate(root_dirs):
            print(f"  [{i}] {d}")

        choice = input("\nSelect root folder (number): ").strip()
        root = root_dirs[int(choice)]
        print(f"➡️ Going to root: {root}")
        ftp.cwd(root)

        selected = None  # will hold list of (folder, filename) tuples
        nc_files = []    # .nc files in the current folder (for non-recursive selection)

        while True:
            print(f"\n📂 Folder: {ftp.pwd()}")
            items = ftp.nlst()

            subfolders = []
            nc_files = []

            for item in items:
                if item.lower().endswith(".nc"):
                    nc_files.append(item)
                else:
                    subfolders.append(item)

            if nc_files:
                print(f"\nFound {len(nc_files)} .nc files:")
                for i, f in enumerate(nc_files):
                    print(f"   [{i}] {f}")
                # We found .nc files in this folder; we'll choose which to download after the loop
                break

            if not subfolders:
                print("❌ No .nc files and no more folders.")
                return

            print("\nSubfolders:")
            for i, s in enumerate(subfolders):
                print(f"  [{i}] {s}")
            print("Enter number, or 'all' to search all recursively")

            ans = input("Choice: ").strip()
            if ans == "all":
                all_files = dl.recursive_list(ftp, ftp.pwd())
                print(f"\n📌 Found {len(all_files)} .nc files total (recursive)!")
                selected = all_files         # Already a list of (folder, filename)
                break
            else:
                ftp.cwd(subfolders[int(ans)])

        # ----------------------------------------------------------
        # FILE SELECTION (if not already selected recursively)
        # ----------------------------------------------------------
        if selected is None:
            print("\nEnter file numbers to download (comma separated) or 'all':")
            ans = input("> ").strip()

            if ans == "all":
                selected = [(ftp.pwd(), f) for f in nc_files]
            else:
                idxs = [int(i) for i in ans.split(",")]
                selected = [(ftp.pwd(), nc_files[i]) for i in idxs]

        # ----------------------------------------------------------
        # DOWNLOAD FILES (NO REGION FILTER)
        # ----------------------------------------------------------
        print("\n=== DOWNLOADING FILES ===")
        for folder, filename in selected:
            try:
                # Just let download_file handle "already exists" logic
                dl.download_file(ftp, folder, filename)
            except Exception as e:
                print(f"Error with {filename}: {e}")

        print("\n🎉 DONE! All selected files downloaded (no region filter).\n")


if __name__ == "__main__":
    main()
