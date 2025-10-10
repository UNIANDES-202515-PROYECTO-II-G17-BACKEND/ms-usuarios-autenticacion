import pytest

# --- Pruebas para el endpoint de JWKS (/.well-known/jwks.json) ---

def test_get_jwks(client):
    """
    Prueba que el endpoint de JWKS funciona correctamente.
    """
    response = client.get("/.well-known/jwks.json")
    
    assert response.status_code == 200
    
    data = response.json()
    
    # Verificar la estructura básica de un JWKS
    assert "keys" in data
    assert isinstance(data["keys"], list)
    
    # Si hay claves, verificar la estructura de la primera clave
    if len(data["keys"]) > 0:
        key = data["keys"][0]
        assert "kty" in key
        assert "kid" in key
        assert "use" in key
        assert "alg" in key
        assert "n" in key
        assert "e" in key
