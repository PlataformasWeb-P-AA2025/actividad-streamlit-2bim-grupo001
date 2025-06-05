import streamlit as st
from db import get_session
from clases import Usuario, Reaccion

def ejecutar():
    st.title("Publicaciones donde reaccionó un usuario")

    session = get_session()

    usuarios = session.query(Usuario).all()

    nombres = [u.nombre_usuario for u in usuarios]
    usuario_seleccionado = st.selectbox("Selecciona un usuario:", nombres)

    if usuario_seleccionado:
        usuario = session.query(Usuario).filter(Usuario.nombre_usuario == usuario_seleccionado).first()
        if usuario:
            reacciones = session.query(Reaccion).filter(Reaccion.usuario_id == usuario.id).all()

            if reacciones:
                st.write(f"Publicaciones donde **{usuario_seleccionado}** reaccionó:")
                for r in reacciones:
                    contenido_pub = r.publicacion.contenido if r.publicacion else "Publicación no disponible"
                    st.markdown(f"- Publicación: {contenido_pub}  \n  Reacción: {r.tipo_reaccion}")
            else:
                st.info(f"El usuario {usuario_seleccionado} no ha reaccionado a ninguna publicación.")
        else:
            st.error("Usuario no encontrado.")

    session.close()
