import sqlite3
import csv
import os
import random

def criar_tabela():
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS especies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            local TEXT NOT NULL,
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    conn.close()

def menu():
    print("\nMenu:")
    print("1. Adicionar espécie invasora")
    print("2. Visualizar todas as espécies")
    print("3. Editar espécie")
    print("4. Remover espécie")
    print("5. Pesquisar espécie")
    print("6. Exportar para CSV")
    print("7. Importar do CSV")
    print("8. Limpar banco de dados")
    print("9. Sair")

def coordenadas(local):
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return latitude, longitude

def adicionar():
    especie = input("Digite o nome da espécie invasora: ").strip().title()
    local = input("Digite o local onde a espécie foi vista: ").strip().title()
    latitude, longitude = coordenadas(local)
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO especies (nome, local, latitude, longitude)
        VALUES (?, ?, ?, ?)
    ''', (especie, local, latitude, longitude))
    conn.commit()
    conn.close()
    print(f"Espécie {especie} adicionada no local {local} (Latitude: {latitude}, Longitude: {longitude}).")

def visualizar():
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, local, latitude, longitude FROM especies')
    especies = cursor.fetchall()
    conn.close()
    if not especies:
        print("Nenhuma espécie invasora registrada.")
    else:
        especies_dict = {}
        for nome, local, latitude, longitude in especies:
            if nome in especies_dict:
                especies_dict[nome].append((local, latitude, longitude))
            else:
                especies_dict[nome] = [(local, latitude, longitude)]
        for nome, locais in especies_dict.items():
            print(f"Espécie: {nome}")
            for local, latitude, longitude in locais:
                print(f"  - Local: {local} (Latitude: {latitude}, Longitude: {longitude})")

def editar():
    especie = input("Digite o nome da espécie a ser editada: ").strip().title()
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM especies WHERE nome = ?', (especie,))
    resultado = cursor.fetchall()
    if not resultado:
        print(f"Espécie {especie} não encontrada.")
        conn.close()
        return
    novos_locais = input("Digite os novos locais onde a espécie foi vista (separados por vírgulas): ").strip().title().split(',')
    cursor.execute('DELETE FROM especies WHERE nome = ?', (especie,))
    for local in novos_locais:
        latitude, longitude = coordenadas(local)
        cursor.execute('INSERT INTO especies (nome, local, latitude, longitude) VALUES (?, ?, ?, ?)', (especie, local.strip(), latitude, longitude))
    conn.commit()
    conn.close()
    print(f"Locais da espécie {especie} atualizados.")

def remover():
    especie = input("Digite o nome da espécie a ser removida: ").strip().title()
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM especies WHERE nome = ?', (especie,))
    if cursor.rowcount == 0:
        print(f"Espécie {especie} não encontrada.")
        conn.close()
        return
    else:
        print(f"Espécie {especie} e todos os locais associados foram removidos.")
    
    conn.commit()
    conn.close()

def pesquisar():
    criterio = input("Digite o critério de pesquisa (nome ou local): ").strip().title()
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome, local, latitude, longitude FROM especies WHERE nome = ? OR local = ?', (criterio, criterio))
    resultado = cursor.fetchall()
    conn.close()
    if not resultado:
        print("Nenhuma espécie encontrada com o critério fornecido.")
    else:
        especies_dict = {}
        for nome, local, latitude, longitude in resultado:
            if nome in especies_dict:
                especies_dict[nome].append((local, latitude, longitude))
            else:
                especies_dict[nome] = [(local, latitude, longitude)]
        for nome, locais in especies_dict.items():
            print(f"Espécie: {nome}")
            for local, latitude, longitude in locais:
                print(f"  - Local: {local} (Latitude: {latitude}, Longitude: {longitude})")

def exportar_csv():
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM especies')
    especies = cursor.fetchall()
    conn.close()

    nome_arquivo = 'especies_invasoras.csv'
    with open(nome_arquivo, 'w', newline='') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerow(['id', 'nome', 'local', 'latitude', 'longitude'])
        escritor_csv.writerows(especies)
    print(f"Dados exportados para {nome_arquivo}.")

def importar_csv():
    nome_arquivo = 'especies_invasoras.csv'
    if not os.path.exists(nome_arquivo):
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return

    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    with open(nome_arquivo, 'r') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        next(leitor_csv)  # Pular o cabeçalho
        for row in leitor_csv:
            cursor.execute('''
                INSERT INTO especies (nome, local, latitude, longitude)
                VALUES (?, ?, ?, ?)
            ''', (row[1], row[2], row[3], row[4]))  # Exclui o id (row[0])
    conn.commit()
    conn.close()
    print(f"Dados importados do {nome_arquivo}.")

def limpar_banco_de_dados():
    conn = sqlite3.connect('especies_invasoras.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM especies')
    conn.commit()
    conn.close()
    print("Banco de dados limpo.")

def main():
    criar_tabela()
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            adicionar()
            break
        elif opcao == '2':
            visualizar()
            break
        elif opcao == '3':
            editar()
            break
        elif opcao == '4':
            remover()
            break
        elif opcao == '5':
            pesquisar()
            break
        elif opcao == '6':
            exportar_csv()
            break
        elif opcao == '7':
            importar_csv()
            break
        elif opcao == '8':
            limpar_banco_de_dados()
            break
        elif opcao == '9':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
