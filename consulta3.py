import streamlit as st
from sqlalchemy import or_, not_
from db import get_session
from clases import Usuario, Reaccion

def ejecutar():
    st.subheader("Reacciones 'alegre', 'enojado' o 'pensativo' de usuarios cuyo nombre NO inicia con vocal")

    session = get_session()

    # Filtro para nombres que NO empiezan con vocal (mayúscula o minúscula)
    vocales = ['A', 'E', 'I', 'O', 'U']
    filtro_nombre = not_(or_(
        Usuario.nombre_usuario.ilike(f'{v}%') for v in vocales
    ))

    # Ejecutar la consulta
    resultados = (
        session.query(Usuario.nombre_usuario, Reaccion.tipo_reaccion)
        .join(Reaccion, Usuario.id == Reaccion.usuario_id)
        .filter(Reaccion.tipo_reaccion.in_(["alegre", "enojado", "pensativo"]))
        .filter(filtro_nombre)
        .all()
    )

    # Mostrar resultados
    if resultados:
        datos = [
            {"Usuario": nombre, "Emoción": tipo}
            for nombre, tipo in resultados
        ]
        st.success(f"Se encontraron {len(resultados)} reacciones.")
        st.table(datos)
    else:
        st.info("No se encontraron reacciones que cumplan los criterios.")

    session.close()
