import random
from datetime import date, timedelta
import itertools
from datetime import datetime

codigo_sns = 0
generated_NIFs = set()
generated_SSN = set()
generated_names = set()
medicos = []
pacientes = []
enfermeiros = []
trabalha = []
consultas = []
consultas_medicos = []
possible_hours = [f"{i}:00" for i in range(8, 13)] + [f"{i}:00" for i in range(14, 19)]
medicamentos = ["xanax", "valium", "paracetamol", "ibuprofeno", "brufen", "codeina"]
first_names = [
    "José",
    "Marta",
    "Carlos",
    "Sofia",
    "Inês",
    "Maria",
    "João",
    "Ana",
    "Manuel",
    "Rita",
    "Beatriz",
    "Daniel",
    "Eduardo",
    "Fernanda",
    "Gabriel",
    "Helena",
    "Isabela",
    "Karina",
    "Leonardo",
    "Nuno",
    "Olivia",
    "Pedro",
    "Quirino",
    "Raquel",
    "Thiago",
    "Ursula",
    "Vinícius",
    "William",
    "Xavier",
    "Yara",
    "Zeca",
    "Alice",
    "Bruno",
    "Clara",
    "Diego",
    "Elisa",
    "Felipe",
    "Giovana",
    "Hugo",
    "Irene",
    "Júlio",
    "Kátia",
    "Lucas",
    "Nelson",
    "Otávio",
    "Paula",
    "Renato",
    "Silvia",
    "Tomás",
    "Vera",
    "Wagner",
    "Yasmin",
    "Zuleica",
    "Amanda",
    "Caio",
    "Diana",
    "Enzo",
    "Flávia",
    "Gustavo",
    "Heloísa",
    "Igor",
    "Janaina",
    "Kleber",
    "Lúcia",
    "Natália",
    "Oscar",
    "Patrícia",
    "Roberta",
    "Samuel",
    "Tânia",
    "Vítor",
    "Wesley",
    "Ximena",
    "Yolanda",
    "Zeferino",
    "Bianca",
    "Cristiano",
    "Débora",
    "Elias",
    "Fábio",
    "Graziela",
    "Henrique",
    "Isabel",
    "Josué",
    "Kelly",
    "Leandro",
    "Milena",
    "Noemi",
    "Orlando",
    "Priscila",
    "Rodrigo",
    "Sabrina",
    "Telma",
    "Ulisses",
    "Vanessa",
    "Wallace",
    "Xuxa",
    "Yuri",
    "Zoraide",
    "Arthur",
    "Cecília",
    "David",
    "Esther",
    "Melissa",
]
last_names = [
    "Santos",
    "Silva",
    "Pereira",
    "Costa",
    "Ferreira",
    "Gomes",
    "Rodrigues",
    "Martins",
    "Moreira",
    "Almeida",
    "Santo",
    "Silvinho",
    "Pereirinha",
    "Costinha",
    "Ferreirinha",
    "Gominho",
    "Rodriguinho",
    "Martinho",
    "Moreirinha",
    "Almeidinha",
    "San",
    "Silvano",
    "Pereirão",
    "Costão",
    "Ferreirão",
    "Gominho",
    "Rodrigão",
    "Martin",
    "Moreirão",
    "Almeidão",
    "Santoca",
    "Silvinha",
    "Pereirinha",
    "Costinha",
    "Ferreirinha",
    "Gominha",
    "Rodriguinho",
    "Martinha",
    "Moreirinha",
    "Almeidinha",
    "Santinho",
    "Silvinho",
    "Pereirinha",
    "Costinha",
    "Ferreirinha",
    "Gominho",
    "Rodriguinho",
    "Martinho",
    "Moreirinha",
    "Almeidinha",
    "Santonio",
    "Silvinio",
    "Pereirio",
    "Costio",
    "Ferreirio",
    "Gomio",
    "Rodriguio",
    "Martio",
    "Moreirio",
    "Almeidio",
    "Santovski",
    "Silvinski",
    "Pereirski",
    "Costinski",
    "Ferreirski",
    "Gominski",
    "Rodriginski",
    "Martinski",
    "Moreirski",
    "Almeidinski",
    "Santinho",
    "Silvinho",
    "Pereirinha",
    "Costinha",
    "Ferreirinha",
    "Gominho",
    "Rodriguinho",
    "Martinho",
    "Moreirinha",
    "Almeidinha",
    "San",
    "Silvinho",
    "Pereirinha",
    "Costinha",
    "Ferreirinha",
    "Gominho",
    "Rodriguinho",
    "Martinho",
    "Moreirinha",
    "Almeidinha",
    "Sant",
    "Silva",
    "Pereira",
    "Costa",
    "Ferreira",
    "Gomes",
    "Rodrigues",
    "Martins",
    "Moreira",
    "Almeida",
]
ruas = [
    "Rua de Santo Antonio",
    "Avenida da Liberdade",
    "Rua Direita",
    "Rua Nova",
    "Travessa do Sol",
    "Rua das Flores",
    "Avenida dos Aliados",
    "Rua do Comércio",
    "Rua dos Douradores",
    "Praça do Rossio",
    "Rua da Boavista",
    "Avenida Dom Afonso Henriques",
    "Rua da Constituição",
    "Travessa dos Cedros",
    "Rua dos Carvalhos",
    "Avenida João XXI",
    "Rua da Paz",
    "Praça da República",
    "Avenida General Humberto Delgado",
    "Rua da Alegria",
    "Rua dos Cedros",
    "Avenida Dom João IV",
    "Travessa das Oliveiras",
    "Rua do Salgueiral",
    "Praça das Flores",
    "Avenida da Boavista",
    "Rua das Rosas",
    "Rua de São João",
    "Avenida Central",
    "Travessa do Alecrim",
    "Rua do Ouro",
    "Avenida Almirante Reis",
    "Rua do Cais",
    "Rua do Sol",
    "Praça da Liberdade",
    "Avenida dos Combatentes",
    "Rua da Sé",
    "Rua dos Cedros",
    "Avenida Engenheiro Duarte Pacheco",
    "Travessa das Laranjeiras",
    "Rua das Oliveiras",
    "Avenida das Acácias",
    "Rua do Castelo",
    "Rua do Souto",
    "Praça da Rainha",
    "Avenida dos Descobrimentos",
    "Rua do Poço",
    "Rua dos Limoeiros",
    "Avenida da República",
    "Travessa do Ferreiro",
    "Rua das Pedras",
    "Avenida dos Moinhos",
    "Rua do Ribeiro",
    "Rua da Fonte",
    "Praça da Batalha",
    "Avenida dos Louros",
    "Rua do Pinhal",
    "Rua dos Carreiros",
    "Avenida das Oliveiras",
    "Travessa dos Pinheiros",
    "Rua das Laranjeiras",
    "Avenida das Rosas",
    "Rua dos Pescadores",
    "Rua do Sobreiro",
    "Praça da Estrela",
    "Avenida dos Carvalhos",
    "Rua do Lago",
    "Rua das Glicínias",
    "Avenida do Mar",
    "Travessa do Beco",
    "Rua dos Narcisos",
    "Avenida das Águias",
    "Rua da Fontinha",
    "Rua da Cruz",
    "Praça do Castelo",
    "Avenida das Violetas",
    "Rua do Monte",
    "Rua do Pomar",
    "Avenida dos Castanheiros",
    "Travessa das Margaridas",
    "Rua das Orquídeas",
    "Avenida das Borboletas",
    "Rua da Cidade",
    "Rua do Campo",
    "Praça do Poder",
    "Avenida das Amendoeiras",
    "Rua das Figueiras",
    "Rua dos Ciprestes",
    "Avenida do Sol",
    "Travessa do Olival",
    "Rua das Acácias",
    "Avenida dos Plátanos",
    "Rua do Jardim",
    "Rua do Açude",
    "Praça do Mercado",
]
cidades = [
    "Lisboa",
    "Sintra",
    "Amadora",
    "Oeiras",
    "Cascais",
    "Loures",
    "Odivelas",
    "Vila Franca de Xira",
    "Almada",
    "Seixal",
    "Barreiro",
    "Mafra",
    "Torres Vedras",
    "Moita",
    "Montijo",
    "Setúbal",
    "Alverca do Ribatejo",
    "Póvoa de Santa Iria",
    "Sacavém",
    "Queluz",
    "Agualva-Cacém",
    "Cacém",
    "Santo António dos Cavaleiros",
    "Moscavide",
    "Portela",
    "Algés",
    "Linda-a-Velha",
    "Carnaxide",
    "Queijas",
    "Carcavelos",
    "Parede",
    "Estoril",
    "Cascais",
    "Alcabideche",
    "Ericeira",
    "Malveira",
    "Mafra",
    "Azenhas do Mar",
    "Colares",
    "Queluz de Baixo",
    "Massamá",
    "Monte Abraão",
    "Belas",
    "Algueirão-Mem Martins",
    "Rio de Mouro",
    "Tapada das Mercês",
    "Vialonga",
    "Póvoa de Santo Adrião",
    "Camarate",
    "São João da Talha",
]
especialidades = [
    "ortopedia",
    "oftalmogia",
    "cardiologia",
    "pediatria",
    "reumatologia",
]
# Generate a list of all dates in 2023 and 2024
dates = [date(2023, 1, 1) + timedelta(days=i) for i in range(2 * 365 + 1)]
sintomas_c = [
    "Pressão arterial",
    "Frequência cardíaca",
    "Temperatura corporal",
    "Nível de glicose no sangue",
    "Saturação de oxigênio",
    "Frequência respiratória",
    "Índice de Massa Corporal",
    "Nível de colesterol",
    "Nível de triglicerídeos",
    "Hemoglobina",
    "Contagem de leucócitos",
    "Volume globular médio",
    "Nível de creatinina no sangue",
    "Taxa de filtração glomerular",
    "Nível de ácido úrico",
    "Nível de hemoglobina glicada",
    "Velocidade de sedimentação das hemácias",
    "Nível de bilirrubina",
    "pressão diastólica",
    "Capacidade vital forçada",
]
sintomas_s = [
    "Febre",
    "Tosse",
    "Dor de cabeça",
    "Náusea",
    "Vômito",
    "Fadiga",
    "Diarreia",
    "Dor abdominal",
    "Dor no peito",
    "Falta de ar",
    "Palpitações",
    "Tontura",
    "Vertigem",
    "Perda de apetite",
    "Sudorese",
    "Calafrios",
    "Insônia",
    "Cãibras",
    "Dor muscular",
    "Rigidez articular",
    "Coceira",
    "Erupção cutânea",
    "Inchaço",
    "Vermelhidão",
    "Icterícia",
    "Sangramento",
    "Hematúria",
    "Hemoptise",
    "Fotofobia",
    "Diplopia",
    "Zumbido no ouvido",
    "Perda de audição",
    "Alterações de humor",
    "Confusão mental",
    "Alucinações",
    "Convulsões",
    "Desmaio",
    "Tremores",
    "Perda de peso",
    "Ganho de peso",
    "Constipação",
    "Incontinência",
    "Ardência ao urinar",
    "Disfagia",
    "Disartria",
    "Dor de garganta",
    "Rouquidão",
    "Perda Sensibilidade",
    "Dor pescoço",
    "Dor costas",
]

