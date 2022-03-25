#  Copyright (c) 2022. MarilaSoft.
#  #
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  #
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  #
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from requests import RequestException

from libsuitetecsa.__about__ import __name__ as prog_name
from libsuitetecsa.core.exception import LogoutException
from libsuitetecsa.core.protocol import Nauta, UserPortal
from libsuitetecsa.core.session import NautaSession


class UserPortalClient:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.session = None

    def init_session(self):
        """
        Crea una sesión.
        :return:
        """
        self.session = UserPortal.create_session()
        self.session.save()

    @property
    def captcha_as_bytes(self) -> bytes:
        """
        Si la sesión no está creada, la crea y devuelve la imagen captcha
        en formato de bytes.
        :return: bytes: imagen captcha
        """
        if not self.session:
            self.init_session()
        return UserPortal.get_captcha(self.session)

    def login(self, captcha_code: str):
        """
        Inicia sesión en el portal de usuario.
        :param captcha_code: Código captcha.
        :return: instancia de esta clase.
        """
        if not self.session:
            self.init_session()

        self.session.__dict__.update(
            UserPortal.login(
                self.session,
                self.username,
                self.password,
                captcha_code
            ).__dict__
        )

        self.session.save()

        return self

    def recharge(self, recharge_code: str):
        """
        Recarga el saldo de la cuenta registrada.
        :param recharge_code: Código de recarga.
        :return:
        """
        UserPortal.recharge(
            self.session,
            recharge_code
        )

        self.session.__dict__.update(
            UserPortal.get_user_info(
                self.session
            ).__dict__
        )

        self.session.save()

    def transfer(self, mount_to_transfer: str, account_to_transfer: str):
        """
        Transfiere saldo a otra cuenta nauta.
        :param mount_to_transfer: Monto a transferir.
        :param account_to_transfer: Cuenta de destino.
        :return:
        """
        UserPortal.transfer(
            self.session,
            mount_to_transfer,
            account_to_transfer,
            self.password
        )

        self.session.__dict__.update(
            UserPortal.get_user_info(
                self.session
            ).__dict__
        )

        self.session.save()

    def change_password(self, new_passwrd: str):
        """
        Cambia la contraseña de acceso a internet de la cuenta registrada.
        :param new_passwrd: Nueva contraseña.
        :return:
        """
        UserPortal.change_password(
            self.session,
            self.password,
            new_passwrd
        )

    def change_email_password(self, new_passwrd: str):
        """
        Cambia la contraseña de la cuenta de correo asociada.
        :param new_passwrd: Nueva contraseña.
        :return:
        """
        UserPortal.change_email_password(
            self.session,
            self.password,
            new_passwrd
        )

    def get_lasts(self, action: str = "connections", large: int = 5):
        """
        Devuelve las últimas `large` `action` realizadas por la cuenta.
        :param action: Acciones u operaciones que se requieren.
        :param large: Cantidad de action que se requieren.
        :return: Lista de (`Connection | Recharge | Transfer` según el valor de
        `action`).
        """
        return UserPortal.get_lasts(
            self.session,
            action,
            large
        )

    def get_connections(self, year: int, month: int):
        """
        Devuelve las conexiones realizadas en el periodo mes-año especificado.
        :param year: Año en el que buscar.
        :param month: Mes en el que buscar.
        :return: Lista de Connection en el periodo solicitado.
        """
        return UserPortal.get_connections(
            self.session,
            year,
            month
        )

    def get_recharges(self, year: int, month: int):
        """
        Devuelve las recargas realizadas en el periodo mes-año especificado.
        :param year: Año en el que buscar.
        :param month: Mes en el que buscar.
        :return: Lista de Recharge en el periodo solicitado.
        """
        return UserPortal.get_recharges(
            self.session,
            year,
            month
        )

    def get_transfers(self, year: int, month: int):
        """
        Devuelve las transferencias realizadas en el periodo mes-año
        especificado.
        :param year: Año en el que buscar.
        :param month: Mes en el que buscar.
        :return: Lista de Transfer en el periodo solicitado.
        """
        return UserPortal.get_transfers(
            self.session,
            year,
            month
        )

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def block_date(self):
        """
        :return: Fecha de bloqueo de la cuenta registrada.
        """
        return self.session.block_date if self.session else None

    @property
    def delete_date(self):
        """
        :return: Fecha de eliminación de la cuenta registrada.
        """
        return self.session.delete_date if self.session else None

    @property
    def account_type(self):
        """
        :return: Tipo de cuenta de la cuenta registrada.
        """
        return self.session.account_type if self.session else None

    @property
    def service_type(self):
        """
        :return: Tipo de servicio de la cuenta registrada.
        """
        return self.session.service_type if self.session else None

    @property
    def credit(self):
        """
        :return: Saldo disponible de la cuenta registrada.
        """
        return self.session.credit if self.session else None

    @property
    def time(self):
        """
        :return: Tiempo disponible de la cuenta registrada.
        """
        return self.session.time if self.session else None

    @property
    def mail_account(self):
        """
        :return: Cuenta de correo asociada a la cuenta registrada.
        """
        return self.session.mail_account if self.session else None


class NautaClient(object):
    def __init__(self, user: str = None, password: str = None):
        self.user = user
        self.password = password
        self.session = None

    def init_session(self):
        """
        Crea una sesión.
        :return:
        """
        self.session = Nauta.create_session()
        self.session.save()

    @property
    def is_logged_in(self):
        """
        :return: True si hay una sesión abierta.
        """
        return NautaSession.is_logged_in()

    def login(self):
        """
        Inicia sesión en internet.
        :return: Instancia de esta clase.
        """
        if not self.session:
            self.init_session()

        self.session.attribute_uuid = Nauta.login(
            self.session,
            self.user,
            self.password
        )

        self.session.save()

        return self

    @property
    def user_credit(self):
        """
        :return: Saldo disponible de la cuenta.
        """
        dispose_session = False
        try:
            if not self.session:
                dispose_session = True
                self.init_session()

            return Nauta.get_user_credit(
                session=self.session,
                username=self.user,
                password=self.password
            )
        finally:
            if self.session and dispose_session:
                self.session.dispose()
                self.session = None

    @property
    def remaining_time(self):
        """
        :return: Tiempo disponible de la cuenta registrada.
        """
        dispose_session = False
        try:
            if not self.session:
                dispose_session = True
                self.session = NautaSession()

            return Nauta.get_user_time(
                session=self.session,
                username=self.user,
            )
        finally:
            if self.session and dispose_session:
                self.session.dispose()
                self.session = None

    def logout(self):
        """
        Cierra la sesión abierta.
        :return:
        """
        try:
            Nauta.logout(
                session=self.session,
                username=self.user,
            )
            self.session.dispose()
            self.session = None

            return
        except RequestException:
            raise LogoutException(
                "Hay problemas en la red y no se puede cerrar la session.\n"
                "Es posible que ya este desconectado. Intente con '{} down' "
                "dentro de unos minutos".format(prog_name)
            )

    def load_last_session(self):
        """
        Carga la última sesión.
        :return:
        """
        self.session = NautaSession.load()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
