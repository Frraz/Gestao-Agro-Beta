#/src/routes/auditoria.py
from flask import Blueprint, render_template
from src.models.auditoria import Auditoria
from flask_login import login_required

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/admin/auditoria')
@login_required
def painel_auditoria():
    logs = Auditoria.query.order_by(Auditoria.data_hora.desc()).limit(100).all()
    return render_template('admin/auditoria.html', logs=logs)