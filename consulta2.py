import streamlit as st
from db import get_session
from clases import Publicacion

def ejecutar():
    st.subheader("Reacciones a una publicación")
    session = get_session()

    publicaciones = session.query(Publicacion).all()

    # Crear lista de opciones con ID + preview del contenido
    opciones = [f"{p.id} - {p.contenido[:30]}" for p in publicaciones]
    seleccion = st.selectbox("Selecciona una publicación:", opciones)

    # Obtener el ID de la publicación seleccionada
    publicacion_id = int(seleccion.split(" - ")[0])
    publicacion = session.query(Publicacion).filter_by(id=publicacion_id).first()

    if publicacion:
        st.markdown(f"**Contenido completo:** {publicacion.contenido}")

        if publicacion.reacciones:
            tipo_reaccion = list(sorted({r.tipo_reaccion for r in publicacion.reacciones}))
            tipo_reaccion.insert(0, "Todos")

            tipo_filtrado = st.radio("Filtrar por emoción:", tipo_reaccion, horizontal=True)

            reacciones_filtradas = [
                r for r in publicacion.reacciones
                if tipo_filtrado == "Todos" or r.tipo_reaccion == tipo_filtrado
            ]

            if reacciones_filtradas:
                st.markdown("**Reacciones:**")
                st.table([
                    {
                        "Usuario": r.usuario.nombre_usuario,
                        "Emoción": r.tipo_reaccion
                    } for r in reacciones_filtradas
                ])
            else:
                st.info("No hay reacciones con ese tipo de emoción.")
        else:
            st.info("Esta publicación no tiene reacciones.")
    else:
        st.error("Publicación no encontrada.")
    
    session.close()