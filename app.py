import streamlit as st
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

from libreria_funciones_proyecto1 import (
    calcular_punto_equilibrio, calcular_margen_neto,
    calcular_roi, calcular_valor_futuro, calcular_cuota_prestamo_frances
)
from libreria_clases_proyecto1 import Empleado

# ─────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Proyecto 1 – Python Fundamentals",
    page_icon="🐍",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────
# CONEXIÓN A FIREBASE
# Las credenciales se leen desde .streamlit/secrets.toml
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    return firestore.client()

try:
    db = init_firebase()
    FIREBASE_OK = True
except Exception:
    FIREBASE_OK = False

# ─────────────────────────────────────────────────────────────────
# COLORES POR CATEGORÍA
# ─────────────────────────────────────────────────────────────────
COLORES_CATEGORIA = {
    "Electrónico": "#FFF176",   # Amarillo
    "Alimento":    "#C8E6C9",   # Verde
    "Ropa":        "#BBDEFB",   # Azul
    "Hogar":       "#FFE0B2",   # Naranja
    "Otro":        "#E1BEE7",   # Morado
}

def colorear_fila(row):
    color = COLORES_CATEGORIA.get(row["Categoría"], "#FFFFFF")
    return [f"background-color: {color}"] * len(row)

# ─────────────────────────────────────────────────────────────────
# MENÚ LATERAL
# ─────────────────────────────────────────────────────────────────
if FIREBASE_OK:
    st.sidebar.success("🔥 Firebase conectado")
else:
    st.sidebar.warning("⚠️ Firebase no configurado – datos solo en sesión")

pagina = st.sidebar.selectbox(
    "📂 Navegación",
    ["🏠 Home", "📋 Ejercicio 1", "📦 Ejercicio 2", "🔢 Ejercicio 3", "👤 Ejercicio 4"]
)

