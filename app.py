#!/usr/bin/python3
# Copyright (c) BDist Development Team
# Distributed under the terms of the Modified BSD License.
import os
from logging.config import dictConfig
from datetime import datetime
from flask import Flask, jsonify, request
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool

# Use the DATABASE_URL environment variable if it exists, otherwise use the default.
# Use the format postgres://username:password@hostname/database_name to connect to the database.
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://saude:saude@postgres/saude")

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    kwargs={
        "autocommit": True,  # If True don’t start transactions automatically.
        "row_factory": namedtuple_row,
    },
    min_size=4,
    max_size=10,
    open=True,
    # check=ConnectionPool.check_connection,
    name="postgres_pool",
    timeout=5,
)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
app.config.from_prefixed_env()
log = app.logger
app.config["JSON_AS_ASCII"] = False


def date_in_future(data, hora):
    data = datetime.strptime(data, "%Y-%m-%d")
    hora = datetime.strptime(hora, "%H:%M")
    data_hora = datetime.combine(data, hora.time())
    if data_hora < datetime.now():
        return False
    return True


@app.route("/", methods=("GET",))
def clinics_index():
    """Show all the clinics"""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            clinics = cur.execute(
                """
                SELECT nome, morada
                FROM clinica
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    return jsonify(clinics), 200


@app.route("/c/<clinica>", methods=("GET",))
def specialities_clinic(clinica):
    """Shows the specialities availabel at <clinica>."""
    #  TODO make query to get specialities
    with pool.connection() as conn:
        with conn.cursor() as cur:
            specialities = cur.execute(
                """
                SELECT DISTINCT especialidade 
                FROM clinica 
                JOIN trabalha ON clinica.nome=trabalha.nome 
                JOIN medico ON trabalha.nif=medico.nif 
                WHERE clinica.nome = %(clinica)s;
                """,
                {"clinica": clinica},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # At the end of the `connection()` context, the transaction is committed
    # or rolled back, and the connection returned to the pool.
    return jsonify(specialities), 200


@app.route("/c/<clinica>/<especialidade>", methods=("GET",))
def clinics_specialities_doctors(clinica, especialidade):
    """Shows all the doctors that have the <especialidade> at <clinica>. And the 3 first schedules available. (date, hour)"""

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT DISTINCT especialidade
                        FROM medico;
                        """)
            
            rows = cur.fetchall()
            especialidades = [row.especialidade for row in rows]
            if especialidade not in especialidades:
                return jsonify({"message": f"A especialidade '{especialidade}' não existe", "status": "error"}), 404



            doctors = cur.execute(
                """WITH horarios_disponiveis AS (
                    SELECT DISTINCT m.nome, m.nif, m.especialidade, clinica.nome AS clinica_nome,
                        d.data,
                        h.hora, 
                        c.hora AS hora_consulta
                    FROM medico m
                        JOIN trabalha t ON t.nif = m.nif
                        JOIN clinica ON clinica.nome = t.nome
                        CROSS JOIN (SELECT DISTINCT data FROM consulta) d 
                        CROSS JOIN horarios h
                        LEFT JOIN consulta c ON c.nif = m.nif  AND c.hora = h.hora AND c.nome = clinica.nome AND c.data = d.data
                    WHERE m.especialidade = %(especialidade)s 
                        AND clinica.nome = %(clinica)s
                        AND (d.data + h.hora) > (NOW() AT TIME ZONE 'Europe/Lisbon')
                        AND t.dia_da_semana = EXTRACT(DOW FROM d.data)
                    ORDER BY 
                        m.nome, d.data, h.hora),

                    horarios_partidos AS (SELECT nome, data, hora, 
                        ROW_NUMBER() OVER (PARTITION BY nif ORDER BY data + hora) AS row_num
                        FROM horarios_disponiveis
                        WHERE hora_consulta IS NULL)

                    SELECT nome, 
                        TO_CHAR(data, 'YYYY-MM-DD') AS data, 
                        TO_CHAR(hora, 'HH24:MI:SS') AS hora
                    FROM horarios_partidos
                        WHERE row_num <= 3
                        ORDER BY nome, data, hora;
                 """,
                {"clinica": clinica, "especialidade": especialidade},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")
        
    if not doctors:
        return jsonify({"message": f"A clínica '{clinica}' não tem médicos da especialidade '{especialidade}'", "status": "error"}), 404

    # At the end of the `connection()` context, the transaction is committed
    # or rolled back, and the connection returned to the pool.
    return jsonify(doctors), 200


@app.route("/a/<clinica>/registrar", methods=("POST", "PUT"))
def register_consult(clinica):
    """Register a consult."""
    # TODO: MAKE date filter
    #       MAKE date validation
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")

    error = None

    if not paciente:
        error = "Paciente is required."
    if not medico:
        error = "Medico is required."
    if not data:
        error = "Data is required."
    if not hora:
        error = "Hora is required."
    if not date_in_future(data, hora):
        error = (
            "Data ou hora é invalida, tem de ser uma data e hora posterior à atual."
        )

    if error is not None:
        return jsonify({"message": error, "status": "error"}), 400
    else:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # gets last sns_code
                last_sns_code = cur.execute(
                    """SELECT codigo_sns 
                        FROM consulta
                        WHERE consulta.codigo_sns IS NOT NULL
                        ORDER BY consulta.codigo_sns 
                        DESC LIMIT 1;
                    """
                ).fetchone()
                new_sns_code = int(last_sns_code[0]) + 1
                new_sns_code = str(new_sns_code).zfill(12)

                try:
                    cur.execute("""
                                SELECT 1
                                FROM consulta
                                WHERE nome = %(clinica)s
                                    AND nif = %(medico)s
                                    AND data = %(data)s
                                    AND hora = %(hora)s;
                                """,
                                {
                                    "clinica": clinica,
                                    "medico": medico,
                                    "data": data,
                                    "hora": hora,
                                },
                    )
                except Exception as e:
                    return jsonify({"message": str(e), "status": "error"}), 400
                
                if cur.rowcount != 0:
                    return jsonify({"message": "O médico está em consulta a essa hora", "status": "error"}), 400

                try:
                    cur.execute(
                        """
                        INSERT INTO consulta (ssn, nif, nome, data, hora)
                        VALUES (%(ssn)s, %(nif)s, %(nome)s,%(data)s, %(hora)s);
                        """,
                        {
                            "ssn": paciente,
                            "nif": medico,
                            "nome": clinica,
                            "data": data,
                            "hora": hora,
                        },
                    )
                    # The result of this statement is persisted immediately by the database
                    # because the connection is in autocommit mode.
                except Exception as e:
                    error_message = str(e).split("\n")[0]
                    return (
                        jsonify(
                            {
                                "message": error_message,
                                "status": "error",
                            }
                        ),
                        400,
                    )

        return (
            jsonify(
                {
                    "message": f"Consulta marcada para o dia {data} às {hora} com sucesso",
                    "status": "success",
                }
            ),
            200,
        )


@app.route("/a/<clinica>/cancelar", methods=("POST",))
def cancel_consult(clinica):
    """Cancel a consult."""
    # TODO: make query to register consult
    paciente = request.args.get("paciente")
    medico = request.args.get("medico")
    data = request.args.get("data")
    hora = request.args.get("hora")

    error = None

    if not paciente:
        error = "Paciente is required."
    if not medico:
        error = "Medico is required."
    if not data:
        error = "Data is required."
    if not hora:
        error = "Hora is required."
    if not date_in_future(data, hora):
        error = (
            "Data ou hora é invalida, tem de ser uma data ou hora posterior à atual."
        )

    if error is not None:
        return jsonify({"message": error, "status": "error"}), 400
    else:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                                SELECT 1 
                                FROM consulta
                                WHERE nome = %(clinica)s
                                    AND nif = %(medico)s
                                    AND ssn = %(paciente)s
                                    AND data = %(data)s
                                    AND hora = %(hora)s;
                                """,
                            {
                            "clinica": clinica,
                            "medico": medico,
                            "paciente": paciente,
                            "data": data,
                            "hora": hora,
                        },
                    )
                    if cur.rowcount == 0:
                        return jsonify({"message": "Consulta não encontrada", "status": "error"}), 400
                    
                except Exception as e:
                    return jsonify({"message": str(e), "status": "error"}), 400


                try:    
                    cur.execute(
                        """
                        DELETE FROM consulta
                        WHERE nome = %(clinica)s
                        AND nif = %(medico)s
                        AND ssn = %(paciente)s
                        AND data = %(data)s
                        AND hora = %(hora)s;
                        """,
                        {
                            "clinica": clinica,
                            "medico": medico,
                            "paciente": paciente,
                            "data": data,
                            "hora": hora,
                        },
                    )
                    # These two operations run atomically in the same transaction
                except Exception as e:
                    return jsonify({"message": str(e), "status": "error"}), 400
                else:
                    # COMMIT is executed at the end of the block.
                    # The connection is in idle state again.
                    log.debug(f"Deleted {cur.rowcount} rows.")
    # The connection is returned to the pool at the end of the `connection()` context

    return (
        jsonify(
            {
                "message": f"Consulta no dia {data} às {hora} foi cancelada com sucesso",
                "status": "success",
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run()
