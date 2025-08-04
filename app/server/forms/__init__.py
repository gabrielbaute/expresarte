"""Módulo de formularios de WTForms."""

from app.server.forms.auth_forms import LoginForm, PasswordResetForm
from app.server.forms.admin_forms import CreateUserForm, UserStatusForm, ActualizarUserForm
from app.server.forms.asignar_catedra_form import AsignarCatedraForm
from app.server.forms.califications_form import CalificacionForm, SetCalificacionForm
from app.server.forms.periodo_academico_forms import PeriodoAcademicoForm, CrearPeriodoAcademicoForm, CatedraPeriodoForm