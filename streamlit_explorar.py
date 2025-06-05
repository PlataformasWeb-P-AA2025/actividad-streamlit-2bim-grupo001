# explorador_streamlit.py

import streamlit as st
from db import get_session
from clases import Usuario, Publicacion, Reaccion
import consulta1, consulta2, consulta3, consulta4, consulta5

st.set_page_config(page_title="Base de Red FutRedx", layout="wide")

def listar_usuarios():
    st.header("Usuarios")
    session = get_session()
    usuarios = session.query(Usuario).all()

    if not usuarios:
        st.info("No hay usuarios registrados.")
        session.close()
        return

    for u in usuarios:
        with st.expander(f"ID {u.id} → {u.nombre_usuario}", expanded=False):
            st.write(f"**ID:** {u.id}")
            st.write(f"**Nombre de usuario:** {u.nombre_usuario}")
            
            # Publicaciones
            if u.publicaciones:
                st.write("**Publicaciones:**")
                filas_pub = []
                for p in u.publicaciones:
                    filas_pub.append({
                        "Publicación ID": p.id,
                        "Contenido": p.contenido,
                        "Reacciones": len(p.reacciones),
                    })
                st.table(filas_pub)
            else:
                st.write("Este usuario no tiene publicaciones.")
            
            # Reacciones (solo las primeras 10)
            if u.reacciones:
                st.write("**Reacciones hechas (máx. 10):**")
                filas_rea = []
                for r in u.reacciones[:10]:
                    filas_rea.append({
                        "Reacción ID": r.id,
                        "Tipo": r.tipo_reaccion,
                        "Publicación": r.publicacion.contenido,
                    })
                st.table(filas_rea)
            else:
                st.write("Este usuario no tiene reacciones.")
    session.close()

def listar_publicaciones():
    st.header("Publicaciones")
    session = get_session()
    publicaciones = session.query(Publicacion).all()

    if not publicaciones:
        st.info("No hay publicaciones registradas.")
        session.close()
        return

    for p in publicaciones:
        with st.expander(f"ID {p.id} → {p.contenido[:40]}", expanded=False):
            st.write(f"**ID:** {p.id}")
            st.write(f"**Contenido:** {p.contenido}")
            st.write(f"**Autor:** {p.usuario.nombre_usuario}")
            st.write(f"**Reacciones:** {len(p.reacciones)}")

            if p.reacciones:
                st.write("**Reacciones recibidas (máx. 10):**")
                filas_rea = []
                for r in p.reacciones[:10]:
                    filas_rea.append({
                        "Reacción ID": r.id,
                        "Usuario": r.usuario.nombre_usuario,
                        "Tipo": r.tipo_reaccion,
                    })
                st.table(filas_rea)
            else:
                st.write("Ninguna reacción aún.")
    session.close()


def listar_reacciones():
    st.header("Reacciones")
    session = get_session()
    
    # Solo se obtienen las primeras 100 reacciones
    reacciones = session.query(Reaccion).limit(100).all()

    if not reacciones:
        st.info("No hay reacciones registradas.")
        session.close()
        return

    filas = []
    for r in reacciones:
        filas.append({
            "Reacción ID": r.id,
            "Usuario": r.usuario.nombre_usuario,
            "Publicación": r.publicacion.contenido,
            "Tipo": r.tipo_reaccion,
        })
    st.table(filas)
    session.close()


def main():
    st.title("Base de Red FutRedx")

    # Menú principal
    menu = st.sidebar.radio("Selecciona una sección:", ("Entidades", "Consultas"))

    if menu == "Entidades":
        entidad = st.sidebar.selectbox(
            "Selecciona una entidad:",
            ("Usuarios", "Publicaciones", "Reacciones")
        )

        if entidad == "Usuarios":
            listar_usuarios()
        elif entidad == "Publicaciones":
            listar_publicaciones()
        elif entidad == "Reacciones":
            listar_reacciones()

    elif menu == "Consultas":
        consulta = st.sidebar.selectbox(
            "Selecciona una consulta:",
            (
                "Consulta1 - Publicaciones por usuario",
                "Consulta2 - Reacciones de usuario por publicación",
                "Consulta3 - Reacciones con tipos específicos y nombre no vocal",
                "Consulta4 - Publicaciones con todos los tipos de reacciones",
                "Consulta5 - Publicaciones donde reaccionó un usuario"
            )
        )

        if consulta.startswith("Consulta1"):
            import consulta1
            consulta1.ejecutar()
        elif consulta.startswith("Consulta2"):
            import consulta2
            consulta2.ejecutar()
        elif consulta.startswith("Consulta3"):
            import consulta3
            consulta3.ejecutar()
        elif consulta.startswith("Consulta4"):
            import consulta4
            consulta4.ejecutar()
        elif consulta.startswith("Consulta5"):
            import consulta5
            consulta5.ejecutar()


if __name__ == "__main__":
    main()
