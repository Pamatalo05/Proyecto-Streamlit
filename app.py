import streamlit as st
import pandas as pd
import numpy as np

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
# COLORES POR CATEGORÍA (Ejercicio 2)
# ─────────────────────────────────────────────────────────────────
COLORES_CATEGORIA = {
    "Electrónico": "#00E5FF",  # Cian brillante
    "Alimento":    "#00FF9C",  # Verde neón
    "Ropa":        "#2979FF",  # Azul intenso
    "Hogar":       "#FF9100",  # Naranja fuerte
    "Otro":        "#D500F9",  # Morado neón
}

def colorear_fila(row):
    color = COLORES_CATEGORIA.get(row["Categoría"], "#FFFFFF")
    return [f"background-color: {color}"] * len(row)

# ─────────────────────────────────────────────────────────────────
# MENÚ LATERAL
# ─────────────────────────────────────────────────────────────────
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
            "https://aulavirtualdmc.com/learning/pluginfile.php/88512/course/overviewfiles/perfil%20dmc%20institute%20redes%20dark.png",
            use_container_width=True
        )
    with col2:
        st.markdown("""
**👤 Estudiante:** Paulo Marcelo Tapia Loor  

Soy estudiante de Ingeniería en Computación en la ESPOL, tengo 23 años y me interesa especialmente la ciberseguridad y el análisis de datos. Me motiva enfrentar nuevos retos, aprender constantemente y aplicar mis conocimientos en la resolución de problemas reales. Aunque a veces el miedo esté presente, lo utilizo como impulso para seguir avanzando y mejorar cada día, buscando siempre crecer dentro del área tecnológica.

**📚 Módulo:** Python Fundamentals  
**🏫 Institución:** DMC Institute  
**📅 Año:** 2025  

🔗 **LinkedIn:** [www.linkedin.com/in/paulotapialoor](https://www.linkedin.com/in/paulotapialoor)  
💻 **GitHub:** [github.com/Pamatalo05](https://github.com/Pamatalo05)  
""")

    st.markdown("---")
    st.markdown("### 📝 Descripción del proyecto")
    st.write(
        "Esta aplicación interactiva integra los conceptos fundamentales del Módulo 1: "
        "variables, estructuras de datos, control de flujo, funciones, "
        "programación funcional y programación orientada a objetos (POO). "
        "Cada ejercicio representa una sección independiente conectada a través del menú lateral."
    )

    st.markdown("### 🛠️ Tecnologías utilizadas")
    st.markdown("""
- 🐍 **Python 3**
- 📊 **Streamlit** – Interfaz web interactiva
- 🔢 **NumPy** – Manejo de arrays
- 🐼 **Pandas** – DataFrames y tablas
- 📦 Librerías del curso: `libreria_funciones_proyecto1.py` · `libreria_clases_proyecto1.py`
""")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 1 – Flujo de caja con listas
# ═══════════════════════════════════════════════════════════════
elif pagina == "📋 Ejercicio 1":
    st.title("📋 Ejercicio 1 – Flujo de Caja")
    st.markdown("""
> Registra tus ingresos y gastos. La aplicación calcula el saldo final  
> e indica si el flujo de caja está **a favor** o **en contra**.
""")
    st.markdown("---")

    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []

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
            st.session_state.movimientos.append({
                "Concepto":  concepto.strip(),
                "Tipo":      tipo,
                "Valor ($)": round(valor, 2)
            })
            st.success(f"✅ Movimiento '{concepto}' agregado.")

    st.markdown("---")

    if st.session_state.movimientos:
        df = pd.DataFrame(st.session_state.movimientos)
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
            st.session_state.movimientos = []
            st.rerun()
    else:
        st.info("Aún no hay movimientos registrados. ¡Agrega el primero!")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 2 – NumPy + colores por categoría
