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
