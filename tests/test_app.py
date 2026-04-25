from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


def test_read_root(client):
    response = client.get('/')
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


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


def test_read_users(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_user_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'test2',
            'email': 'test2@gmail.com',
            'password': 'test2',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }
