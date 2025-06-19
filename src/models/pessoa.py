# /src/models/pessoa.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Index, Boolean
from sqlalchemy.orm import relationship
from src.models.db import db
import datetime

pessoa_fazenda = Table(
    'pessoa_fazenda',
    db.Model.metadata,
    Column('pessoa_id', Integer, ForeignKey('pessoa.id', ondelete='CASCADE'), primary_key=True),
    Column('fazenda_id', Integer, ForeignKey('fazenda.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_pessoa_fazenda', 'pessoa_id', 'fazenda_id')
)

class Pessoa(db.Model):
    __tablename__ = 'pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, index=True)
    cpf_cnpj = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    endereco = Column(String(200), nullable=True)
    whatsapp = Column(String(20), nullable=True, index=True)
    notificar_email = Column(Boolean, default=True, nullable=False)
    notificar_whatsapp = Column(Boolean, default=False, nullable=False)
    data_criacao = Column(db.Date, default=datetime.date.today, nullable=False)
    data_atualizacao = Column(db.Date, default=datetime.date.today, onupdate=datetime.date.today, nullable=False)
    fazendas = relationship('Fazenda', secondary=pessoa_fazenda, back_populates='pessoas', lazy='selectin')
    documentos = relationship('Documento', back_populates='pessoa', cascade='all, delete-orphan', lazy='selectin')
    endividamentos = relationship('Endividamento', secondary='endividamento_pessoa', back_populates='pessoas')
    __table_args__ = (
        Index('idx_pessoa_nome_cpf', 'nome', 'cpf_cnpj'),
    )
    def __repr__(self):
        return f'<Pessoa {self.nome} - {self.cpf_cnpj}>'
    @property
    def total_fazendas(self):
        return len(self.fazendas) if self.fazendas else 0
    @property
    def total_documentos(self):
        return len(self.documentos) if self.documentos else 0
    @property
    def total_endividamentos(self):
        return len(self.endividamentos) if self.endividamentos else 0
    @property
    def documentos_vencidos(self):
        return [doc for doc in self.documentos if doc.esta_vencido]
    @property
    def documentos_a_vencer(self):
        return [doc for doc in self.documentos if not doc.esta_vencido and doc.precisa_notificar]
    def formatar_cpf_cnpj(self):
        cpf_cnpj = self.cpf_cnpj.replace('.', '').replace('-', '').replace('/', '')
        if len(cpf_cnpj) == 11:
            return f"{cpf_cnpj[:3]}.{cpf_cnpj[3:6]}.{cpf_cnpj[6:9]}-{cpf_cnpj[9:]}"
        elif len(cpf_cnpj) == 14:
            return f"{cpf_cnpj[:2]}.{cpf_cnpj[2:5]}.{cpf_cnpj[5:8]}/{cpf_cnpj[8:12]}-{cpf_cnpj[12:]}"
        return self.cpf_cnpj