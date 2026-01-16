"""Entry point for le-chat application."""
import torch  # noqa: F401

from le_chat.app import ChatApp


def main():
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    main()
