import shelve


class beacon:
        stop = False
        db = "C:/temp/reposrev.db"

        def setup(self):
            self.conn = shelve.open(self.db, writeback=True)

        def recv(self, args):
            """
            Block on receiving data from a post commit hook
            script. return the repos and revision
            """
            pass

        def persist(self, repos, revision):
            """
            store the new revision number for the repos
            """
            conn[repos] = revision
            conn.sync()

        def broadcast(self, data):
            pass

        def loop(self):
            while(not stop):
                repos, rev = recv()
                persist(data)
                broadcast(data)

def main():
        setup()
        loop()


if __name__ == '__main__':
        main()
