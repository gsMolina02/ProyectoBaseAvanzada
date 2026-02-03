from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'pichincha_secret_key_2024'

# URL del backend
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000/api')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cedula = request.form.get('cedula')
        
        try:
            # Buscar cliente por cédula
            response = requests.get(f'{BACKEND_URL}/clientes')
            clientes = response.json()
            
            cliente = next((c for c in clientes if c['cedula'] == cedula), None)
            
            if cliente:
                session['cliente_id'] = cliente['id']
                session['cliente_nombre'] = f"{cliente['nombre']} {cliente['apellido']}"
                return redirect(url_for('dashboard'))
            else:
                flash('Cliente no encontrado. Por favor, regístrese.', 'error')
                return redirect(url_for('registro'))
        except Exception as e:
            flash(f'Error al conectar con el servidor: {str(e)}', 'error')
    
    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        data = {
            'cedula': request.form.get('cedula'),
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'email': request.form.get('email'),
            'telefono': request.form.get('telefono')
        }
        
        try:
            response = requests.post(f'{BACKEND_URL}/clientes', json=data)
            
            if response.status_code == 201:
                cliente = response.json()
                flash('Registro exitoso. Ahora puede iniciar sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash(response.json().get('error', 'Error al registrar cliente'), 'error')
        except Exception as e:
            flash(f'Error al conectar con el servidor: {str(e)}', 'error')
    
    return render_template('registro.html')


@app.route('/dashboard')
def dashboard():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Obtener cuentas del cliente
        response = requests.get(f'{BACKEND_URL}/cuentas?cliente_id={session["cliente_id"]}')
        cuentas = response.json()
        
        return render_template('dashboard.html', 
                             cliente_nombre=session['cliente_nombre'],
                             cuentas=cuentas)
    except Exception as e:
        flash(f'Error al cargar datos: {str(e)}', 'error')
        return render_template('dashboard.html', 
                             cliente_nombre=session['cliente_nombre'],
                             cuentas=[])


@app.route('/transferir', methods=['GET', 'POST'])
def transferir():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'cuenta_origen': request.form.get('cuenta_origen'),
            'cuenta_destino': request.form.get('cuenta_destino'),
            'monto': float(request.form.get('monto')),
            'tipo_transferencia': request.form.get('tipo_transferencia'),
            'concepto': request.form.get('concepto')
        }
        
        try:
            response = requests.post(f'{BACKEND_URL}/transferencias', json=data)
            
            if response.status_code == 201:
                transferencia = response.json()
                flash(f'Transferencia exitosa. Referencia: {transferencia["referencia"]}', 'success')
                return redirect(url_for('comprobante', id=transferencia['id']))
            else:
                flash(response.json().get('error', 'Error al realizar transferencia'), 'error')
        except Exception as e:
            flash(f'Error al conectar con el servidor: {str(e)}', 'error')
    
    try:
        # Obtener cuentas del cliente
        response = requests.get(f'{BACKEND_URL}/cuentas?cliente_id={session["cliente_id"]}')
        cuentas = response.json()
        
        return render_template('transferir.html', 
                             cliente_nombre=session['cliente_nombre'],
                             cuentas=cuentas)
    except Exception as e:
        flash(f'Error al cargar datos: {str(e)}', 'error')
        return render_template('transferir.html', 
                             cliente_nombre=session['cliente_nombre'],
                             cuentas=[])


@app.route('/historial')
def historial():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    try:
        # Obtener cuentas del cliente
        response_cuentas = requests.get(f'{BACKEND_URL}/cuentas?cliente_id={session["cliente_id"]}')
        cuentas = response_cuentas.json()
        
        # Obtener transferencias de todas las cuentas del cliente
        todas_transferencias = []
        for cuenta in cuentas:
            response = requests.get(f'{BACKEND_URL}/transferencias?cuenta_id={cuenta["id"]}')
            transferencias = response.json()
            todas_transferencias.extend(transferencias)
        
        # Ordenar por fecha
        todas_transferencias.sort(key=lambda x: x['fecha_transferencia'], reverse=True)
        
        return render_template('historial.html', 
                             cliente_nombre=session['cliente_nombre'],
                             transferencias=todas_transferencias)
    except Exception as e:
        flash(f'Error al cargar historial: {str(e)}', 'error')
        return render_template('historial.html', 
                             cliente_nombre=session['cliente_nombre'],
                             transferencias=[])


@app.route('/comprobante/<int:id>')
def comprobante(id):
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.get(f'{BACKEND_URL}/transferencias/{id}')
        transferencia = response.json()
        
        return render_template('comprobante.html', 
                             cliente_nombre=session['cliente_nombre'],
                             transferencia=transferencia)
    except Exception as e:
        flash(f'Error al cargar comprobante: {str(e)}', 'error')
        return redirect(url_for('dashboard'))


@app.route('/crear-cuenta', methods=['GET', 'POST'])
def crear_cuenta():
    if 'cliente_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = {
            'cliente_id': session['cliente_id'],
            'tipo_cuenta': request.form.get('tipo_cuenta'),
            'saldo': float(request.form.get('saldo', 0))
        }
        
        try:
            response = requests.post(f'{BACKEND_URL}/cuentas', json=data)
            
            if response.status_code == 201:
                cuenta = response.json()
                flash(f'Cuenta creada exitosamente. Número: {cuenta["numero_cuenta"]}', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Error al crear cuenta', 'error')
        except Exception as e:
            flash(f'Error al conectar con el servidor: {str(e)}', 'error')
    
    return render_template('crear_cuenta.html', cliente_nombre=session['cliente_nombre'])


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