# ═══════════════════════════════════════════════════════════════
elif pagina == "📦 Ejercicio 2":
    st.title("📦 Ejercicio 2 – Registro de Productos")
    st.markdown("""
> Registra productos usando **arrays de NumPy**. La tabla se colorea  
> automáticamente según la **categoría** de cada producto.
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

    # Inicializar arrays
    if "arr_nombre"    not in st.session_state: st.session_state.arr_nombre    = np.array([], dtype=str)
    if "arr_categoria" not in st.session_state: st.session_state.arr_categoria = np.array([], dtype=str)
    if "arr_precio"    not in st.session_state: st.session_state.arr_precio    = np.array([], dtype=float)
    if "arr_cantidad"  not in st.session_state: st.session_state.arr_cantidad  = np.array([], dtype=int)

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
            st.session_state.arr_nombre    = np.append(st.session_state.arr_nombre,    p_nombre.strip())
            st.session_state.arr_categoria = np.append(st.session_state.arr_categoria, p_categoria)
            st.session_state.arr_precio    = np.append(st.session_state.arr_precio,    p_precio)
            st.session_state.arr_cantidad  = np.append(st.session_state.arr_cantidad,  int(p_cantidad))
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
            for key in ["arr_nombre", "arr_categoria", "arr_precio", "arr_cantidad"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.info("Aún no hay productos registrados. ¡Agrega el primero!")


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 3 – Funciones desde librería externa
# ═══════════════════════════════════════════════════════════════
elif pagina == "🔢 Ejercicio 3":
    st.title("🔢 Ejercicio 3 – Calculadora Financiera")
    st.markdown("""
> Selecciona una función de la **librería del profesor**, ingresa  
> los parámetros y ejecuta. El resultado se guarda en un **histórico**.
""")
    st.markdown("---")

    if "hist_func" not in st.session_state:
        st.session_state.hist_func = []

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

    if st.session_state.hist_func:
        st.markdown("---")
        st.subheader("🗂️ Histórico de cálculos")
        st.dataframe(pd.DataFrame(st.session_state.hist_func), use_container_width=True)
        if st.button("🗑️ Limpiar histórico"):
            st.session_state.hist_func = []
            st.rerun()


# ═══════════════════════════════════════════════════════════════
# EJERCICIO 4 – Clases CRUD (Empleado)
# ═══════════════════════════════════════════════════════════════
elif pagina == "👤 Ejercicio 4":
    st.title("👤 Ejercicio 4 – Gestión de Empleados (CRUD)")
    st.markdown("""
> Usa la clase **`Empleado`** para gestionar empleados con  
> operaciones **Crear · Leer · Actualizar · Eliminar**.
""")
    st.markdown("---")

    if "empleados"        not in st.session_state: st.session_state.empleados        = {}
    if "emp_id_counter"   not in st.session_state: st.session_state.emp_id_counter   = 1

    tab_crear, tab_ver, tab_editar, tab_eliminar = st.tabs(
        ["➕ Crear", "📋 Ver", "✏️ Actualizar", "🗑️ Eliminar"]
    )

    # ── CREAR ────────────────────────────────────────────────────
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
                    eid = st.session_state.emp_id_counter
                    st.session_state.empleados[eid] = emp.resumen()
                    st.session_state.emp_id_counter += 1
                    st.success(f"✅ Empleado **{nombre_c}** guardado con ID #{eid}.")
                except ValueError as e:
                    st.error(f"Error: {e}")

    # ── VER ──────────────────────────────────────────────────────
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

    # ── ACTUALIZAR ───────────────────────────────────────────────
    with tab_editar:
        st.subheader("Actualizar empleado")
        if st.session_state.empleados:
            sel_id     = st.selectbox("Selecciona empleado (ID)", list(st.session_state.empleados.keys()), key="upd_id")
            emp_actual = st.session_state.empleados[sel_id]
            c1, c2    = st.columns(2)
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
                        st.session_state.empleados[sel_id] = emp_upd.resumen()
                        st.success("✅ Empleado actualizado correctamente.")
                    except ValueError as e:
                        st.error(f"Error: {e}")
        else:
            st.info("No hay empleados para actualizar.")

    # ── ELIMINAR ─────────────────────────────────────────────────
    with tab_eliminar:
        st.subheader("Eliminar empleado")
        if st.session_state.empleados:
            del_id     = st.selectbox("Selecciona el empleado a eliminar", list(st.session_state.empleados.keys()), key="del_id")
            nombre_del = st.session_state.empleados[del_id]["nombre"]
            st.write(f"Vas a eliminar a: **{nombre_del}**")
            if st.button("🗑️ Confirmar eliminación", type="primary"):
                del st.session_state.empleados[del_id]
                st.success(f"✅ Empleado **{nombre_del}** eliminado.")
                st.rerun()
        else:
            st.info("No hay empleados para eliminar.")
