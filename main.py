import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import psycopg2 # El equivalente de pymongo para PostgreSQL
from psycopg2.extras import RealDictCursor #  Sirve para devolver un dict en lugar de un tuple
from fastmcp import FastMCP

app = FastMCP("company-db-server")

def get_db_connection():
    conn = psycopg2.connect( 
        host = os.environ.get("DB_HOST", "localhost"),
        port = int(os.environ.get("DB_PORT", "5432")), 
        user =  os.environ.get("DB_USER", "postgres"),
        password = os.environ.get("DB_PASSWORD", "postgres"),
        database = os.environ.get("DB_DATABASE", "postgres"),
        cursor_factory = RealDictCursor
    )
    return conn

# Función para listar empleados
@app.tool
def list_employees(limit: int = 5) -> List[Dict[str, Any]]: # la salida del Dict se especifica la llave (str), valor (Any)
    """Esta función lista los empleados de la empresa"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor() # Esto es para poder usar código PostgreSQL en Python
        cursor.execute("""
            SELECT id, name, position, department, salary, hire_date
            FROM employees
            ORDER BY id
            LIMIT %s
            """, (limit,)) # El %s es para pasar variables de forma segura y evitar SQL injection
        rows = cursor.fetchall()
        employees = [
            {
                "id": row['id'],
                "name": row['name'],
                "position": row['position'],
                "department": row['department'],
                "salary": float(row['salary']),
                "hire_date": str(row['hire_date'])
            }
            for row in rows
        ]
        cursor.close()
        conn.close()
        return employees
    
    except Exception as e:
        raise RuntimeError(f"Error en la base de datos: {str(e)}")
        
@app.tool
def add_employee(name: str, position: str, department: str, salary: float, hire_date: Optional[str] = None):
    """Agrega un nuevo empleado a la base de datos"""
    try:
        if not name.strip():
            return {'error': 'El nombre del empleado no puede estar vacío'}
        if salary <= 0:
            return {'error': 'La salario debe ser mayor que cero'}
        if not hire_date:
            hire_date = datetime.now().strftime('%Y-%m-%d')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (name, position, department, salary, hire_date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, position, department, salary, hire_date
            """, (name.strip(), position.strip(),   department.strip(), salary, hire_date))
        
        new_employee = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        return {"success": True, 
                "employee": {
                    "id": new_employee['id'], 
                    "name": new_employee['name'], 
                    "position": new_employee['position'], 
                    "department": new_employee['department'], 
                    "salary": float(new_employee['salary']),
                    "hire_date": str(new_employee['hire_date'])
                    }
                }   
    except Exception as e:
        raise RuntimeError(f"Error al agregar empleado: {str(e)}")   
    
if __name__ == "__main__":
    app.run(transport="sse", host="0.0.0.0", port=3000)

                 