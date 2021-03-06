import subprocess
from time import sleep
import sys


def run_clear():
    subprocess.run("clear", shell=True)

try:
    from colorama import Fore, Back, Style
except:
    subprocess.run("pip install colorama", shell=True)
    run_clear()
    from colorama import Fore, Back, Style

try:
    import requests
except:
    subprocess.run("pip install requests", shell=True)
    run_clear()
    import requests


class TiktokService:
    HOST = "https://backend-tdc.traodoicheo.net/".strip('/')

    @classmethod
    def login(cls, username, password):
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
            yes_no = input(f"B???n c?? mu???n ????ng nh???p v???i t??i kho???n {Fore.RED + username+Style.RESET_ALL} (Y/n): ").upper()
            if yes_no == 'Y':
                res = TiktokService.login(username.strip(), password.strip())
                if "token" in res:
                    # print(res)
                    self.token = res["token"]
                    run_clear()
                    print(f"????ng nh???p t??i kho???n {Fore.GREEN}{username}{Style.RESET_ALL} th??nh c??ng!")
                    return
        except:
            pass
        print('????ng nh???p TraoDoiCheo')
        while True:
            try:
                username = input(Fore.RED + Back.GREEN +"T??i kho???n: ")
                password = input("M???t kh???u: ")
                res = TiktokService.login(username, password)
                # import json
                # print(Style.RESET_ALL + json.dumps(res))
                if ("status" in res and res["status"] == 422) or ('success' in res and not res['success']):
                    print(Style.RESET_ALL + Fore.RED + res["message"])
                    continue
                print(Style.RESET_ALL)
                if "token" in res:
                    self.token = res["token"]
                    print(f"{Fore.GREEN}????ng nh???p t??i kho???n {username} th??nh c??ng!")
                    with open("account.txt", "w", encoding="utf-8") as fout:
                        fout.write(f"{username}|{password}")
                    break
            except KeyboardInterrupt:
                # quit
                sys.exit()
            except:
                print("Kh??ng th??? ????ng nh???p, vui l??ng li??n h??? admin v?? th??? l???i sau v??i ph??t")
                pass

    def choose_accounts(self):
        res = TiktokService.get_accounts(self.token)
        accounts = res["data"]
        if len(accounts) == 0:
            print(f"{Fore.RED}Kh??ng c?? t??i kho???n tiktok n??o, vui l??ng th??m t??i kho???n tr??n web traodoicheo")
            return
        accounts = list(map(lambda acc: {"unique_id": acc["unique_id"], "unique_username": acc["unique_username"]}, accounts))
        print(f"{Fore.YELLOW}X??c nh???n t??i kho???n t????ng t??c:")
        for idx, account in enumerate(accounts):
            print(f"\t{str(idx+1)}. {account['unique_username']} {account['unique_id']}")
        choose = int(input("Ch???n: "))
        self.unique_id = accounts[choose-1]["unique_id"]

    def do_jobs(self):
        while True:
            res = TiktokService.get_jobs(self.token, self.unique_id)
            jobs = res["data"]
            if len(jobs) == 0:
                run_clear()
                print(f"{Style.RESET_ALL}Vui l??ng ?????i 10s ????? t???i job m???i")
                sleep(10)
            for job in jobs:
                job_id = job["id"]
                subprocess.run(f"am start --user 0 -W {job['link']}", shell=True, stdout=subprocess.DEVNULL)
                TiktokService.complete(self.token, self.unique_id, job_id)

    def run(self):
        self.choose_accounts()
        if self.unique_id is not None:
            self.do_jobs()


def main():
    run_clear()
    try:
        tt = Tiktok()
        tt.login()
        tt.run()
    except Exception as e:
        print(e)
        # print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
