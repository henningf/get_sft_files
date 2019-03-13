import datetime
import paramiko
import logging
from stat import S_ISDIR
from os import getenv

'''
Small program to download files from sftp server
'''

'''
Logging setup
'''
LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='log.log',
                        filemode='a',
                        format=LOG_FORMAT,
                        datefmt='%d:%m:%Y %H:%M:%S',
                        level=logging.INFO)

# Loading variables from environment
FTP_SERVERNAME = getenv('FTP_SERVERNAME')
FTP_USERNAME = getenv('FTP_USERNAME')
FTP_PASSWORD = getenv('FTP_PASSWORD')
FTP_PRIVATE_KEY = getenv('FTP_PRIVATE_KEY')
FTP_PORT = int(getenv('FTP_PORT'))
FTP_FOLDER = getenv('FTP_FOLDER')
FTP_KEYFILETYPE = getenv('FTP_KEYFILETYPE')
LOCAL_DIRECTORY = getenv('LOCAL_DIRECTORY')

class  Get_ftp_files():
    def __init__(self):
        # Parameter to hold SFTP CONNECTION
        SFTP_CONNECTION = None

    def connect(self, hostname, username, password, portname, keyfilepath, keyfiletype):
        '''
        create_sftp_client(host, port, username, password, keyfilepath, keyfiletype) -> SFTPClient

        Creates a SFTP client connected to the supplied host on the supplied port authenticating as the user with
        supplied username and supplied password or with the private key in a file with the supplied path.
        If a private key is used for authentication, the type of the keyfile needs to be specified as DSA or RSA.
        :rtype: SFTPClient object.
        '''
        try:
            if keyfilepath is not None:
                # Get private key used to authenticate user.
                if keyfiletype == 'DSA':
                    # The private key is a DSA type key.
                    key = paramiko.DSSKey.from_private_key_file(keyfilepath)
                else:
                    # The private key is a RSA type key.
                    key = paramiko.RSAKey.from_private_key_file(keyfilepath)

            # Create Transport object using supplied method of authentication.
            transport = paramiko.Transport((hostname, portname))
            transport.connect(None, username, password, key)
            
            # Set SFTP_VARIABLE
            self.SFTP_CONNECTION = paramiko.SFTPClient.from_transport(transport)

        except Exception as e:
            logging.error('An error occurred creating SFTP client: %s: %s' % (e.__class__, e)) 

    def close(self):
        # Check that variable SFTP_CONNECTION is set
        SFTP_CONNECTION = self.SFTP_CONNECTION
        if SFTP_CONNECTION is not None:
            try:
                SFTP_CONNECTION.close()
            except Exception as e:
                logging.error('An error occured closing the SFTP connection: %s: %s' % (e.__class__, e))
        else:
            raise Exception('SFTP_CONNECTION is not set')
        
    
    def get_files(self, remote_directory, local_directory):
        '''
        Retrieves files from remote directory,
        Takes input of remote_directory and local_directory
        '''
        SFTP_CONNECTION = self.SFTP_CONNECTION
        try:
            # Looping through all files in directory and downloading them.
            files_copied = 0
            for f in SFTP_CONNECTION.listdir_attr(remote_directory):
                if not S_ISDIR(f.st_mode):
                    try:
                        remote_file_path = remote_directory + f.filename
                        local_file_path = local_directory + f.filename
                        SFTP_CONNECTION.get(remote_file_path, local_file_path)
                        logging.info('Downloaded file: %s to location %s', (f.filename, local_directory))
                        files_copied += 1
                    except Exception as e:
                        logging.error('Could not download file: %s: %s' % (e.__class__, e))
            if files_copied == 0:
                logging.info('no files found')
        except Exception as e:
            logging.error('An error occured getting files from remote directory: %s: %s' % (e.__class__, e))

    
# Initializing class
GET_FILES_FROM_FTP = Get_ftp_files()
# Connecting
GET_FILES_FROM_FTP.connect(FTP_SERVERNAME, FTP_USERNAME, FTP_PASSWORD, FTP_PORT,  FTP_PRIVATE_KEY, FTP_KEYFILETYPE)
# Download files
GET_FILES_FROM_FTP.get_files(FTP_FOLDER, LOCAL_DIRECTORY)
# Closing connectin
GET_FILES_FROM_FTP.close()
