import json
from odoo import http
from odoo.http import request
import secrets  # para generar claves seguras
from datetime import datetime, timedelta
import pytz
import logging

_logger = logging.getLogger(__name__)


class MuPasswordController(http.Controller):

    # Endpoint para obtener usuarios
    @http.route(
        "/api/mu_password/users", type="http", auth="none", methods=["GET"], csrf=False
    )
    def get_users(self, **kwargs):
        try:
            users = (
                request.env["res.users"]
                .sudo()
                .with_context(active_test=False)
                .search([("id", "not in", [2, 1, 3, 4, 5])])
            )
            result = []
            for u in users:
                result.append(
                    {
                        "id": u.id,
                        "name": u.name,
                        "login": u.login,
                        "mu_password": u.mu_password,
                        "mu_api_key": u.mu_api_key,
                        "mu_api_key_expiration": u.mu_api_key_expiration.strftime("%Y-%m-%d %H:%M:%S"),
                        "company_name": (
                            u.company_id.name if u.company_id else None
                        ),  # Empresa del usuario
                        "company_id": u.company_id.id if u.company_id else None,
                    }
                )
            return request.make_response(
                json.dumps(result), headers=[("Content-Type", "application/json")]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[("Content-Type", "application/json")],
            )

    # class MuPasswordController(http.Controller):

    # @http.route(
    #     "/api/mu_password/change",
    #     type="http",
    #     auth="none",
    #     methods=["POST"],
    #     csrf=False,
    # )
    # def change_mu_password(self, **kwargs):
    #     try:
    #         # Leer el cuerpo crudo del POST y convertir a JSON
    #         data = json.loads(request.httprequest.data.decode("utf-8"))

    #         user_id = int(data.get("user_id", 0))
    #         new_password = data.get("new_password")

    #         if not user_id or not new_password:
    #             return request.make_response(
    #                 json.dumps({"error": "user_id y new_password son requeridos"}),
    #                 headers=[("Content-Type", "application/json")],
    #             )

    #         # Incluir usuarios inactivos
    #         user = (
    #             request.env["res.users"]
    #             .sudo()
    #             .with_context(active_test=False)
    #             .browse(user_id)
    #         )
    #         if not user.exists():
    #             return request.make_response(
    #                 json.dumps({"error": "Usuario no encontrado"}),
    #                 headers=[("Content-Type", "application/json")],
    #             )

    #         user.write({"mu_password": new_password})

    #         return request.make_response(
    #             json.dumps(
    #                 {"success": True, "user_id": user.id, "new_password": new_password}
    #             ),
    #             headers=[("Content-Type", "application/json")],
    #         )

    #     except Exception as e:
    #         return request.make_response(
    #             json.dumps({"error": f"Excepción: {str(e)}"}),
    #             headers=[("Content-Type", "application/json")],
    #         )
    @http.route(
        "/api/mu_password/change",
        type="http",
        auth="none",
        methods=["POST"],
        csrf=False,
    )
    def change_mu_password(self, **kwargs):
        try:
            # VALIDACIÓN DE TOKEN
            auth_header = request.httprequest.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return request.make_response(
                    json.dumps({"error": "Token no proporcionado"}),
                    headers=[("Content-Type", "application/json")],
                )
            token = auth_header.split(" ")[1]
            _logger.info(f"Token recibido: {token}")

            # Obtener usuario con el token
            user_token = (
                request.env["res.users"]
                .sudo()
                .with_context(active_test=False)
                .search([("mu_api_key", "=", token)], limit=1)
            )
            if not user_token:
                return request.make_response(
                    json.dumps({"error": "Token inválido"}),
                    headers=[("Content-Type", "application/json")],
                )

            # CORRECCIÓN: Comparación correcta de fechas
            bolivia_tz = pytz.timezone("America/La_Paz")
            now_bolivia = datetime.now(bolivia_tz)

            # Convertir la fecha de expiración (naive) a datetime aware de Bolivia
            # Asumimos que la fecha guardada está en hora Bolivia
            expiration_naive = user_token.mu_api_key_expiration
            if expiration_naive:
                # Convertir el naive a aware (asumiendo que está en hora Bolivia)
                expiration_bolivia = bolivia_tz.localize(expiration_naive)

                if expiration_bolivia < now_bolivia:
                    return request.make_response(
                        json.dumps({"error": "Token expirado"}),
                        headers=[("Content-Type", "application/json")],
                    )
            else:
                return request.make_response(
                    json.dumps({"error": "Token sin fecha de expiración"}),
                    headers=[("Content-Type", "application/json")],
                )

            # LECTURA DE DATOS DEL POST
            data = json.loads(request.httprequest.data.decode("utf-8"))
            user_id = int(data.get("user_id", 0))
            new_password = data.get("new_password")

            if not user_id or not new_password:
                return request.make_response(
                    json.dumps({"error": "user_id y new_password son requeridos"}),
                    headers=[("Content-Type", "application/json")],
                )

            # Cambiar password
            user = (
                request.env["res.users"]
                .sudo()
                .with_context(active_test=False)
                .browse(user_id)
            )
            if not user.exists():
                return request.make_response(
                    json.dumps({"error": "Usuario no encontrado"}),
                    headers=[("Content-Type", "application/json")],
                )

            user.write({"mu_password": new_password})

            return request.make_response(
                json.dumps(
                    {"success": True, "user_id": user.id, "new_password": new_password}
                ),
                headers=[("Content-Type", "application/json")],
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": f"Excepción: {str(e)}"}),
                headers=[("Content-Type", "application/json")],
            )

    @http.route(
        "/api/mu_password/login", type="http", auth="none", methods=["POST"], csrf=False
    )
    def login_user(self, **kwargs):
        try:
            # Leer los datos JSON del cuerpo del request
            data = json.loads(request.httprequest.data.decode("utf-8"))
            login = data.get("login")
            password = data.get("password")

            if not login or not password:
                return request.make_response(
                    json.dumps({"error": "Debe proporcionar login y password"}),
                    headers=[("Content-Type", "application/json")],
                )

            # Intentar autenticar el usuario
            uid = request.session.authenticate(request.db, login, password)

            # Solo permitir usuario con uid = 2
            if uid != 2:
                return request.make_response(
                    json.dumps({"error": "No tienes permisos para usar esta API"}),
                    headers=[("Content-Type", "application/json")],
                )

            user = request.env["res.users"].sudo().browse(uid)

            # Generar la API Key
            new_key = secrets.token_hex(20)

            # Hora de Bolivia - tanto para guardar como para mostrar
            bolivia_tz = pytz.timezone("America/La_Paz")
            expiration_time_aware = datetime.now(bolivia_tz) + timedelta(minutes=30)

            # Convertir a naive para guardar en base de datos (pero manteniendo la hora de Bolivia)
            expiration_time_naive = expiration_time_aware.replace(tzinfo=None)

            users_to_update = (
                request.env["res.users"]
                .sudo()
                .with_context(active_test=False)
                .search([("id", "not in", [2, 1, 3, 4, 5])])
            )

            users_to_update.write(
                {
                    "mu_api_key": new_key,
                    "mu_api_key_expiration": expiration_time_naive,  # Se guarda con hora Bolivia pero sin timezone
                }
            )

            # Para la respuesta, formatear la hora con timezone
            expiration_display = expiration_time_aware.strftime("%Y-%m-%d %H:%M:%S")

            result = {
                # "message": "Autenticación exitosa",
                # "user_id": user.id,
                # "user_name": user.name,
                "api_key": new_key,
                #"api_key_expiration": expiration_display,  # Hora Bolivia formateada
                #"timezone": "America/La_Paz",  # Para claridad
            }

            return request.make_response(
                json.dumps(result),
                headers=[("Content-Type", "application/json")],
            )

        except Exception as e:
            return request.make_response(
                json.dumps({"error": str(e)}),
                headers=[("Content-Type", "application/json")],
            )
