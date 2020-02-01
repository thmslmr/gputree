import asyncio

from .model import Session
from .view import View


class App:

    def __init__(self, hosts, timeout):
        self.sessions = [Session(**host) for host in hosts]
        self.view = View()

        self.timeout = timeout

    async def future_sessions(self):
        self.view.display(self.sessions)

        q = asyncio.Queue()
        producers = [asyncio.get_event_loop().create_task(self.produce_task(s, q))
                     for s in self.sessions]
        consumers = [asyncio.get_event_loop().create_task(self.consume_task(q))
                     for n in range(10)]

        await asyncio.gather(*producers)
        await q.join()

        for c in consumers:
            c.cancel()

    def main(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.future_sessions())
        finally:
            loop.close()

    async def produce_task(self, session, q):
        res = await session.fetch(timeout=self.timeout)
        session.update(res)
        await q.put("DONE")

    async def consume_task(self, q):
        while True:
            await q.get()
            self.view.clear()
            self.view.display(self.sessions)
            q.task_done()
