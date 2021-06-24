from typing import Union


class Subject:
    def do_the_job(self, user: str) -> None:
        raise NotImplementedError()


class RealSubject(Subject):
    def do_the_job(self, user: str) -> None:
        print(f"I am doing the job for {user}")


class Proxy(Subject):
    def __init__(self) -> None:
        self._real_subject = RealSubject()

    def do_the_job(self, user: str) -> None:
        print(f"[log] Doing the job for {user} is requested.")
        if user == "admin":
            self._real_subject.do_the_job(user)
        else:
            print("[log] I can do the job just for `admins`.")


def client(job_doer: Union[RealSubject, Proxy], user: str) -> None:
    job_doer.do_the_job(user)


proxy = Proxy()
real_subject = RealSubject()
client(proxy, 'admin')
client(proxy, 'anonymous')
# [log] Doing the job for admin is requested.
# I am doing the job for admin
# [log] Doing the job for anonymous is requested.
# [log] I can do the job just for `admins`.
client(real_subject, 'admin')
client(real_subject, 'anonymous')
# I am doing the job for admin
# I am doing the job for anonymous