# ═══════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════
if pagina == "🏠 Home":
    st.title("🐍 Proyecto 1 – Python Fundamentals")
    st.subheader("Especialización en Python for Analytics · Módulo 1")
    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/240px-Python-logo-notext.svg.png",
            width=130
        )
    with col2:
        st.markdown("""
**👤 Estudiante:** Tu Nombre Completo  
**📚 Módulo:** Python Fundamentals  
**🏫 Institución:** DMC Institute  
**📅 Año:** 2025  
""")

    st.markdown("---")
    st.markdown("### 📝 Descripción del proyecto")
    st.write(
        "Esta aplicación interactiva integra los conceptos fundamentales del Módulo 1: "
        "variables, estructuras de datos, control de flujo, funciones, "
        "programación funcional y programación orientada a objetos (POO). "
        "Todos los datos se persisten en tiempo real con Firebase Firestore."
    )
    st.markdown("### 🛠️ Tecnologías utilizadas")
    st.markdown("""
- 🐍 **Python 3**
- 📊 **Streamlit** – Interfaz web interactiva
- 🔢 **NumPy** – Manejo de arrays
- 🐼 **Pandas** – DataFrames y tablas
- 🔥 **Firebase Firestore** – Base de datos en tiempo real
- 📦 Librerías del curso: `libreria_funciones_proyecto1.py` · `libreria_clases_proyecto1.py`
""")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 1 – Flujo de caja con listas + Firebase
# ═══════════════════════════════════════════════════════════════
elif pagina == "📋 Ejercicio 1":
    st.title("📋 Ejercicio 1 – Flujo de Caja")
    st.markdown("""
> Registra ingresos y gastos. El saldo final indica si el flujo está  
> **a favor** o **en contra**. Datos guardados en 🔥 Firebase.
""")
    st.markdown("---")

    # Cargar desde Firebase la primera vez
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []
        if FIREBASE_OK:
            docs = db.collection("flujo_caja").order_by("timestamp").stream()
            for doc in docs:
                d = doc.to_dict()
                st.session_state.movimientos.append({
                    "Concepto":  d.get("concepto", ""),
                    "Tipo":      d.get("tipo", ""),
                    "Valor ($)": d.get("valor", 0.0),
                    "_id":       doc.id
                })

    col1, col2, col3 = st.columns(3)
    with col1:
        concepto = st.text_input("Concepto", placeholder="Ej: Venta de producto")
    with col2:
        tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    with col3:
        valor = st.number_input("Valor ($)", min_value=0.01, step=0.01, format="%.2f")

    if st.button("➕ Agregar movimiento"):
        if concepto.strip() == "":
            st.warning("⚠️ Por favor ingresa un concepto.")
        else:
            import datetime
            nuevo = {
                "Concepto":  concepto.strip(),
                "Tipo":      tipo,
                "Valor ($)": round(valor, 2),
                "_id":       None
            }
            if FIREBASE_OK:
                ref = db.collection("flujo_caja").add({
                    "concepto":  concepto.strip(),
                    "tipo":      tipo,
                    "valor":     round(valor, 2),
                    "timestamp": datetime.datetime.utcnow()
                })
                nuevo["_id"] = ref[1].id
            st.session_state.movimientos.append(nuevo)
            st.success(f"✅ Movimiento '{concepto}' agregado.")

    st.markdown("---")

    if st.session_state.movimientos:
        df = pd.DataFrame([
            {k: v for k, v in m.items() if k != "_id"}
            for m in st.session_state.movimientos
        ])
        st.subheader("📄 Movimientos registrados")
        st.dataframe(df, use_container_width=True)

        total_ingresos = df[df["Tipo"] == "Ingreso"]["Valor ($)"].sum()
        total_gastos   = df[df["Tipo"] == "Gasto"]["Valor ($)"].sum()
        saldo_final    = total_ingresos - total_gastos

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Total Ingresos", f"${total_ingresos:,.2f}")
        col2.metric("💸 Total Gastos",   f"${total_gastos:,.2f}")
        col3.metric("🏦 Saldo Final",    f"${saldo_final:,.2f}")

        st.markdown("---")
        if saldo_final >= 0:
            st.success(f"✅ El flujo de caja está **a favor** con un saldo de ${saldo_final:,.2f}")
        else:
            st.error(f"❌ El flujo de caja está **en contra** con un déficit de ${abs(saldo_final):,.2f}")

        if st.button("🗑️ Limpiar movimientos"):
            if FIREBASE_OK:
                for doc in db.collection("flujo_caja").stream():
                    doc.reference.delete()
            st.session_state.movimientos = []
            st.rerun()
    else:
        st.info("Aún no hay movimientos registrados. ¡Agrega el primero!")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 2 – NumPy + colores por categoría + Firebase
