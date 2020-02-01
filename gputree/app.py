import asyncio

from .model import Session
from .view import View


class App:
    def __init__(self, hosts, timeout):
        self.sessions = [Session(**host) for host in hosts]
        self.view = View()

        self.timeout = timeout

    def main(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.future_sessions())
        finally:
            loop.close()

    async def future_sessions(self):
        self.view.display(self.sessions)

        q = asyncio.Queue()
        sessions_infos = [
            asyncio.get_event_loop().create_task(self.fetch_session_infos(s, q))
            for s in self.sessions
        ]
        view_infos = [
            asyncio.get_event_loop().create_task(self.view_session_infos(q))
            for n in range(10)
        ]

        await asyncio.gather(*sessions_infos)
        await q.join()

        for c in view_infos:
            c.cancel()

    async def fetch_session_infos(self, session, q):
        res = await session.fetch(timeout=self.timeout)
        session.update(res)
        await q.put("DONE")

    async def view_session_infos(self, q):
        while True:
            await q.get()
            self.view.clear()
            self.view.display(self.sessions)
            q.task_done()
