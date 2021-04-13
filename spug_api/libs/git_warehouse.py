import gitlab


class GitWarehouse:
    def __init__(self):
        self.url = 'http://192.168.7.197:8083'
        self.private_token = 'x-E6D9iziymxjRX2JJsL'
        self.gl = gitlab.Gitlab(self.url, self.private_token)

    def get_all_group(self):
        return self.gl.groups.list()

    def get_all_project_by_group_id(self, group_id):
        return self.gl.groups.get(group_id).projects.list(all=True)

    def get_all_branch_by_project_id(self, project_id):
        return self.gl.projects.get(project_id).branches.list()


def test():
    gl = GitWarehouse()

    groups = gl.get_all_group()
    for group in groups:
        print(group)

        projects = group.projects.list(all=True)
        for project in projects:
            print(project)

            branches = gl.get_all_branch_by_project_id(project.id)
            for branch in branches:
                print(branch)

            break

        break


if __name__ == '__main__':
    test()
