from datetime import date

import pgpy

from .models import KeyManage, DEF_KEY_TYPE


class GPGData:
    def __init__(self, keytype=DEF_KEY_TYPE):
        self.key = self._get_key(keytype)
        self.keytype = keytype

    def _get_key(self, keytype):
        ds = KeyManage.objects.filter(key_type=keytype, valid_till__gte=date.today())
        if len(ds) > 0:
            key_obj = ds[0]
            key, _ = pgpy.PGPKey.from_blob(key_obj.key)
        else:
            key = None
        return key

    def encrypt_file(self, filepath):
        file_message = pgpy.PGPMessage.new(filepath, file=True)
        encrypt_message = self.key.encrypt(file_message)
        new_filepath = filepath + '.gpg'
        with open(new_filepath, "w") as f:
            f.write(encrypt_message)
