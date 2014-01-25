import win32cred
import pywintypes
import win32ui
import win32con
import sys
import os
import os.path
import uuid
import subprocess

service = "Podium"
podium_online_path = "c:/prevas1/podium online"


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

def build_co(url, creds):
    lst = ["svn", "co"]
    for x in zip(("--username", "--password"), creds):
        lst.extend(x)
    lst.extend(("--non-interactive", "--depth", "empty"))
    lst.append(url)
    uuid_dir = uuid.uuid1().hex
    lst.append(uuid_dir)
    return lst, uuid_dir

def checkout(url, dst, creds):
    url_path = os.path.dirname(url)
    filename = os.path.basename(url)
    if not os.path.exists(dst):
        os.makedirs(dst)
    os.chdir(dst)
    lst, co = build_co(url_path, creds)
    subprocess.check_output(lst)
    os.chdir(co)
    subprocess.check_output(["svn", "up", "-r", "HEAD", filename])
    return filename
    
def checkin(creds):
    pass

def edit_file(filename):
    subprocess.call(["start", filename])

def lock(dest, creds):
    pass

def unlock(dest, creds):
    pass

def main(url):
    creds = get_creds()
    checkout(url, podium_online_path, creds)
    


if __name__ == '__main__':
    pass
#    main()
