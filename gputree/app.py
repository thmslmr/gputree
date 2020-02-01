import asyncio

from .model import Session
from .view import View


class App:
    """App object as main object.

    Attributes:
        sessions (list[Session]): List of session object to store session informations.
        view (View): View object to display informations.
        timeout (int): SSH connection timeout.

    """

    def __init__(self, hosts: list, timeout: int):
        """Create sessions and view.

        Args:
            hosts (list): List of dict used to pass hosts informations.
            timeout (int): SSH connection timeout.

        """
        self.sessions = [Session(**host) for host in hosts]
        self.view = View()

        self.timeout = timeout

    def main(self):
        """Run the app."""
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.future_sessions())
        finally:
            loop.close()

    async def future_sessions(self):
        """Create view, fetch session informations and display them as they arrived."""
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

    async def fetch_session_infos(self, session: Session, q: asyncio.Queue):
        """Fetch single session and information and put message in queue once it's done.

        Args:
            session (Session): The session object.
            q (Queue): The asyncio queue.

        """
        res = await session.fetch(timeout=self.timeout)
        session.update(res)
        await q.put("DONE")

    async def view_session_infos(self, q: asyncio.Queue):
        """Update view by displaying new session information when new message in queue.

        Args:
            q (Queue): The asyncio queue.

        """
        while True:
            await q.get()
            self.view.clear()
            self.view.display(self.sessions)
            q.task_done()
