# tests/test_api_documento.py

import pytest

@pytest.fixture
def client(app):
    return app.test_client()

def test_criar_documento(client):
    """
    Testa criação de documento via API REST.
    """
    payload = {
        "nome": "Documento Teste",
        "tipo": "CERTIDOES",
        "data_emissao": "2025-06-20",
        "tipo_entidade": "PESSOA",
        "pessoa_id": 1,
        # Adicione outros campos obrigatórios conforme o schema do endpoint
    }
    response = client.post("/api/documentos/", json=payload)
    assert response.status_code == 201, f"Status inesperado: {response.status_code} - {response.data}"
    data = response.get_json()
    assert data["nome"] == payload["nome"]
    assert data["tipo"] == payload["tipo"]

def test_criar_documento_faltando_campo_obrigatorio(client):
    """
    Testa tentativa de criação de documento com campo obrigatório faltando.
    Deve retornar erro 400 ou 422.
    """
    payload = {
        # "nome" está faltando
        "tipo": "CERTIDOES",
        "data_emissao": "2025-06-20",
        "tipo_entidade": "PESSOA",
        "pessoa_id": 1,
    }
    response = client.post("/api/documentos/", json=payload)
    assert response.status_code in (400, 422), f"Status esperado 400 ou 422, recebeu: {response.status_code}"

def test_criar_documento_tipo_invalido(client):
    """
    Testa tentativa de criação de documento com tipo inválido.
    """
    payload = {
        "nome": "Doc Inválido",
        "tipo": "TIPO_INEXISTENTE",
        "data_emissao": "2025-06-20",
        "tipo_entidade": "PESSOA",
        "pessoa_id": 1,
    }
    response = client.post("/api/documentos/", json=payload)
    assert response.status_code in (400, 422)
    # Corrija esta linha:
    assert "inválido" in response.get_data(as_text=True).lower()

def test_listar_documentos(client):
    """
    Testa listagem dos documentos via API.
    """
    response = client.get("/api/documentos/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)