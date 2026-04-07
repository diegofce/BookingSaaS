"""Role-based access control dependencies.

Roles defined in the system:
- admin    → full access to the negocio (create/edit/delete everything)
- empleado → can view and manage citas, view clients and services
- cliente  → end-user role, no staff access
"""

from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.models.usuario import Usuario

# Roles considered staff (can operate the back-office)
_STAFF_ROLES = {"admin", "empleado"}


def ensure_admin(current_user: Usuario) -> Usuario:
    """Allow only users with rol='admin'."""
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol 'admin' para esta acción.",
        )
    return current_user


def ensure_staff(current_user: Usuario) -> Usuario:
    """Allow admin and empleado roles; reject anyone else (e.g. cliente)."""
    if current_user.rol not in _STAFF_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol 'admin' o 'empleado' para esta acción.",
        )
    return current_user


def require_admin(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    return ensure_admin(current_user)


def require_staff(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    return ensure_staff(current_user)
