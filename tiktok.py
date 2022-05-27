import subprocess
from time import sleep
import sys
try:
    from colorama import Fore, Back, Style
except:
    subprocess.run("pip install colorama", shell=True)
    subprocess.run("clear", shell=True)
    from colorama import Fore, Back, Style

try:
    import requests
except:
    subprocess.run("pip install requests", shell=True)
    subprocess.run("clear", shell=True)
    import requests


class TiktokService:
    HOST = "https://backend-tdc.traodoicheo.net/".strip('/')

    @classmethod
    def login(cls, username, password):
        print(username, password)
        return requests.post(f"{cls.HOST}/api/login", json={
            "username": username,
            "password": password
        }).json()

    @classmethod
    def get_accounts(cls, token):
        return requests.get(
            url=f"{cls.HOST}/api/tiktok-account",
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()

    @classmethod
    def get_jobs(cls, token, unique_id):
        return requests.get(
            url=f"{cls.HOST}/api/tiktok-jobs?unique_id={unique_id}",
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()

    @classmethod
    def complete(cls, token, unique_id, job_id):
        return requests.post(
            url=f"{cls.HOST}/api/tiktok-jobs/complete",
            json={
                "unique_id": unique_id,
                "job_id": job_id
            },
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()

    @classmethod
    def report(cls, token, unique_id, job_id):
        return requests.post(
            url=f"{cls.HOST}/api/tiktok-jobs/report",
            json={
                "unique_id": unique_id,
                "job_id": job_id
            },
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()

    @classmethod
    def skip(cls, token, unique_id, job_id):
        return requests.post(
            url=f"{cls.HOST}/api/tiktok-jobs/skip",
            json={
                "unique_id": unique_id,
                "job_id": job_id
            },
            headers={
                'Authorization': f'Bearer {token}'
            }
        ).json()


class Tiktok:

    token = None
    unique_id = None

    def login(self):
        try:
            data = open("account.txt").read()
            username, password = data.split('|')
            yes_no = input(f"Bạn có muốn đăng nhập với tài khoản {Fore.RED + username+Style.RESET_ALL} (Y/n): ").upper()
            if yes_no == 'Y':
                res = TiktokService.login(username.strip(), password.strip())
                if "token" in res:
                    # print(res)
                    self.token = res["token"]
                    print(f"{Fore.GREEN}Đăng nhập tài khoản {username} thành công!")
                    return
        except:
            pass
        print('Đăng nhập TraoDoiCheo')
        while True:
            try:
                username = input(Fore.RED + Back.GREEN +"Tài khoản: ")
                password = input("Mật khẩu: ")
                res = TiktokService.login(username, password)
                # import json
                # print(Style.RESET_ALL + json.dumps(res))
                if ("status" in res and res["status"] == 422) or ('success' in res and not res['success']):
                    print(Style.RESET_ALL + Fore.RED + res["message"])
                    continue
                print(Style.RESET_ALL)
                if "token" in res:
                    self.token = res["token"]
                    print(f"{Fore.GREEN}Đăng nhập tài khoản {username} thành công!")
                    with open("account.txt", "w", encoding="utf-8") as fout:
                        fout.write(f"{username}|{password}")
                    break
            except KeyboardInterrupt:
                # quit
                sys.exit()
            except:
                print("Không thể đăng nhập, vui lòng liên hệ admin và thử lại sau vài phút")
                pass

    def choose_accounts(self):
        res = TiktokService.get_accounts(self.token)
        accounts = res["data"]
        if len(accounts) == 0:
            print("Không có tài khoản tiktok nào, vui lòng thêm tài khoản trên web traodoicheo")
            return
        accounts = list(map(lambda acc: {"unique_id": acc["unique_id"], "unique_username": acc["unique_username"]}, accounts))
        print("Xác nhận tài khoản tương tác:")
        for idx, account in enumerate(accounts):
            print(f"\t{str(idx+1)}. {account['unique_username']} {account['unique_id']}")
        choose = int(input("Chọn: "))
        self.unique_id = accounts[choose-1]["unique_id"]
        print(self.unique_id)

    def do_jobs(self):
        res = TiktokService.get_jobs(self.token, self.unique_id)
        jobs = res["data"]
        for job in jobs:
            job_id = job["id"]
            subprocess.run(f"am start --user 0 -W {job['link']}", shell=True)
            sleep(10)
            TiktokService.complete(self.token, self.unique_id, job_id)

    def run(self):
        self.choose_accounts()
        if self.unique_id is not None:
            self.do_jobs()


def main():
    try:
        tt = Tiktok()
        tt.login()
        tt.run()
    except Exception as e:
        print(e)
        # print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