clinics = [
    {
        "nome": "CUF - Alvalade",
        "telefone": 210001122,
        "morada": "Rua de Alvalade, 123, 1700-123 Lisboa",
    },
    {
        "nome": "CUF - Cascais",
        "telefone": 210001123,
        "morada": "Rua de Cascais, 12, 2750-123 Cascais",
    },
    {
        "nome": "CUF - Belem",
        "telefone": 210001124,
        "morada": "Rua de Belem, 1, 1300-123 Lisboa",
    },
    {
        "nome": "CUF - Mafra",
        "telefone": 210001125,
        "morada": "Rua de Mafra, 1, 2640-123 Mafra",
    },
    {
        "nome": "CUF - Descobertas",
        "telefone": 210001126,
        "morada": "Rua das Descobertas, 1, 1300-123 Lisboa",
    },
]


def generate_phone_number():
    phone_number = "9"
    phone_number += str(random.choice([2, 3, 6, 1]))
    for i in range(7):
        phone_number += str(random.randint(0, 9))
    return phone_number


def generate_name():
    while True:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        if (first_name, last_name) not in generated_names:
            generated_names.add((first_name, last_name))
            return first_name + " " + last_name


def generate_postal_code():
    postal_code = ""
    postal_code += str(random.randint(1000, 9999))
    postal_code += "-"
    postal_code += str(random.randint(100, 999))
    return postal_code


