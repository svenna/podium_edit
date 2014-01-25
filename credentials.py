import win32cred
import pywintypes
import win32ui
import win32con
import sys
import os
import os.path
import uuid
import subprocess

def cred_dialog(user=None, passwd=None):
    try:
        user, passwd, persisted = win32cred.CredUIPromptForCredentials(
            service,
            0,
            user,
            passwd,
            True,
            win32cred.CREDUI_FLAGS_GENERIC_CREDENTIALS,
            {
                "Parent": None,
                "CaptionText": "Prevas Podium Online Edit",
                "MessageText": "Enter Prevas Podium Credentials"
            }
        )
        return user, passwd
    except pywintypes.error, e:
        if e[:2] == (1223, 'CredUIPromptForCredentials'):
            win32ui.MessageBox("No credentials available, exiting edit",
                               "Prevas Podium online edit",
                               win32con.MB_ICONEXCLAMATION)
            sys.exit()
    
def get_creds():
    """Return username and password"""
    try:
        creds = win32cred.CredRead(service, win32cred.CRED_TYPE_GENERIC,0)
        return creds['UserName'], creds['CredentialBlob'].decode('utf16')
    except pywintypes.error, e:
        if e[:2] == (1168, 'CredRead'):
            return cred_dialog()

def main(url):
    creds = get_creds()
    checkout(url, podium_online_path, creds)

if __name__ == '__main__':
    pass
#    main()
