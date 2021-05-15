import uuid, random
import hashlib, pickle
import redis
import sys
import base64
import pycksum


def client_base64(fn):
    try:
        print(fn)
        with open(fn, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print("\n")
            # print(encoded_string.decode('utf-8'))
            image_file.close()

        return encoded_string

    except (IndexError, OSError):
        print("file encoded")


class Util:

    @staticmethod
    def checksum(filename):
        pyck = pycksum.Cksum()
        sha256 = Util.sha256_checksum(filename)
        checksum_md5 = Util.md5_checksum(filename)
        with open(filename, 'rb') as file:
            for b in file:
                pyck._add(b)
        print("Checksum : ", pyck.get_cksum(), "size :", pyck.get_size(), "sha256",
              sha256,
              "md5", checksum_md5, "status:", True)


    @staticmethod
    def sha256_checksum(filename):
        checksum_256 = hashlib.sha256()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                checksum_256.update(chunk)
        return checksum_256.hexdigest()

    @staticmethod
    def md5_checksum(filename):
        checksum_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                checksum_md5.update(chunk)
        return checksum_md5.hexdigest()


    @staticmethod
    def sha256_checksum_base64(filebase):
        checksum_256 = hashlib.sha256()
        checksum_256.update(filebase)
        return checksum_256.hexdigest()

    @staticmethod
    def compare_checksum(sent_file, recv_file):
        if sent_file == recv_file:
            return True
        else:
            return False

    @staticmethod
    def reference_name():
        base = 'ABCDEFG2345HJKLMN6789PQRSTUVWXYZ'
        import time
        b = len(base)
        raw = int(time.time() * 1e5 - 1.45e14)
        n = pow(raw, b, (b ** 7 - b ** 6 - 1)) + b ** 6
        ref = ""
        check = 0
        while n:
            check = (check + n) % b
            ref = base[n % b] + ref
            n //= b
            time.sleep(0.000000000001)
        return str(uuid.uuid4().hex) + ref + base[(-check) % b]

    @staticmethod
    def create_samples():
        import shutil, os
        print(Util.reference_name() + '.jpg File is being copied')
        arr = os.listdir('sample_data')

        original = f'sample_data/{str(arr[random.randint(0, len(arr) - 1)])}'
        target = f'dataset/{Util.reference_name()}.jpg'
        shutil.copyfile(original, target)

    @staticmethod
    def client_base64(fn):
        try:
            with open(fn, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                print("\n")
                print(encoded_string.decode())
            return encoded_string

        except (IndexError, OSError):
            print("file encoded")

    @staticmethod
    def check_code(key):
        redisClient = redis.StrictRedis(host='127.0.0.1', port=6379)
        res = redisClient.get(key)

        if not res:
            print(f'file {key} Redis Key Expired or not found')
            return False
        else:
            print(f'file checksum already exist with {key} with response {res}')

            return True

    @staticmethod
    def redis_new_entry(key, value=None):
        """
        :param insert_response:
        :return:
        """
        try:
            # redispass mNEbI3J8zYYxfgxV
            redisClient = redis.StrictRedis(host='127.0.0.1', port=6379)
            insert_response = str(key)
            redisClient.set(key, str(insert_response))
            redisClient.expire(key, 5000)
        except Exception as e:
            print(f'Redis error {e}')
        finally:
            return dict({'redis_status': 'OK', 'key': key})


if __name__ == '__main__':
    a = Util()

    # print('preparing dataset')
    # for i in range(0, 101):
    #     print(" Number of Images Copied:", i + 1)
    #     a.create_samples()

    # c = a.sha256_checksum('received_data/2410eca8e1654807b7595a9c8eb64b3fJH6US4J6.jpg')
    # print(c)
    # c = a.client_base64('dataset/5a5ba2266290448f8a8a9da0c4a34010EXPM42KY.jpg')
    # # print('c=', c)
    # #c = c.encode('utf-8')
    # d = a.sha256_checksum_base64(c)
    #
    # print(d)
    # print("\n")
    # e = client_base64('dataset/5ee73ab1411b48a794eba13b3a505dcd7FYNJL5R.jpg')
    # # print('c=', c)
    # # c = c.encode('utf-8')
    # f = a.sha256_checksum_base64(e)
    #
    # print(f)
    #
    # print("\n")
    # e = client_base64('received_data/9c0cab04cd9e4db7ad1f7875cfc97bf4N39M265D.jpg')
    # # print('c=', c)
    # # c = c.encode('utf-8')
    # g = a.sha256_checksum_base64(e)
    #
    # print(g)
    a.checksum('dataset/5ee73ab1411b48a794eba13b3a505dcd7FYNJL5R.jpg')
    a.checksum('dataset/0bd9017a570d4d72a5aaf090c9e04cf4DYF5Z52A.jpg')
