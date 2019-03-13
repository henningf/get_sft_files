# Get SFTP files

## About
A Small python program to fetch files from an sftp server.

## Project setup
```
pip install -r requirements.txt
```

### Extra needed
```
You will need to create a private.pem file for this project to work
Project also loads environment variables, so you need to set these environment variables or overwrite them in
the project:
FTP_SERVERNAME, FTP_USERNAME, FTP_PASSWORD, FTP_PRIVATE_KEY, FTP_PORT, FTP_FOLDER, FTP_KEYFILETYPE, LOCAL_DIRECTORY
```

### How to run:
```
python getfiles.py
```
