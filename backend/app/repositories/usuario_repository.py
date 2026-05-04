from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_username(self, username: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def exists_by_username(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def add(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def list_all(self) -> list[Usuario]:
        return self.db.query(Usuario).order_by(Usuario.username.asc()).all()

    def count_active_ingenieros(self) -> int:
        return (
            self.db.query(Usuario)
            .filter(
                Usuario.rol == "ingeniero",
                Usuario.activo.is_(True),
            )
            .count()
        )