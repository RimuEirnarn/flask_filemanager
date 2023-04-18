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

**Note**: to create account, you can try using `python3 server create-user`

it might asks you if you want to use your username. Also, this asks you for a password. Make sure it's quite different from your login credential.

To change your password, you can delete and create your account.

## Security Consideration

This program is intended to run not as root. In login context, there's no set-uid to make sure only 1 user can access data from its view. If the program was executed by root, all users authenticated will be able to **delete** all files.