def generate_address():
    rua = random.choice(ruas)
    cidade = random.choice(cidades)
    numero = random.randint(1, 100)
    return f"{rua}, {numero}, {generate_postal_code()} {cidade}"


def generate_NIF():
    while True:
        NIF = random.randint(100000000, 999999999)
        if NIF not in generated_NIFs:
            generated_NIFs.add(NIF)
            return NIF


def generate_SSN():
    while True:
        SSN = random.randint(10000000000, 99999999999)
        if SSN not in generated_SSN:
            generated_SSN.add(SSN)
            return SSN


def generate_birth_date():
    year = random.randint(1975, 2020)
    month = random.randint(1, 12)
    days_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return f"{year}-{str(month).zfill(2)}-{str(random.randint(1, days_month[month-1])).zfill(2)}"


def generate_codigo_sns():
    global codigo_sns
    codigo_sns = codigo_sns + 1
    return str(codigo_sns).zfill(12)


def generate_clinics(f):
    f.write(
        """\n-------------------------------------
-- CLINICAS
-------------------------------------\n"""
    )
    clinics_data = []
    for clinic in clinics:
        clinics_data.append(
            f"('{clinic['nome']}', {clinic['telefone']}, '{clinic['morada']}')"
        )
    f.write("INSERT INTO clinica (nome, telefone, morada) VALUES\n")
    f.write(",\n".join(clinics_data))
    f.write(";")
    return len(clinics_data)


