import requests

API_URL = "API_URL = "API_URL = "https://your-deployed-backend-url""

if "token" not in st.session_state:
    with st.spinner("Logging in..."):
        res = requests.post(
            f"{API_URL}/token",
            data={
                "username": "vansh",
                "password": "1234"
            }
        )

        if res.status_code == 200:
            st.session_state.token = res.json()["access_token"]
        else:
            st.error("Login failed")
            st.stop()

token = st.session_state.token


def upload_file(file, token):
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}

    return requests.post(f"{API_URL}/upload", files=files, headers=headers)


def ask_query(query, token):
    headers = {"Authorization": f"Bearer {token}"}

    return requests.post(
        f"{API_URL}/chat",
        json={"query": query},
        headers=headers
    )