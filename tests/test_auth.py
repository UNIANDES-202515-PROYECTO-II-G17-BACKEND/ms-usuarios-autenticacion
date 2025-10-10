import pytest

# --- Pruebas para el endpoint de Registro (/v1/auth/register) ---

def test_register_success(client):
    """
    Prueba el registro exitoso de un nuevo usuario.
    """
    response = client.post(
        "/v1/auth/register",
        headers={"X-Country": "co"},
        json={
            "username": "testuser",
            "password": "testpassword",
            "role": "cliente",
            "institution_name": "Test Inc."
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data

def test_register_existing_user(client):
    """
    Prueba que no se puede registrar un usuario con un username que ya existe.
    """
    client.post(
        "/v1/auth/register",
        headers={"X-Country": "co"},
        json={"username": "existinguser", "password": "testpassword", "role": "cliente"}
    )
    response = client.post(
        "/v1/auth/register",
        headers={"X-Country": "co"},
        json={"username": "existinguser", "password": "anotherpassword", "role": "admin"}
    )
    assert response.status_code == 409

def test_register_missing_fields(client):
    """
    Prueba que el registro falla si faltan campos requeridos.
    """
    response = client.post(
        "/v1/auth/register",
        headers={"X-Country": "co"},
        json={"username": "incompleteuser"}
    )
    assert response.status_code == 422

# --- Pruebas para el endpoint de Login (/v1/auth/login) ---

@pytest.fixture
def registered_user(client):
    """
    Fixture que registra un usuario y lo devuelve para usarlo en otras pruebas.
    """
    user_data = {
        "username": "loginuser",
        "password": "loginpassword",
        "role": "admin",
        "institution_name": "Login Corp."
    }
    client.post("/v1/auth/register", headers={"X-Country": "co"}, json=user_data)
    return user_data

def test_login_success(client, registered_user):
    """
    Prueba el inicio de sesión exitoso con credenciales correctas.
    """
    response = client.post(
        "/v1/auth/login",
        headers={"X-Country": "co"},
        json={"username": registered_user["username"], "password": registered_user["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_wrong_password(client, registered_user):
    """
    Prueba que el login falla con una contraseña incorrecta.
    """
    response = client.post(
        "/v1/auth/login",
        headers={"X-Country": "co"},
        json={"username": registered_user["username"], "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    """
    Prueba que el login falla para un usuario que no existe.
    """
    response = client.post(
        "/v1/auth/login",
        headers={"X-Country": "co"},
        json={"username": "nonexistentuser", "password": "anypassword"}
    )
    assert response.status_code == 401

# --- Pruebas para el endpoint de Refresh (/v1/auth/refresh) ---

def test_refresh_success(client, registered_user):
    """
    Prueba la actualización exitosa de un token de acceso.
    """
    # Primero, iniciar sesión para obtener un refresh token
    login_response = client.post(
        "/v1/auth/login",
        headers={"X-Country": "co"},
        json={"username": registered_user["username"], "password": registered_user["password"]}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Luego, usar el refresh token para obtener un nuevo access token
    refresh_response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_refresh_invalid_token(client):
    """
    Prueba que la actualización falla con un token de refresco inválido.
    """
    response = client.post(
        "/v1/auth/refresh",
        json={"refresh_token": "invalid.token.here"}
    )
    assert response.status_code == 401