def generate_pacients(f):
    f.write(
        """\n-------------------------------------
-- PACIENTES
-------------------------------------\n"""
    )
    pacientes_data = []
    for i in range(5000):
        ssn = generate_SSN()
        nif = generate_NIF()
        name = generate_name()
        phone_number = generate_phone_number()
        address = generate_address()
        b_day = generate_birth_date()
        pacientes.append((ssn, nif, name, phone_number, address, b_day))
        pacientes_data.append(
            f"('{ssn}', '{nif}', '{name}', '{phone_number}', '{address}', '{b_day}')"
        )
    f.write("INSERT INTO paciente\nVALUES\n")
    f.write(",\n".join(pacientes_data))
    f.write(";")
    return len(pacientes_data)


def generate_enfermeiros(f):
    f.write(
        """\n-------------------------------------
-- ENFERMEIROS
-------------------------------------\n"""
    )
    enfermeiros_data = []
    for clinica in clinics:
        for i in range(5):
            nif = generate_NIF()
            name = generate_name()
            phone_number = generate_phone_number()
            address = generate_address()
            clinica_name = clinica["nome"]
            enfermeiros.append((nif, name, phone_number, clinica))
            enfermeiros_data.append(
                f"('{nif}', '{name}', '{phone_number}', '{address}', '{clinica_name}')"
            )
    f.write("INSERT INTO enfermeiro\nVALUES\n")
    f.write(",\n".join(enfermeiros_data))
    f.write(";")
    return len(enfermeiros_data)


