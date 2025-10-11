import pytest

# --- Pruebas para el endpoint de JWKS (/.well-known/jwks.json) ---

def test_get_jwks_is_not_available(client):
    """
    Prueba que el endpoint de JWKS ya no está disponible, como corresponde
    al usar un algoritmo simétrico (HS256).
    """
    response = client.get("/.well-known/jwks.json")
    
    # Se espera un 404 Not Found porque el endpoint fue desactivado
    assert response.status_code == 404
