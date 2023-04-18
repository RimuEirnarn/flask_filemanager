# flask_filemanager
Flask File Manager

You can use this as online graphical file manager. Setup by cloning this repo then

```sh
python -m venv .venv
pip install -r ./requirements.txt
```

**Note**: You need to download and unpack bootstrap (+ icons) and put them to static folder.
The structure for bootstrap looks like this

```
/static
  /bootstrap
    /icons
```

## Note

To create account, you can try using `python3 server create-user`

it might asks you if you want to use your username. Also, this asks you for a password. Make sure it's quite different from your login credential.

To change your password, you can delete and create your account.

### Limitation Feature

In DOS systems (Windows), you can only access 1 disk at once as the file systems 'follows' unix way to interpret files, AKA starting from /

As set-uid _doesn't work_ for windows as how setuid in Linux works<sup>[[1]](https://superuser.com/a/973359)</sup>, there may be no setuid app context in future (with setuid, users may be able to actually use their account without actually using root except if invalid user is assigned to database).

### Security Consideration

This program is intended to run not as root. In login context, there's no set-uid to make sure only 1 user can access data from its view. If the program was executed by root, all users authenticated will be able to **delete** all files.
