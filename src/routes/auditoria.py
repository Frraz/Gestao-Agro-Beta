from flask import Blueprint, render_template
from src.models.audit_log import AuditLog

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/admin/auditoria')
def painel_auditoria():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template('admin/auditoria.html', logs=logs)