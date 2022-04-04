import logging
import socket

from .constants import BUFSIZE
from .utils import StoppableThread

class ConnectionHandler(StoppableThread):
    def __init__(self, addr, socket):
        super().__init__()
        self.addr = addr
        self.socket = socket

    def __del__(self):
        logging.info("Closing handler socket")
        self.socket.close()

    def run(self):
        try:
            msg = self.socket.recv(BUFSIZE).rstrip().decode("utf-8")
            logging.info(
                "Message received from connection %s. Msg: %s",
                self.socket.getpeername(),
                msg,
            )
            self.socket.send(f"Your Message has been received: {msg}\n".encode("utf-8"))
        except ConnectionResetError:
            logging.info("Client closed connection before I could echo their message")
        except OSError:
            logging.info("Error while reading socket %s", self.socket)
        finally:
            self.socket.close()


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            logging.error("Could not open socket", exc_info=True)
            raise RuntimeError("Socket error")

        try:
            self._server_socket.bind(("", port))
            self._server_socket.listen(listen_backlog)
        except socket.error:
            logging.error("Could not bind socket", exc_info=True)
            raise RuntimeError("Socket binding error")

        self._signaled_termination = False
        self.active_threads = {}

    def __del__(self):
        """Closes resources used."""
        logging.info("Closing server socket")
        self._server_socket.close()

    def _handle_sigterm(self, *args):
        logging.debug("Got SIGTERM, exiting gracefully")
        logging.debug("Force stopping all children threads")
        for child in self.active_threads.values():
            child.stop()
        logging.debug("Joining all children threads")
        for child in self.active_threads.values():
            child.join()
        logging.debug("Signaling termination")
        self._signaled_termination = True

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        while not self._signaled_termination:
            client_sock, client_addr = self._accept_new_connection()
            handler = ConnectionHandler(client_addr, client_sock)
            self.active_threads[client_sock] = handler

            handler.start()

    def _accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("Proceed to accept new connections")
        conn, addr = self._server_socket.accept()
        logging.info(f"Got connection from {addr}")
        return conn, addr