def generate_medicos(f):
    f.write(
        """\n-------------------------------------
-- MEDICOS
-------------------------------------\n"""
    )
    medicos_data = []
    # A gerar os 20 médicos de Clinica Geral
    for i in range(20):
        nif = generate_NIF()
        name = generate_name()
        phone_number = generate_phone_number()
        address = generate_address()
        especialidade = "clínica geral"
        medicos.append((nif, name, phone_number, address, especialidade))
        medicos_data.append(
            f"('{nif}', '{name}', '{phone_number}', '{address}', '{especialidade}')"
        )
    # A gerar os restantes 40 medicos de outras especialidades
    for i in range(40):
        nif = generate_NIF()
        name = generate_name()
        phone_number = generate_phone_number()
        address = generate_address()
        especialidade = random.choice(especialidades)
        medicos.append((nif, name, phone_number, address, especialidade))
        medicos_data.append(
            f"('{nif}', '{name}', '{phone_number}', '{address}', '{especialidade}')"
        )
    f.write("INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES\n")
    f.write(",\n".join(medicos_data))
    f.write(";")
    return len(medicos_data)


def generate_trabalha(f):
    f.write(
        """\n-------------------------------------
-- TRABALHA
-------------------------------------\n"""
    )
    days_week = [0, 1, 2, 3, 4, 5, 6]
    medico_cycle = itertools.cycle(medicos)
    trabalha_data = []
    # A atribuir 8 médicos a cada clínica para cada dia da semana
    for day in days_week:
        for clinica in clinics:
            for i in range(8):
                med = next(medico_cycle)
                trabalha.append((med[0], clinica["nome"], day))
                trabalha_data.append(f"('{med[0]}', '{clinica['nome']}', {day})")
    f.write("INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES\n")
    f.write(",\n".join(trabalha_data))
    f.write(";")
    return len(trabalha_data)


def generate_consultas(f):
    f.write(
        """\n-------------------------------------
-- CONSULTAS
-------------------------------------\n"""
    )
    paciente_cycle = itertools.cycle(pacientes)
    consultas_data = []
    for current_date in dates:
        day_of_week = current_date.weekday()
        # Transformar pythonn week day (Monday - 0) to postgres weekday (Monday 1)
        day_of_week = (day_of_week + 1) % 7
        # precorrer todas as clinicas a cada dia
        for clinic in clinics:
            doctors_working_today = [
                t for t in trabalha if t[1] == clinic["nome"] and t[2] == day_of_week
            ]
            # A Adicionar 20 consultas por dia (8 médicos a cada dia, e têm de ter 2 consultas por dia = 16)
            for _ in range(20):
                # Get the list of doctors working in each clinic on this day
                # Select a random doctor from the list of doctors working today
                paci = next(paciente_cycle)
                doctor = random.choice(doctors_working_today)
                # iterar até encontrar uma hora que não esteja ocupada
                loop_check = 0
                # confirmando que o mesmo medico não tem consulta no mesmo dia à mesma hora. Caso tenha, escolhe outra hora
                while True:
                    loop_check += 1
                    hour = random.choice(possible_hours)
                    if ((doctor[0], current_date, hour)) not in consultas_medicos:
                        break
                    if loop_check > 20:
                        # print("Getting new doctor")
                        doctor = random.choice(doctors_working_today)
                        loop_check = 0
                sns_code = generate_codigo_sns()
                # A guardar a consulta gerada para utilizar mais tarde (sintomas e receitas)
                consultas.append(
                    (
                        paci[0],
                        doctor[0],
                        clinic["nome"],
                        current_date,
                        hour,
                        sns_code,
                    )
                )
                # A guardar a consulta gerada para não repetir os dados
                consultas_medicos.append((doctor[0], current_date, hour))
                consultas_data.append(
                    f"('{paci[0]}', '{doctor[0]}', '{clinic['nome']}', '{current_date}', '{hour}:00', '{sns_code}')"
                )
    f.write("INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES\n")
    f.write(",\n".join(consultas_data))
    f.write(";")
    return len(consultas_data)


