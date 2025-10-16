import pytest

# --- Pruebas para el endpoint de /me (/v1/usuarios/me) ---

@pytest.fixture
def auth_headers(client):
    """
    Fixture que registra, loguea un usuario y devuelve las cabeceras de autorización.
    """
    # Registrar usuario
    client.post(
        "/v1/auth/register",
        headers={"X-Country": "co"},
        json={
            "username": "me_user",
            "password": "me_password",
            "role": "admin",
            "institution_name": "Me Corp."
        }
    )
    
    # Iniciar sesión para obtener el token
    login_response = client.post(
        "/v1/auth/login",
        headers={"X-Country": "co"},
        json={"username": "me_user", "password": "me_password"}
    )
    access_token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def setup_users(client):
    users_data = [
        {"username": "user1", "password": "pass1", "role": "seller"},
        {"username": "user2", "password": "pass2", "role": "admin"},
        {"username": "user3", "password": "pass3", "role": "seller"},
        {"username": "user4", "password": "pass4", "role": "institutional_customer"},
    ]
    for user in users_data:
        client.post("/v1/auth/register", headers={"X-Country": "co"}, json=user)

def test_get_me_success(client, auth_headers):
    """
    Prueba el acceso exitoso al endpoint /me con un token válido.
    """
    response = client.get("/v1/usuarios/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "me_user"
    assert data["role"] == "admin"
    assert data["institution_name"] == "Me Corp."
    assert "id" in data

def test_get_me_no_token(client):
    """
    Prueba que el acceso a /me falla si no se proporciona un token.
    """
    response = client.get("/v1/usuarios/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Falta token"

def test_get_me_invalid_token(client):
    """
    Prueba que el acceso a /me falla con un token inválido.
    """
    headers = {"Authorization": "Bearer invalid.token"}
    response = client.get("/v1/usuarios/me", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido"

def test_get_users_success(client, setup_users):
    response = client.get("/v1/usuarios/", headers={"X-Country": "co"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_users_filter_by_role(client, setup_users):
    response = client.get("/v1/usuarios/?role=seller", headers={"X-Country": "co"})
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 2
    assert all(user['role'] == 'seller' for user in users)

def test_get_users_invalid_role(client):
    response = client.get("/v1/usuarios/?role=invalid_role", headers={"X-Country": "co"})
    assert response.status_code == 400

def test_get_users_pagination(client, setup_users):
    response = client.get("/v1/usuarios/?offset=1&limit=2", headers={"X-Country": "co"})
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_users_empty_list(client):
    # Assuming no users with role 'non_existent_role' exist
    response = client.get("/v1/usuarios/?role=non_existent_role", headers={"X-Country": "co"})
    assert response.status_code == 400
