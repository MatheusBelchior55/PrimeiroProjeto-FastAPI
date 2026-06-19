from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'test',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'test',
        'email': 'test@gmail.com',
        'id': 1,
    }


def test_read_user_with_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'test@gmail.com',
            'password': 'test',
            'id': 1,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'test2',
        'email': 'test@gmail.com',
        'id': 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_update_integrity_error(client, user, other_user, token):
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test2',
            'email': 'test2@gmail.com',
            'password': 'test',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'You can only update your own user'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'You can only delete your own user'}
