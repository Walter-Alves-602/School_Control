"""
Erros de domínio — não dependem de FastAPI nem de nenhum framework web.
Os entrypoints (ex.: entrypoints/api.py) traduzem essas exceções para
respostas HTTP apropriadas.
"""


class DomainError(Exception):
    """Erro base de domínio/aplicação."""


class InvalidCredentialsError(DomainError):
    pass


class ForbiddenCargoError(DomainError):
    def __init__(self, allowed_cargo: str):
        self.allowed_cargo = allowed_cargo
        super().__init__(f"Acesso restrito a usuários do cargo '{allowed_cargo}'")


class InvalidTokenError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass


class DuplicateLoginError(DomainError):
    pass


class CannotDeleteSelfError(DomainError):
    pass


class SalaNotFoundError(DomainError):
    def __init__(self, sala_name: str):
        self.sala_name = sala_name
        super().__init__(f"Sala '{sala_name}' não encontrada ou sem computadores cadastrados")
