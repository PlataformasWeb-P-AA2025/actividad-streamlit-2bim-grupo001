import streamlit as st
from sqlalchemy import func
from db import get_session
from clases import Publicacion, Reaccion

def ejecutar():
    st.subheader("Publicaciones que recibieron todos los tipos de reacciones disponibles")

    session = get_session()

    # Obtener la cantidad total de tipos de reacción distintos
    tipos = session.query(Reaccion.tipo_reaccion).distinct().all()
    total_tipos = len(tipos)

    # Consulta: publicaciones que tienen todos los tipos de reacciones
    resultados = (
        session.query(
            Publicacion.contenido,
            func.count(func.distinct(Reaccion.tipo_reaccion)).label("tipos_usados")
        )
        .join(Reaccion)
        .group_by(Publicacion.id)
        .having(func.count(func.distinct(Reaccion.tipo_reaccion)) == total_tipos)
        .all()
    )

    if resultados:
        datos = [
            {"Publicación": contenido, "Tipos de reacciones usados": tipos_usados}
            for contenido, tipos_usados in resultados
        ]
        st.success(f"Se encontraron {len(resultados)} publicaciones.")
        st.table(datos)
    else:
        st.info("No se encontraron publicaciones que hayan recibido todos los tipos de reacciones.")

    session.close()
