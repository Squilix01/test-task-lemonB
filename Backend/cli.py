import argparse
import asyncio
from database.session import session_factory
from repository.user_repo import UserRepository
from services.security import hash_password


async def create_user(username: str, password: str) -> None:
    async with session_factory() as session:
        repo = UserRepository(session)
        existing = await repo.get_by_username(username)
        hashed = hash_password(password)
        
        if existing:
            existing.password = hashed
            await session.commit()
            print(f"Успішно оновлено пароль для користувача: {existing.username} (ID: {existing.id})")
            return

        user = await repo.create(username=username, password=hashed)
        await session.commit()
        print(f"Успішно створено користувача: {user.username} (ID: {user.id})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lemon B — CLI Управління користувачами")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create-user", help="Створити нового користувача")
    create_parser.add_argument("--username", "-u", required=True, help="Ім'я користувача")
    create_parser.add_argument("--password", "-p", required=True, help="Пароль")

    args = parser.parse_args()

    if args.command == "create-user":
        asyncio.run(create_user(args.username, args.password))


if __name__ == "__main__":
    main()
