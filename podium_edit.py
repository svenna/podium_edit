import win32cred
import pywintypes
import win32ui
import win32con
import win32api
import sys
import os
import os.path
import uuid
import subprocess
from credentials import *

service = "Podium"
podium_online_path = "c:/prevas1/podium online"
tsturl = "https://frsvfrsv.pdprojects.prevas.com/svn/aef123.documents/trunk/G - Administration/aef123g001 Checklist Completion meeting.doc"

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
    subprocess.check_output(("svn", "up", "-r", "HEAD", filename))
    return filename
    
def checkin(filename):
        subprocess.check_output(('svn', 'ci', filename, '-m', 'Podium online edit'))

def edit_file(filename):
    """
    Edit fthe filename in the args with the default editor
    and return True if the file is modified
    """
    before = os.path.getmtime(filename)
    sfn = win32api.GetShortPathName(filename)
    subprocess.check_call(('start', '/wait', sfn), shell=True)
    if before != os.path.getmtime(filename):
        return True
    else:
        return False

def extract_lock_text(txt):
    """
    Extract all lines from the svn info text regarding lock.
    NOTE, The lock message is not extracted!
    """
    lst = list()
    for line in txt.splitlines():
        if line.startswith('Lock'):
            lst.append(line)
    return lst

def repos_check_lock(url):
    """
    Go to the url and check if there is a lock on the
    file we want ot edit. if so is the case as the user
    if we should steal the lock.
    """
    out = subprocess.check_output(('svn', 'info', url))
    if not "lock" in out:
        return False, False
    else:
        lock_txt = extract_lock_text(out)
        txt = "\n".join(("The file is locked by:", lock_txt[1], lock_txt[2], "Do you want to steal the lock?"))
        if win32ui.MessageBox(txt, "File Locked", 
                win32con.MB_YESNO + win32con.MB_ICONWARNING + win32con.MB_SYSTEMMODAL)  == 6: #steal the lock
            return  True, True
        else:
            return True, False
    
def lock(url, filename):
    """
    Lock the file to be edited.
    """
    locked, steal = repos_check_lock(url)
    if steal:
        unlock(url)       
    if not locked or steal:
        subprocess.check_output(('svn', 'lock', filename, '-m', 'Podium online edit'))
    else:
        sys.exit()

def unlock(url):
    """
    Unlock the file in the repos.
    """
    subprocess.check_output(('svn', 'unlock', '--force', url))

def main(url):
    creds = get_creds(service)
    filename = checkout(url, podium_online_path, creds)
    lock(url, filename)
    if edit_file(filename):
        checkin(filename)

if __name__ == '__main__':
    main(sys.argv[1])
