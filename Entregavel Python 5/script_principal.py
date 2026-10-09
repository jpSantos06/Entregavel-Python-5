import csv
import re
from datetime import datetime


# Excecao personalizada
class FormatoInvalidoError(Exception):
    """Excecao para dados que nao respeitam as regras do projeto."""
    pass


# 1. Validacao de e-mail
def validar_email(email):
    padrao = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
    return re.fullmatch(padrao, email) is not None


# 2. Validacao de CPF
def validar_cpf(cpf):
    # Aceita CPF com ou sem pontuacao.
    digitos = re.sub(r"\D", "", cpf)

    if not re.fullmatch(r"\d{11}", digitos):
        return False

    # Rejeita CPFs com todos os digitos iguais.
    if digitos == digitos[0] * 11:
        return False

    # Calcula o primeiro digito verificador.
    soma = sum(int(digitos[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    primeiro = 0 if resto == 10 else resto

    if primeiro != int(digitos[9]):
        return False

    # Calcula o segundo digito verificador.
    soma = sum(int(digitos[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    segundo = 0 if resto == 10 else resto

    return segundo == int(digitos[10])


# 3. Validacao de telefone brasileiro
def validar_telefone(telefone):
    # Aceita 10 ou 11 digitos, com DDD.
    padrao = r"^(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9?\d{4})-?\d{4}$"
    return re.fullmatch(padrao, telefone) is not None


# 4. Validacao de data no formato DD/MM/AAAA
def validar_data(data):
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", data):
        return False

    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


# 5. Validacao completa de um registro
def validar_registro(registro):
    resultados = {
        "email": validar_email(registro["email"].strip()),
        "cpf": validar_cpf(registro["cpf"].strip()),
        "telefone": validar_telefone(registro["telefone"].strip()),
        "data": validar_data(registro["data"].strip())
    }

    # Regra de negocio: todos os campos devem ser validos.
    if not all(resultados.values()):
        campos_invalidos = [
            campo for campo, valido in resultados.items()
            if not valido
        ]

        raise FormatoInvalidoError(
            "Campos invalidos: " + ", ".join(campos_invalidos)
        )

    return True


# 6. Leitura e analise do CSV
def analisar_arquivo(nome_arquivo):
    registros_validos = []
    registros_invalidos = []

    try:
        with open(nome_arquivo, "r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            colunas_obrigatorias = {
                "email", "cpf", "telefone", "data"
            }

            if leitor.fieldnames is None:
                raise ValueError("O arquivo CSV esta vazio ou sem cabecalho.")

            colunas = set(leitor.fieldnames)
            faltantes = colunas_obrigatorias - colunas

            if faltantes:
                raise KeyError(
                    "Colunas ausentes: " + ", ".join(sorted(faltantes))
                )

            for numero_linha, registro in enumerate(leitor, start=2):
                try:
                    if None in registro:
                        raise ValueError("Existem colunas extras na linha.")

                    validar_registro(registro)
                    registros_validos.append(registro)

                except FormatoInvalidoError as erro:
                    registro["motivo"] = str(erro)
                    registro["linha"] = str(numero_linha)
                    registros_invalidos.append(registro)

                except (ValueError, KeyError) as erro:
                    registro["motivo"] = str(erro)
                    registro["linha"] = str(numero_linha)
                    registros_invalidos.append(registro)

    except FileNotFoundError:
        print(f"Erro: o arquivo '{nome_arquivo}' nao foi encontrado.")
        return None

    except (KeyError, ValueError) as erro:
        print(f"Erro na estrutura do arquivo: {erro}")
        return None

    except OSError as erro:
        print(f"Erro ao ler o arquivo: {erro}")
        return None

    else:
        print("Leitura e analise do arquivo concluidas.")
        return registros_validos, registros_invalidos

    finally:
        print("Operacao de leitura finalizada.")


# 7. Geracao do relatorio CSV
def gerar_relatorio(registros_validos, registros_invalidos):
    try:
        with open(
            "relatorio.csv",
            "w",
            encoding="utf-8",
            newline=""
        ) as arquivo:
            campos = [
                "status", "email", "cpf", "telefone",
                "data", "linha", "motivo"
            ]

            escritor = csv.DictWriter(
                arquivo,
                fieldnames=campos,
                extrasaction="ignore"
            )

            escritor.writeheader()

            for registro in registros_validos:
                escritor.writerow({
                    **registro,
                    "status": "Valido",
                    "linha": "",
                    "motivo": ""
                })

            for registro in registros_invalidos:
                escritor.writerow({
                    **registro,
                    "status": "Invalido"
                })

    except OSError as erro:
        print(f"Erro ao salvar o relatorio: {erro}")
        return

    else:
        print("Relatorio salvo em relatorio.csv.")

    finally:
        print("Processo de geracao do relatorio finalizado.")


# 8. Relatorio final formatado
def exibir_relatorio(resultado):
    if resultado is None:
        return

    validos, invalidos = resultado
    total = len(validos) + len(invalidos)

    print("\n========== RELATORIO FINAL ==========")
    print(f"Total de registros analisados: {total}")
    print(f"Registros validos: {len(validos)}")
    print(f"Registros invalidos: {len(invalidos)}")

    if total > 0:
        percentual = len(validos) / total * 100
        print(f"Percentual de aprovacao: {percentual:.2f}%")

    print("\n--- Registros validos ---")
    for registro in validos:
        print(
            f"E-mail: {registro['email']} | "
            f"CPF: {registro['cpf']} | "
            f"Telefone: {registro['telefone']} | "
            f"Data: {registro['data']}"
        )

    print("\n--- Registros invalidos ---")
    for registro in invalidos:
        print(
            f"Linha {registro.get('linha', '?')}: "
            f"{registro.get('email', '(sem e-mail)')} | "
            f"Motivo: {registro.get('motivo', 'Erro desconhecido')}"
        )

    print("=====================================")


# 9. Programa principal
def main():
    nome_arquivo = input(
        "Nome do arquivo CSV (ex.: dados.csv): "
    ).strip()

    resultado = analisar_arquivo(nome_arquivo)

    if resultado is not None:
        validos, invalidos = resultado
        gerar_relatorio(validos, invalidos)
        exibir_relatorio(resultado)


if __name__ == "__main__":
    main()