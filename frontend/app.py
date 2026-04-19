import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Banking RAG Chatbot", layout="wide")

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

if "data_uploaded" not in st.session_state:
    st.session_state.data_uploaded = False


# ---------------- LOGIN ----------------
def login_ui():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner("Logging in..."):
            try:
                res = requests.post(
                    f"{API_URL}/token",
                    data={"username": username, "password": password}
                )

                if res.status_code == 200:
                    data = res.json()
                    token = data.get("access_token")

                    if token:
                        st.session_state.token = token
                        st.success("Login successful ✅")
                        st.rerun()
                    else:
                        st.error("No token received ❌")

                else:
                    st.error("Invalid credentials ❌")

            except Exception as e:
                st.error(f"Backend not reachable: {e}")


# ---------------- MAIN APP ----------------
def main_app():
    st.title("Banking RAG Chatbot")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # -------- SIDEBAR --------
    with st.sidebar:
        st.header("Upload Dataset")

        uploaded_file = st.file_uploader(
            "Upload CSV or Excel",
            type=["csv", "xlsx"]
        )

        if uploaded_file is not None:
            if st.button("Upload File"):
                with st.spinner("Uploading..."):
                    try:
                        files = {
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type
                            )
                        }

                        res = requests.post(
                            f"{API_URL}/upload",
                            files=files,
                            headers=headers
                        )

                        if res.status_code == 200:
                            st.success("Uploaded successfully ✅")
                            st.session_state.data_uploaded = True
                        else:
                            st.error("Upload failed ❌")
                            st.text(res.text)

                    except Exception as e:
                        st.error(f"Error: {e}")

        if st.session_state.data_uploaded:
            st.success("✅ Dataset Ready")

        if st.button("Logout"):
            st.session_state.token = None
            st.session_state.data_uploaded = False
            st.rerun()

    # -------- CHAT --------
    st.subheader("💬 Ask a banking question")

    query = st.text_input(
        "Enter your query",
        disabled=not st.session_state.data_uploaded
    )

    if not st.session_state.data_uploaded:
        st.warning("⚠️ Please upload dataset from sidebar to enable chat")

    if st.button("Ask"):
        if not st.session_state.data_uploaded:
            st.warning("Upload dataset first ❗")
            return

        if query.strip() == "":
            st.warning("Please enter a question")
            return

        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    f"{API_URL}/chat",
                    json={"query": query},
                    headers=headers
                )

                if res.status_code == 200:
                    data = res.json()
                    st.success(data.get("response", "No response"))
                else:
                    st.error(f"Error: {res.status_code}")
                    st.text(res.text)

            except Exception as e:
                st.error(f"Error: {e}")


# ---------------- ROUTER ----------------
if not st.session_state.token:
    login_ui()
else:
    main_app()