# ═══════════════════════════════════════════════════════════════
elif pagina == "📦 Ejercicio 2":
    st.title("📦 Ejercicio 2 – Registro de Productos")
    st.markdown("""
> Registra productos con **arrays NumPy**. La tabla se colorea por **categoría**.  
> Datos guardados en 🔥 Firebase.
""")
    st.markdown("---")

    # Leyenda de colores
    st.markdown("**🎨 Leyenda de colores por categoría:**")
    cols_ley = st.columns(5)
    for col, (cat, color) in zip(cols_ley, COLORES_CATEGORIA.items()):
        col.markdown(
            f"<div style='background:{color};padding:6px 8px;border-radius:8px;"
            f"text-align:center;font-size:13px;border:1px solid #ccc'>"
            f"<b>{cat}</b></div>",
            unsafe_allow_html=True
        )
    st.markdown("---")

    # Cargar desde Firebase la primera vez
    if "arr_nombre" not in st.session_state:
        st.session_state.arr_nombre    = np.array([], dtype=str)
        st.session_state.arr_categoria = np.array([], dtype=str)
        st.session_state.arr_precio    = np.array([], dtype=float)
        st.session_state.arr_cantidad  = np.array([], dtype=int)
        st.session_state.arr_ids       = []

        if FIREBASE_OK:
            docs = db.collection("productos").order_by("timestamp").stream()
            for doc in docs:
                d = doc.to_dict()
                st.session_state.arr_nombre    = np.append(st.session_state.arr_nombre,    d.get("nombre", ""))
                st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, d.get("categoria", ""))
                st.session_state.arr_precio    = np.append(st.session_state.arr_precio,    float(d.get("precio", 0)))
                st.session_state.arr_cantidad  = np.append(st.session_state.arr_cantidad,  int(d.get("cantidad", 0)))
                st.session_state.arr_ids.append(doc.id)

    col1, col2 = st.columns(2)
    with col1:
        p_nombre    = st.text_input("Nombre del producto", placeholder="Ej: Laptop")
        p_categoria = st.selectbox("Categoría", list(COLORES_CATEGORIA.keys()))
    with col2:
        p_precio   = st.number_input("Precio unitario ($)", min_value=0.01, step=0.01, format="%.2f")
        p_cantidad = st.number_input("Cantidad", min_value=1, step=1)

    if st.button("➕ Agregar producto"):
        if p_nombre.strip() == "":
            st.warning("⚠️ Ingresa el nombre del producto.")
        else:
            import datetime
            doc_id = None
            if FIREBASE_OK:
                ref = db.collection("productos").add({
                    "nombre":    p_nombre.strip(),
                    "categoria": p_categoria,
                    "precio":    round(p_precio, 2),
                    "cantidad":  int(p_cantidad),
                    "timestamp": datetime.datetime.utcnow()
                })
                doc_id = ref[1].id

            st.session_state.arr_nombre    = np.append(st.session_state.arr_nombre,    p_nombre.strip())
            st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, p_categoria)
            st.session_state.arr_precio    = np.append(st.session_state.arr_precio,    p_precio)
            st.session_state.arr_cantidad  = np.append(st.session_state.arr_cantidad,  int(p_cantidad))
            st.session_state.arr_ids.append(doc_id)
            st.success(f"✅ Producto '{p_nombre}' ({p_categoria}) agregado.")

    st.markdown("---")

    if len(st.session_state.arr_nombre) > 0:
        total_arr = st.session_state.arr_precio * st.session_state.arr_cantidad
        df_prod = pd.DataFrame({
            "Producto":   st.session_state.arr_nombre,
            "Categoría":  st.session_state.arr_categoria,
            "Precio ($)": np.round(st.session_state.arr_precio, 2),
            "Cantidad":   st.session_state.arr_cantidad,
            "Total ($)":  np.round(total_arr, 2)
        })

        st.subheader("📄 Inventario registrado")

        # Tabla con colores por categoría
        styled = df_prod.style.apply(colorear_fila, axis=1).format({
            "Precio ($)": "${:,.2f}",
            "Total ($)":  "${:,.2f}"
        })
        st.dataframe(styled, use_container_width=True)

        col1, col2 = st.columns(2)
        col1.metric("📦 Productos registrados", len(df_prod))
        col2.metric("💰 Valor total inventario", f"${df_prod['Total ($)'].sum():,.2f}")

        if st.button("🗑️ Limpiar inventario"):
            if FIREBASE_OK:
                for doc in db.collection("productos").stream():
                    doc.reference.delete()
            for key in ["arr_nombre", "arr_categoria", "arr_precio", "arr_cantidad", "arr_ids"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.info("Aún no hay productos registrados. ¡Agrega el primero!")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 3 – Funciones + Firebase
# ═══════════════════════════════════════════════════════════════
elif pagina == "🔢 Ejercicio 3":
    st.title("🔢 Ejercicio 3 – Calculadora Financiera")
    st.markdown("""
> Selecciona una función de la **librería del profesor**, ingresa  
> los parámetros y ejecuta. El histórico se guarda en 🔥 Firebase.
""")
    st.markdown("---")

    if "hist_func" not in st.session_state:
        st.session_state.hist_func = []
        if FIREBASE_OK:
            docs = db.collection("historico_funciones").order_by("timestamp").stream()
            for doc in docs:
                d = doc.to_dict()
                d.pop("timestamp", None)
                st.session_state.hist_func.append(d)

    funcion = st.selectbox("📌 Selecciona la función", [
        "Punto de Equilibrio",
        "Margen Neto",
        "ROI",
        "Valor Futuro (Interés Compuesto)",
        "Cuota Préstamo (Sistema Francés)"
    ])

    resultado  = None
    params_str = ""

    if funcion == "Punto de Equilibrio":
        st.markdown("**Calcula unidades y ventas mínimas para cubrir costos.**")
        c1, c2, c3 = st.columns(3)
        costos_fijos   = c1.number_input("Costos fijos ($)",           min_value=0.01, value=5000.0, step=100.0)
        precio_unit    = c2.number_input("Precio unitario ($)",         min_value=0.01, value=50.0,   step=1.0)
        costo_var_unit = c3.number_input("Costo variable unitario ($)", min_value=0.0,  value=20.0,   step=1.0)
        params_str = f"CF={costos_fijos}, PU={precio_unit}, CVU={costo_var_unit}"
        if st.button("⚡ Calcular"):
            try:
                resultado = calcular_punto_equilibrio(costos_fijos, precio_unit, costo_var_unit)
            except ValueError as e:
                st.error(f"Error: {e}")

    elif funcion == "Margen Neto":
        st.markdown("**Calcula utilidad bruta, neta y margen neto.**")
        c1, c2 = st.columns(2)
        ingresos  = c1.number_input("Ingresos ($)",         min_value=0.01, value=100000.0, step=1000.0)
        costos    = c2.number_input("Costos ($)",            min_value=0.0,  value=40000.0,  step=1000.0)
        gastos_op = c1.number_input("Gastos operativos ($)", min_value=0.0,  value=20000.0,  step=1000.0)
        impuestos = c2.number_input("Impuestos ($)",         min_value=0.0,  value=5000.0,   step=500.0)
        params_str = f"Ingresos={ingresos}, Costos={costos}, GO={gastos_op}, Imp={impuestos}"
        if st.button("⚡ Calcular"):
            try:
                resultado = calcular_margen_neto(ingresos, costos, gastos_op, impuestos)
            except ValueError as e:
                st.error(f"Error: {e}")

    elif funcion == "ROI":
        st.markdown("**Retorno sobre la Inversión.**")
        c1, c2 = st.columns(2)
        ganancia  = c1.number_input("Ganancia neta ($)", min_value=0.0,  value=15000.0, step=500.0)
        inversion = c2.number_input("Inversión ($)",     min_value=0.01, value=50000.0, step=1000.0)
        params_str = f"Ganancia={ganancia}, Inversión={inversion}"
        if st.button("⚡ Calcular"):
            try:
                resultado = calcular_roi(ganancia, inversion)
            except ValueError as e:
                st.error(f"Error: {e}")

    elif funcion == "Valor Futuro (Interés Compuesto)":
        st.markdown("**Proyecta el valor futuro de un capital.**")
        c1, c2, c3 = st.columns(3)
        monto = c1.number_input("Monto inicial ($)", min_value=0.01, value=10000.0, step=500.0)
        tasa  = c2.number_input("Tasa anual (%)",    min_value=0.01, value=6.0,     step=0.5)
        anios = c3.number_input("Años",              min_value=1,    value=5,        step=1)
        params_str = f"Monto={monto}, Tasa={tasa}%, Años={anios}"
        if st.button("⚡ Calcular"):
            try:
                resultado = calcular_valor_futuro(monto, tasa, anios)
            except ValueError as e:
                st.error(f"Error: {e}")

    elif funcion == "Cuota Préstamo (Sistema Francés)":
        st.markdown("**Calcula cuota mensual de un préstamo.**")
        c1, c2, c3 = st.columns(3)
        monto_p = c1.number_input("Monto del préstamo ($)", min_value=0.01, value=20000.0, step=1000.0)
        tasa_p  = c2.number_input("Tasa anual (%)",          min_value=0.01, value=12.0,    step=0.5)
        plazo   = c3.number_input("Plazo (meses)",            min_value=1,    value=24,       step=1)
        params_str = f"Monto={monto_p}, Tasa={tasa_p}%, Plazo={plazo}m"
        if st.button("⚡ Calcular"):
            try:
                resultado = calcular_cuota_prestamo_frances(monto_p, tasa_p, int(plazo))
            except ValueError as e:
                st.error(f"Error: {e}")

    if resultado:
        st.markdown("---")
        st.subheader("📊 Resultado")
        cols = st.columns(len(resultado))
        for col, (k, v) in zip(cols, resultado.items()):
            col.metric(k.replace("_", " ").title(), str(v))

        fila = {"Función": funcion, "Parámetros": params_str}
        fila.update(resultado)
        st.session_state.hist_func.append(fila)

        if FIREBASE_OK:
            import datetime
            db.collection("historico_funciones").add({**fila, "timestamp": datetime.datetime.utcnow()})

    if st.session_state.hist_func:
        st.markdown("---")
        st.subheader("🗂️ Histórico de cálculos")
        st.dataframe(pd.DataFrame(st.session_state.hist_func), use_container_width=True)
        if st.button("🗑️ Limpiar histórico"):
            if FIREBASE_OK:
                for doc in db.collection("historico_funciones").stream():
                    doc.reference.delete()
            st.session_state.hist_func = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 4 – Clases CRUD + Firebase
# ═══════════════════════════════════════════════════════════════
elif pagina == "👤 Ejercicio 4":
    st.title("👤 Ejercicio 4 – Gestión de Empleados (CRUD)")
    st.markdown("""
> Usa la clase **`Empleado`** con operaciones  
> **Crear · Leer · Actualizar · Eliminar**. Datos en 🔥 Firebase.
""")
    st.markdown("---")

    if "empleados" not in st.session_state:
        st.session_state.empleados = {}
        if FIREBASE_OK:
            for doc in db.collection("empleados").stream():
                d = doc.to_dict()
                st.session_state.empleados[doc.id] = {
                    "nombre":       d.get("nombre", ""),
                    "salario_base": d.get("salario_base", 0.0),
                    "bono":         d.get("bono", 0.0),
                    "descuento":    d.get("descuento", 0.0),
                    "salario_neto": d.get("salario_neto", 0.0)
                }

    tab_crear, tab_ver, tab_editar, tab_eliminar = st.tabs(
        ["➕ Crear", "📋 Ver", "✏️ Actualizar", "🗑️ Eliminar"]
    )

    # CREAR
    with tab_crear:
        st.subheader("Registrar nuevo empleado")
        c1, c2 = st.columns(2)
        nombre_c  = c1.text_input("Nombre completo", key="c_nombre")
        salario_c = c2.number_input("Salario base ($)", min_value=0.01, value=800.0, step=50.0, key="c_sal")
        bono_c    = c1.number_input("Bono (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key="c_bono")
        desc_c    = c2.number_input("Descuento (%)", min_value=0.0, max_value=100.0, value=9.45, step=0.1, key="c_desc")

        if st.button("💾 Guardar empleado"):
            if nombre_c.strip() == "":
                st.warning("⚠️ El nombre no puede estar vacío.")
            else:
                try:
                    emp = Empleado(nombre_c.strip(), salario_c, bono_c, desc_c)
                    resumen = emp.resumen()
                    if FIREBASE_OK:
                        ref = db.collection("empleados").add({
                            "nombre":       resumen["nombre"],
                            "salario_base": resumen["salario_base"],
                            "bono":         resumen["bono"],
                            "descuento":    resumen["descuento"],
                            "salario_neto": resumen["salario_neto"]
                        })
                        eid = ref[1].id
                    else:
                        import uuid
                        eid = str(uuid.uuid4())[:8]
                    st.session_state.empleados[eid] = resumen
                    st.success(f"✅ Empleado **{nombre_c}** guardado.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # VER
    with tab_ver:
        st.subheader("Lista de empleados")
        if st.session_state.empleados:
            rows = [{"ID": eid, **data} for eid, data in st.session_state.empleados.items()]
            df_emp = pd.DataFrame(rows)
            st.dataframe(df_emp, use_container_width=True)
            col1, col2 = st.columns(2)
            col1.metric("👥 Total empleados", len(df_emp))
            col2.metric("💰 Nómina total ($)", f"${df_emp['salario_neto'].sum():,.2f}")
        else:
            st.info("No hay empleados registrados aún.")

    # ACTUALIZAR
    with tab_editar:
        st.subheader("Actualizar empleado")
        if st.session_state.empleados:
            sel_id     = st.selectbox("Selecciona empleado (ID)", list(st.session_state.empleados.keys()), key="upd_id")
            emp_actual = st.session_state.empleados[sel_id]
            c1, c2 = st.columns(2)
            nuevo_nombre  = c1.text_input("Nuevo nombre", value=emp_actual["nombre"], key="u_nom")
            nuevo_salario = c2.number_input("Nuevo salario base ($)", min_value=0.01, value=float(emp_actual["salario_base"]), step=50.0, key="u_sal")
            bono_pct      = round(emp_actual["bono"] / emp_actual["salario_base"] * 100, 2) if emp_actual["salario_base"] else 0.0
            nuevo_bono    = c1.number_input("Nuevo bono (%)", min_value=0.0, max_value=100.0, value=bono_pct, step=1.0, key="u_bono")
            nuevo_desc    = c2.number_input("Nuevo descuento (%)", min_value=0.0, max_value=100.0, value=9.45, step=0.1, key="u_desc")

            if st.button("🔄 Actualizar"):
                if nuevo_nombre.strip() == "":
                    st.warning("⚠️ El nombre no puede estar vacío.")
                else:
                    try:
                        emp_upd = Empleado(nuevo_nombre.strip(), nuevo_salario, nuevo_bono, nuevo_desc)
                        resumen_upd = emp_upd.resumen()
                        if FIREBASE_OK:
                            db.collection("empleados").document(sel_id).set({
                                "nombre":       resumen_upd["nombre"],
                                "salario_base": resumen_upd["salario_base"],
                                "bono":         resumen_upd["bono"],
                                "descuento":    resumen_upd["descuento"],
                                "salario_neto": resumen_upd["salario_neto"]
                            })
                        st.session_state.empleados[sel_id] = resumen_upd
                        st.success("✅ Empleado actualizado correctamente.")
                    except ValueError as e:
                        st.error(f"Error: {e}")
        else:
            st.info("No hay empleados para actualizar.")

    # ELIMINAR
    with tab_eliminar:
        st.subheader("Eliminar empleado")
        if st.session_state.empleados:
            del_id     = st.selectbox("Selecciona el empleado a eliminar", list(st.session_state.empleados.keys()), key="del_id")
            nombre_del = st.session_state.empleados[del_id]["nombre"]
            st.write(f"Vas a eliminar a: **{nombre_del}**")
            if st.button("🗑️ Confirmar eliminación", type="primary"):
                if FIREBASE_OK:
                    db.collection("empleados").document(del_id).delete()
                del st.session_state.empleados[del_id]
                st.success(f"✅ Empleado **{nombre_del}** eliminado.")
                st.rerun()
        else:
            st.info("No hay empleados para eliminar.")