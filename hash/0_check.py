import hashlib
import os


def hash_md5(word):
    return hashlib.md5(word.encode()).hexdigest()


def hash_sha1(word):
    return hashlib.sha1(word.encode()).hexdigest()


def hash_sha512(word):
    return hashlib.sha512(word.encode()).hexdigest()


if __name__ == "__main__":
    os.makedirs("pwds", exist_ok=True)
    combine_lst = list()
    for f in os.listdir("pwds"):
        with open(os.path.join("pwds", f), "r", encoding="utf8") as f:
            filestr = f.read()
        combine_lst.extend(filestr.splitlines())

    hash = "caa83e04d959b49bd2d85cae2ed31891"  # input()
    for word in combine_lst:
        if hash in [
            hash_md5(word),
            hash_sha1(word),
            hash_sha512(word),
        ]:
            print(word, hash_md5(word))
