# 🌾 Gestão Agro Beta

Sistema completo de gestão para fazendas, pessoas, documentos e endividamentos, focado em produtividade, automação e controle centralizado.

![screenshot](docs/screenshot.png) <!-- Adicione um screenshot real aqui -->

---

## ✨ **Funcionalidades Principais**

- **🏞️ Gestão de Fazendas/Áreas**  
  Matrícula, tamanho, posse, localização e controle do CAR.
- **📄 Documentação**  
  Certidões, contratos, vencimentos, alertas e notificações por e-mail.
- **💰 Endividamentos**  
  Gestão de empréstimos, garantias, parcelas e histórico.
- **👥 Pessoas**  
  Cadastro completo, associação com fazendas e documentos.
- **📊 Dashboard**  
  Visualização gráfica de métricas, vencimentos e alertas.
- **🔔 Notificações Inteligentes**  
  Alertas automáticos de vencimento e acompanhamento.

---

## 🚀 **Começando**

### **Pré-requisitos**

- Python 3.8+
- MySQL 5.7+ ou SQLite (default/dev)
- Redis (opcional, para cache)
- Servidor SMTP para notificações por e-mail

### **Instalação**

```bash
git clone https://github.com/Frraz/Gestao-Agro-Beta.git
cd Gestao-Agro-Beta
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env      # Edite o arquivo com suas configurações
```

### **Configuração**

- Edite o arquivo `.env` com os dados do seu banco, e-mail, etc.
- Para MySQL, crie o banco e ajuste as variáveis de conexão conforme seu ambiente.

### **Rodando o sistema**

```bash
python src/main.py
```

Acesse [http://localhost:5000](http://localhost:5000) no navegador.

---

## 🧪 **Testes**

```bash
chmod +x run_tests.sh
./run_tests.sh
```

---

## ☁️ **Deploy no Railway**

1. [Deploy on Railway](https://railway.app/new)
2. Configure as variáveis de ambiente (.env)
3. O sistema faz deploy automático!

---

## 📂 **Estrutura do Projeto**

```
src/
  models/        # Models do SQLAlchemy
  routes/        # Rotas Flask (Blueprints)
  templates/     # Templates Jinja2/HTML
  static/        # CSS, JS, imagens
  utils/         # Helpers e utilitários
  main.py        # App factory e inicialização
migrations/      # Alembic (migrations do banco)
requirements.txt
.env.example
README.md
```

---

## 🎯 **Contribuindo**

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b minha-feature`)
3. Commit suas mudanças (`git commit -am 'feat: Minha nova feature'`)
4. Envie um Pull Request!

---

## 📝 **Licença**

MIT. Sinta-se livre para usar, contribuir e sugerir melhorias!

---

**Dúvidas? Sugestões?**  
Abra uma issue ou fale comigo em [github.com/Frraz](https://github.com/Frraz)