def generate_receitas(f):
    f.write(
        """\n-------------------------------------
-- RECEITAS
-------------------------------------\n"""
    )
    # A calcular o numero de consultas para chegar à cobertura de 80%
    consultas_passado = [
        consulta
        for consulta in consultas
        if datetime.combine(
            consulta[3],
            datetime.strptime(consulta[4], "%H:%M").time(),
        )
        < datetime.now()
    ]
    range_i = len(consultas_passado) * 0.8
    new_consultas = consultas_passado.copy()
    receitas_data = []
    # iterar 80% das consultas
    for i in range(int(range_i)):
        # escolher uma consulta aleatória
        consulta = random.choice(new_consultas)
        # remover a consulta escolhida da lista de consultas para não voltar a ser escolhida
        new_consultas.remove(consulta)
        # gerar um número aleatório de medicamentos entre 1 e 6
        random_medi_number = random.randint(1, 6)
        new_medicamento = medicamentos.copy()
        # iterar o número de medicamentos gerados
        for _ in range(random_medi_number):
            # escolher um medicamento aleatório da lista de medicamentos
            medicamento = random.choice(new_medicamento)
            # remover o medicamento escolhido da lista de medicamentos para não voltar a ser escolhido
            new_medicamento.remove(medicamento)
            # gerar uma quantidade aleatória de medicamentos entre 1 e 3
            quantidade = random.randint(1, 3)
            # f.write(
            #     f"INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES ('{consulta[5]}', '{medicamento}', {quantidade});\n"
            # )
            receitas_data.append(f"('{consulta[5]}', '{medicamento}', {quantidade})")
    f.write("INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES\n")
    f.write(",\n".join(receitas_data))
    f.write(";")
    return len(receitas_data)


def generate_sintomas(f):
    f.write(
        """\n-------------------------------------
-- SINTOMAS
-------------------------------------\n"""
    )
    # iterar todas as consultas uma vez que todas as consultas t^`em de ter pelo menos 1 sintoma`
    consultas_passado = [
        consulta
        for consulta in consultas
        if datetime.combine(
            consulta[3],
            datetime.strptime(consulta[4], "%H:%M").time(),
        )
        < datetime.now()
    ]
    sintomas_data = []
    sintoma_sem_data = []
    for consulta in consultas_passado:
        # A gerar o numero de sintomas com valor
        sintoma_com_valor = random.randint(0, 3)
        # A gerar o numero de sintommas sem calor e apenas com parametro
        sintoma_sem_valor = random.randint(1, 5)
        new_sintoma_c = sintomas_c.copy()
        new_sintoma_s = sintomas_s.copy()
        # A gerar sintomas sem valor
        for _ in range(sintoma_sem_valor):
            sintoma = random.choice(new_sintoma_s)
            new_sintoma_s.remove(sintoma)
            sintoma_sem_data.append(f"('{consulta[5]}', '{sintoma}')")
        # A gerar sintomas com valor
        for _ in range(sintoma_com_valor):
            sintoma = random.choice(new_sintoma_c)
            # A gerar o valor do sintoma
            quantidade = random.randint(1, 100)
            new_sintoma_c.remove(sintoma)
            sintomas_data.append(f"('{consulta[5]}', '{sintoma}', {quantidade})")
    f.write("INSERT INTO observacao (id, parametro, valor) VALUES\n")
    f.write(",\n".join(sintomas_data))
    f.write(";")
    f.write("INSERT INTO observacao (id, parametro) VALUES\n")
    f.write(",\n".join(sintoma_sem_data))
    f.write(";")
    return len(sintomas_data) + len(sintoma_sem_data)


with open("populate.sql", "w", encoding="utf-8") as f:
    print("Generating clinics...")
    print(generate_clinics(f))
    print("Generating enfermeiros")
    print(generate_enfermeiros(f))
    print("Generating medicos")
    print(generate_medicos(f))
    print("Generating pacients")
    print(generate_pacients(f))
    # Relações
    print("Generating trabalha")
    print(generate_trabalha(f))
    print("Generating consultas")
    print(generate_consultas(f))
    print("Generating receitas")
    print(generate_receitas(f))
    print("Generating sintomas")
    print(generate_sintomas(f))
