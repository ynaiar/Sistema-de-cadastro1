from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
import os


# Carregar variáveis de ambiente
load_dotenv()

# Configurar Supavisor (pooler de transações do Supabase)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres.nxfvcknoecdruyfabsqw:1Mingau*@aws-0-sa-east-1.pooler.supabase.com:6543/postgres")

if not DATABASE_URL:
    raise ValueError("Erro: DATABASE_URL não está definida no .env")

# Criar pool de conexões
try:
    connection_pool = SimpleConnectionPool(5, 20, dsn=DATABASE_URL)
except Exception as e:
    raise RuntimeError(f"Erro ao conectar ao banco de dados: {e}")

def get_db_connection():
    """ Obtém uma conexão do pool """
    return connection_pool.getconn()

def release_db_connection(conn):
    """ Devolve a conexão para o pool """
    connection_pool.putconn(conn)

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_flash_messages'  # Necessário para mensagens flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        endereco = request.form.get('endereco')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')
        telefone = request.form.get('telefone')
        email = request.form.get('email')

        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Inserir contato e obter ID
            cur.execute(
                "INSERT INTO Contato (numerotelefone, email) VALUES (%s, %s) RETURNING IdContato",
                (telefone, email)
            )
            contato_id = cur.fetchone()[0]
            
            # Inserir cliente
            cur.execute(
                "INSERT INTO cliente (nome, sobrenome, endereco, bairro, cidade, uf, fkcontatoid) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nome, sobrenome, endereco, bairro, cidade, uf, contato_id)
            )
            
            conn.commit()
            cur.close()
            flash('Cliente cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao cadastrar cliente: {e}', 'danger')
        finally:
            release_db_connection(conn)
        
        return redirect(url_for('index'))
    
    return render_template('cadastrar_cliente.html')

@app.route('/cadastrar-colaboradores', methods=['GET', 'POST'])
def cadastrar_colaboradores():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        data_nascimento = request.form.get('data_nascimento')
        carteira_trabalho = request.form.get('carteira_trabalho')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        uf = request.form.get('uf')

        conn = get_db_connection()
        try:
            cur = conn.cursor()
            
            # Inserir contato e obter ID
            cur.execute(
                "INSERT INTO Contato (Numero_telefone, Email) VALUES (%s, %s) RETURNING IdContato",
                (telefone, email)
            )
            contato_id = cur.fetchone()[0]
            
            # Inserir colaborador
            cur.execute(
                "INSERT INTO Colaborador (Nome, Sobrenome, Data_nascimento, Numero_carteira_trabalho, Endereco, Bairro, Cidade, UF, fkContatoID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nome, sobrenome, data_nascimento, carteira_trabalho, endereco, bairro, cidade, uf, contato_id)
            )
            
            conn.commit()
            cur.close()
            flash('Colaborador cadastrado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao cadastrar colaborador: {e}', 'danger')
        finally:
            release_db_connection(conn)
        
        return redirect(url_for('index'))
    
    return render_template('cadastrar_colaboradores.html')

if __name__ == '__main__':
    app.run(debug=True)
