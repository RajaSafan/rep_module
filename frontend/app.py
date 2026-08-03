import requests
import streamlit as st


API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

# Temporary organization ID for standalone testing.
ORGANIZATION_ID = "11111111-1111-1111-1111-111111111111"


st.set_page_config(
    page_title="Representative Module",
    page_icon="👥",
    layout="wide",
)

st.title("Representative Management")
st.caption("Add and manage company representatives.")


def get_error_message(response: requests.Response) -> str:
    try:
        error_data = response.json()

        detail = error_data.get("detail")

        if isinstance(detail, str):
            return detail

        return str(error_data)

    except ValueError:
        return response.text or "An unexpected error occurred."


def fetch_representatives() -> list[dict]:
    try:
        response = requests.get(
            f"{API_BASE_URL}/representatives",
            params={
                "organization_id": ORGANIZATION_ID,
            },
            timeout=30,
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        st.error(f"Could not load representatives: {error}")
        return []


def add_representative(
    representative_name: str,
    service: str,
    company_email: str,
) -> tuple[bool, str]:
    payload = {
        "organization_id": ORGANIZATION_ID,
        "representative_name": representative_name,
        "service": service,
        "company_email": company_email,
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/representatives",
            json=payload,
            timeout=30,
        )

        if response.status_code == 201:
            return (
                True,
                "Representative added and invitation email processed.",
            )

        return (
            False,
            f"{response.status_code}: {get_error_message(response)}",
        )

    except requests.RequestException as error:
        return False, str(error)


def delete_representative(
    representative_id: str,
) -> tuple[bool, str]:
    try:
        response = requests.delete(
            f"{API_BASE_URL}/representatives/{representative_id}",
            timeout=30,
        )

        if response.status_code == 204:
            return True, "Representative deleted successfully."

        return (
            False,
            f"{response.status_code}: {get_error_message(response)}",
        )

    except requests.RequestException as error:
        return False, str(error)


with st.form(
    "add_representative_form",
    clear_on_submit=True,
):
    st.subheader("Add Representative")

    representative_name = st.text_input(
        "Representative Name",
        placeholder="Ali",
    )

    service = st.text_input(
        "Service",
        placeholder="Vehicle Inspection",
    )

    company_email = st.text_input(
        "Company Email",
        placeholder="ali@company.com",
    )

    submitted = st.form_submit_button(
        "Add Representative",
        use_container_width=True,
    )

    if submitted:
        if not representative_name.strip():
            st.error("Representative name is required.")

        elif not service.strip():
            st.error("Service is required.")

        elif not company_email.strip():
            st.error("Company email is required.")

        else:
            success, message = add_representative(
                representative_name=representative_name.strip(),
                service=service.strip(),
                company_email=company_email.strip(),
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


st.divider()
st.subheader("Representatives")

representatives = fetch_representatives()

if not representatives:
    st.info("No representatives added yet.")

else:
    for representative in representatives:
        with st.container(border=True):
            col1, col2, col3, col4, col5, col6 = st.columns(
                [1.2, 1.4, 1.8, 1.2, 1.2, 0.8]
            )

            with col1:
                st.write("**Representative**")
                st.write(
                    representative["representative_name"]
                )

            with col2:
                st.write("**Service**")
                st.write(representative["service"])

            with col3:
                st.write("**Company Email**")
                st.write(representative["company_email"])

            with col4:
                st.write("**Invitation**")

                invitation_status = representative.get(
                    "invitation_status",
                    "Pending",
                )

                if invitation_status == "Accepted":
                    st.success("Accepted")
                elif invitation_status == "Sent":
                    st.info("Sent")
                elif invitation_status == "Email Failed":
                    st.error("Email Failed")
                elif invitation_status == "Expired":
                    st.warning("Expired")
                else:
                    st.warning(invitation_status)

            with col5:
                st.write("**Calendar**")

                if representative["calendar_connected"]:
                    st.success("Connected")
                else:
                    st.warning("Not Connected")

            with col6:
                st.write("**Action**")

                if st.button(
                    "Delete",
                    key=(
                        f"delete_"
                        f"{representative['representative_id']}"
                    ),
                    use_container_width=True,
                ):
                    deleted, message = delete_representative(
                        representative["representative_id"]
                    )

                    if deleted:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)