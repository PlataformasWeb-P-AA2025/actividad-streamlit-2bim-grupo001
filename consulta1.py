import streamlit as st
from db import get_session
from clases import Usuario, Publicacion

def ejecutar():
    st.subheader("Publicaciones por usuario")
    session = get_session()
    usuarios = session.query(Usuario).all()
    nombres = [u.nombre_usuario for u in usuarios] 

    nombre_usuario = st.selectbox("Selecciona un usuario:", nombres)

    if nombre_usuario:
        publicaciones = (
            session.query(Publicacion)
            .join(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario)
            .all()
        )

        if publicaciones:
            st.success(f"Publicaciones de {nombre_usuario}:")
            for pub in publicaciones:
                st.markdown(f"- {pub.contenido}")
        else:
            st.info(f"{nombre_usuario} no tiene publicaciones.")
    session.close()
