import streamlit as st
import requests
import time

st.title("Python компилатор през Paiza.IO API")

code = st.text_area("Въведи Python код тук:", value="""
print("Здравей, свят!")
""", height=200)

if st.button("Изпълни кода"):
    create_resp = requests.post(
        "https://api.paiza.io/runners/create.json",
        data={
            "api_key": "guest",
            "language": "python3",
            "source_code": code
        }
    )
    if create_resp.status_code != 200:
        st.error(f"Грешка при изпращане на кода: {create_resp.status_code}")
        st.stop()

    result_create = create_resp.json()
    session_id = result_create.get("id")

    if not session_id:
        st.error(f"Неуспешно получаване на session ID: {result_create}")
        st.stop()

    st.write(f"Сесия стартирана с ID: {session_id}")

    status = "running"
    while status == "running":
        time.sleep(1)
        status_resp = requests.get(
            "https://api.paiza.io/runners/get_status.json",
            params={"api_key": "guest", "id": session_id}
        )
        status_resp.raise_for_status()
        status_data = status_resp.json()
        status = status_data.get("status", "running")
        st.write(f"Статус: {status}")

    details_resp = requests.get(
        "https://api.paiza.io/runners/get_details.json",
        params={"api_key": "guest", "id": session_id}
    )
    details_resp.raise_for_status()
    details_data = details_resp.json()

    st.subheader("Резултат от изпълнението")
    st.text(details_data.get("stdout", ""))

    if details_data.get("stderr"):
        st.subheader("Грешки")
        st.text(details_data["stderr"])
