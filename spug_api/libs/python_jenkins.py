import jenkins


class PythonJenkins:
    def __init__(self):
        self.url = 'http://192.168.113.180:30080/'
        self.username = 'admin'
        self.password = '111111'
        self.server = jenkins.Jenkins(self.url, self.username, self.password)


def test_jenkins():
    pj = PythonJenkins()
    user = pj.server.get_whoami()
    print(user)

    jobs = pj.server.get_all_jobs()
    print(jobs)


if __name__ == '__main__':
    test_jenkins()
