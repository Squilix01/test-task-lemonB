from datetime import timedelta
from services.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hashing():
    raw_password = "supersecretpassword123"
    hashed = hash_password(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_encoding_and_decoding():
    username = "test_admin"
    token = create_access_token(subject=username, expires_delta=timedelta(minutes=60))
    assert isinstance(token, str)

    decoded = decode_access_token(token)
    assert decoded["sub"] == username


if __name__ == "__main__":
    test_password_hashing()
    test_jwt_token_encoding_and_decoding()
    print("✅ test_auth.py passed!")
