import hashlib

for pwd in ["admin123", "dean123", "teacher123", "student123", "app123"]:
    print(pwd, hashlib.sha256(pwd.encode("utf-8")).hexdigest())