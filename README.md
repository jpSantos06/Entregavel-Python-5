# Sistema de Análise e Validação de Dados


1. Descrição do projeto

Este projeto foi desenvolvido em Python para analisar arquivos CSV, validar dados com expressões regulares (Regex) e aplicar tratamento de exceções.

O sistema verifica os seguintes campos:

E-mail
CPF
Telefone
Data

Após a análise, os registos são classificados como válidos ou inválidos, sendo gerado um relatório com as estatísticas.

2. Objetivos
Praticar a manipulação de arquivos CSV.
Utilizar o módulo re para validar dados.
Aplicar try, except, else e finally.
Criar uma exceção personalizada.
Gerar relatórios formatados com f-strings.
Praticar a organização de projetos no GitHub.
3. Tecnologias utilizadas
Python 3
Módulo csv
Módulo re
Módulo datetime
Git e GitHub

Não é necessário instalar bibliotecas externas.

4. Validações com Regex
E-mail

Padrão utilizado:

^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$


Justificativa:

^ indica o início da string.
$ indica o final da string.
\w representa caracteres alfanuméricos e underscore.
+ indica uma ou mais ocorrências.
@ verifica a presença do separador do e-mail.
\. representa um ponto literal.
CPF

Padrão utilizado:

\d{11}


Justificativa:

\d representa um algarismo.
{11} exige exatamente onze algarismos.

O programa também verifica os dígitos verificadores do CPF e rejeita sequências compostas pelo mesmo algarismo.

Telefone

O padrão aceita números com DDD e formatos comuns de telefone brasileiro, incluindo espaços, parênteses e hífen.

Metacaracteres utilizados:

\d: algarismos.
?: ocorrência opcional.
^ e $: delimitam o início e o final.
(?:...): agrupa alternativas sem criar um grupo de captura.
Data

Padrão utilizado:

\d{2}/\d{2}/\d{4}


O padrão exige o formato DD/MM/AAAA.

Além da expressão regular, a função datetime.strptime() verifica se a data existe no calendário. Por exemplo, 31/02/2001 é inválida.

5. Tratamento de exceções
FileNotFoundError

Ocorre quando o arquivo CSV indicado não existe. O programa informa o erro e encerra a análise do arquivo.

ValueError

É tratado quando o CSV está vazio ou sem cabeçalho, quando existem colunas extras numa linha ou quando uma conversão de data não é possível.

KeyError

É utilizado para identificar colunas obrigatórias ausentes, como email, cpf, telefone ou data.

FormatoInvalidoError

É uma exceção personalizada que representa registos cujos campos não cumprem as regras de validação do projeto.

else e finally

O bloco else informa que a leitura foi concluída com sucesso ou que o relatório foi gravado.

O bloco finally apresenta uma mensagem de finalização, independentemente de ocorrer um erro.

6. Exemplo de entrada

Arquivo dados.csv:

email,cpf,telefone,data
ana.silva@email.com,52998224725,11987654321,15/05/2000
joao@email,12345678900,11987654321,31/02/2001

7. Exemplo de saída
========== RELATORIO FINAL ==========
Total de registros analisados: 2
Registros validos: 1
Registros invalidos: 1
Percentual de aprovacao: 50.00%

--- Registros validos ---
E-mail: ana.silva@email.com | CPF: 52998224725 | ...

--- Registros invalidos ---
Linha 3: joao@email | Motivo: Campos invalidos: email, data
=====================================
