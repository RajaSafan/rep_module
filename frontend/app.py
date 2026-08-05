# import requests
# import streamlit as st


# API_BASE_URL = st.secrets.get(
#     "API_BASE_URL",
#     "http://127.0.0.1:8000",
# )

# ORGANIZATION_ID = "11111111-1111-1111-1111-111111111111"

# # Render free services may take time to wake up.
# REQUEST_TIMEOUT = 120


# st.set_page_config(
#     page_title="Representative Module",
#     page_icon="👥",
#     layout="wide",
# )

# st.title("Representative Management")
# st.caption("Add and manage company representatives.")


# def get_error_message(response: requests.Response) -> str:
#     try:
#         data = response.json()
#         detail = data.get("detail", data)

#         if isinstance(detail, str):
#             return detail

#         return str(detail)

#     except ValueError:
#         return response.text or "Unexpected backend error."


# def fetch_representatives() -> list[dict]:
#     try:
#         response = requests.get(
#             f"{API_BASE_URL}/representatives",
#             params={
#                 "organization_id": ORGANIZATION_ID,
#             },
#             timeout=REQUEST_TIMEOUT,
#         )

#         response.raise_for_status()
#         return response.json()

#     except requests.Timeout:
#         st.error(
#             "The backend is taking too long to respond. "
#             "Open the Render backend URL once, wait for it to start, "
#             "then refresh this page."
#         )
#         return []

#     except requests.RequestException as error:
#         st.error(f"Could not load representatives: {error}")
#         return []


# def add_representative(
#     representative_name: str,
#     service: str,
#     company_email: str,
# ) -> tuple[bool, str]:
#     payload = {
#         "organization_id": ORGANIZATION_ID,
#         "representative_name": representative_name,
#         "service": service,
#         "company_email": company_email,
#     }

#     try:
#         response = requests.post(
#             f"{API_BASE_URL}/representatives",
#             json=payload,
#             timeout=REQUEST_TIMEOUT,
#         )

#         if response.status_code == 201:
#             return (
#                 True,
#                 "Representative added successfully. "
#                 "The invitation email has been processed.",
#             )

#         return (
#             False,
#             f"{response.status_code}: {get_error_message(response)}",
#         )

#     except requests.Timeout:
#         return (
#             False,
#             "The backend timed out. Open the Render backend URL, "
#             "wait for it to start, and try again.",
#         )

#     except requests.RequestException as error:
#         return False, str(error)


# def delete_representative(
#     representative_id: str,
# ) -> tuple[bool, str]:
#     try:
#         response = requests.delete(
#             f"{API_BASE_URL}/representatives/{representative_id}",
#             timeout=REQUEST_TIMEOUT,
#         )

#         if response.status_code == 204:
#             return True, "Representative deleted successfully."

#         return (
#             False,
#             f"{response.status_code}: {get_error_message(response)}",
#         )

#     except requests.Timeout:
#         return False, "The backend timed out. Please try again."

#     except requests.RequestException as error:
#         return False, str(error)


# with st.form(
#     "add_representative_form",
#     clear_on_submit=True,
# ):
#     st.subheader("Add Representative")

#     representative_name = st.text_input(
#         "Representative Name",
#         placeholder="Ali",
#     )

#     service = st.text_input(
#         "Service",
#         placeholder="Vehicle Inspection",
#     )

#     company_email = st.text_input(
#         "Company Email",
#         placeholder="ali@company.com",
#     )

#     submitted = st.form_submit_button(
#         "Add Representative",
#         use_container_width=True,
#     )

#     if submitted:
#         if not representative_name.strip():
#             st.error("Representative name is required.")

#         elif not service.strip():
#             st.error("Service is required.")

#         elif not company_email.strip():
#             st.error("Company email is required.")

#         else:
#             success, message = add_representative(
#                 representative_name=representative_name.strip(),
#                 service=service.strip(),
#                 company_email=company_email.strip(),
#             )

#             if success:
#                 st.success(message)
#                 st.rerun()
#             else:
#                 st.error(message)


# st.divider()
# st.subheader("Representatives")

# representatives = fetch_representatives()

# if not representatives:
#     st.info("No representatives added yet.")

# else:
#     for representative in representatives:
#         with st.container(border=True):
#             col1, col2, col3, col4, col5, col6 = st.columns(
#                 [1.2, 1.4, 1.8, 1.2, 1.2, 0.8]
#             )

#             with col1:
#                 st.write("**Representative**")
#                 st.write(
#                     representative.get(
#                         "representative_name",
#                         "Unknown",
#                     )
#                 )

#             with col2:
#                 st.write("**Service**")
#                 st.write(
#                     representative.get(
#                         "service",
#                         "Not provided",
#                     )
#                 )

#             with col3:
#                 st.write("**Company Email**")
#                 st.write(
#                     representative.get(
#                         "company_email",
#                         "Not provided",
#                     )
#                 )

#             with col4:
#                 st.write("**Invitation**")

#                 invitation_status = representative.get(
#                     "invitation_status",
#                     "Pending",
#                 )

#                 if invitation_status == "Accepted":
#                     st.success("Accepted")

#                 elif invitation_status == "Sent":
#                     st.info("Sent")

#                 elif invitation_status == "Email Failed":
#                     st.error("Email Failed")

#                 elif invitation_status == "Expired":
#                     st.warning("Expired")

#                 else:
#                     st.warning(invitation_status)

#             with col5:
#                 st.write("**Calendar**")

#                 if representative.get(
#                     "calendar_connected",
#                     False,
#                 ):
#                     st.success("Connected")
#                 else:
#                     st.warning("Not Connected")

#             with col6:
#                 st.write("**Action**")

#                 representative_id = representative[
#                     "representative_id"
#                 ]

#                 if st.button(
#                     "Delete",
#                     key=f"delete_{representative_id}",
#                     use_container_width=True,
#                 ):
#                     deleted, message = delete_representative(
#                         representative_id
#                     )

#                     if deleted:
#                         st.success(message)
#                         st.rerun()
#                     else:
#                         st.error(message)
                        
                        
                        
# import requests
# import streamlit as st


# API_BASE_URL = st.secrets.get(
#     "API_BASE_URL",
#     "http://127.0.0.1:8000",
# )


# ORGANIZATION_ID = (
#     "11111111-1111-1111-1111-111111111111"
# )


# REQUEST_TIMEOUT = 120



# st.set_page_config(
#     page_title="Representative Module",
#     page_icon="👥",
#     layout="wide",
# )


# st.title("Representative Management")

# st.caption(
#     "Add and manage company representatives."
# )





# def get_error_message(response):

#     try:

#         data = response.json()

#         detail = data.get(
#             "detail",
#             data,
#         )


#         if isinstance(detail, str):
#             return detail


#         return str(detail)


#     except ValueError:

#         return (
#             response.text
#             or "Unexpected backend error."
#         )





# def fetch_representatives():

#     try:

#         response = requests.get(

#             f"{API_BASE_URL}/representatives",

#             params={
#                 "organization_id":
#                     ORGANIZATION_ID,
#             },

#             timeout=REQUEST_TIMEOUT,
#         )


#         response.raise_for_status()


#         return response.json()


#     except Exception as error:

#         st.error(
#             f"Could not load representatives: {error}"
#         )

#         return []





# def add_representative(
#     representative_name,
#     service,
#     service_description,
#     company_email,
# ):

#     payload = {

#         "organization_id":
#             ORGANIZATION_ID,

#         "representative_name":
#             representative_name,

#         "service":
#             service,

#         "service_description":
#             service_description,

#         "company_email":
#             company_email,
#     }



#     try:

#         response = requests.post(

#             f"{API_BASE_URL}/representatives",

#             json=payload,

#             timeout=REQUEST_TIMEOUT,

#         )


#         if response.status_code == 201:

#             return (
#                 True,
#                 "Representative added successfully."
#             )


#         return (
#             False,
#             get_error_message(response)
#         )



#     except Exception as error:

#         return (
#             False,
#             str(error)
#         )





# def delete_representative(
#     representative_id,
# ):

#     try:

#         response = requests.delete(

#             f"{API_BASE_URL}/representatives/{representative_id}",

#             timeout=REQUEST_TIMEOUT,

#         )


#         if response.status_code == 204:

#             return True


#         return False


#     except Exception:

#         return False





# with st.form(
#     "add_representative_form",
#     clear_on_submit=True,
# ):


#     st.subheader(
#         "Add Representative"
#     )


#     representative_name = st.text_input(
#         "Representative Name",
#         placeholder="Ali",
#     )


#     service = st.text_input(
#         "Service",
#         placeholder="Vehicle Inspection",
#     )


#     service_description = st.text_area(
#         "Service Description",
#         placeholder=(
#             "Describe the service "
#             "provided by this representative."
#         ),
#     )


#     company_email = st.text_input(
#         "Company Email",
#         placeholder="ali@company.com",
#     )



#     submitted = st.form_submit_button(
#         "Add Representative",
#         use_container_width=True,
#     )



#     if submitted:


#         if not representative_name.strip():

#             st.error(
#                 "Representative name is required."
#             )


#         elif not service.strip():

#             st.error(
#                 "Service is required."
#             )


#         elif not service_description.strip():

#             st.error(
#                 "Service description is required."
#             )


#         elif not company_email.strip():

#             st.error(
#                 "Company email is required."
#             )


#         else:


#             success, message = add_representative(

#                 representative_name.strip(),

#                 service.strip(),

#                 service_description.strip(),

#                 company_email.strip(),

#             )


#             if success:

#                 st.success(message)

#                 st.rerun()


#             else:

#                 st.error(message)





# st.divider()


# st.subheader(
#     "Representatives"
# )



# representatives = fetch_representatives()



# if not representatives:

#     st.info(
#         "No representatives added yet."
#     )


# else:


#     for representative in representatives:


#         with st.container(
#             border=True
#         ):


#             col1, col2, col3, col4, col5, col6 = st.columns(
#                 [
#                     1.2,
#                     1.2,
#                     1.8,
#                     2,
#                     1.2,
#                     0.8,
#                 ]
#             )



#             with col1:

#                 st.write(
#                     "**Representative**"
#                 )

#                 st.write(
#                     representative.get(
#                         "representative_name",
#                         "Unknown",
#                     )
#                 )



#             with col2:

#                 st.write(
#                     "**Service**"
#                 )

#                 st.write(
#                     representative.get(
#                         "service",
#                         "Not provided",
#                     )
#                 )



#             with col3:

#                 st.write(
#                     "**Company Email**"
#                 )

#                 st.write(
#                     representative.get(
#                         "company_email",
#                         "Not provided",
#                     )
#                 )



#             with col4:

#                 st.write(
#                     "**Service Description**"
#                 )

#                 st.write(
#                     representative.get(
#                         "service_description",
#                         "Not provided",
#                     )
#                 )



#             with col5:

#                 st.write(
#                     "**Invitation**"
#                 )


#                 status = representative.get(
#                     "invitation_status",
#                     "Pending",
#                 )


#                 if status == "Sent":

#                     st.info(
#                         "Sent"
#                     )

#                 elif status == "Email Failed":

#                     st.error(
#                         "Email Failed"
#                     )

#                 else:

#                     st.warning(
#                         status
#                     )



#             with col6:

#                 st.write(
#                     "**Action**"
#                 )


#                 representative_id = (
#                     representative[
#                         "representative_id"
#                     ]
#                 )


#                 if st.button(
#                     "Delete",
#                     key=f"delete_{representative_id}",
#                     use_container_width=True,
#                 ):

#                     if delete_representative(
#                         representative_id
#                     ):

#                         st.success(
#                             "Deleted"
#                         )

#                         st.rerun()

#                     else:

#                         st.error(
#                             "Delete failed"
#                         )



#             # Calendar status
#             if representative.get(
#                 "calendar_connected",
#                 False,
#             ):

#                 st.success(
#                     "Calendar Connected"
#                 )

#             else:

#                 st.warning(
#                     "Calendar Not Connected"
#                 )                       







import requests
import streamlit as st


API_BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)


ORGANIZATION_ID = (
    "11111111-1111-1111-1111-111111111111"
)


REQUEST_TIMEOUT = 120


st.set_page_config(
    page_title="Representative Module",
    page_icon="👥",
    layout="wide",
)


st.title("Representative Management")
st.caption(
    "Add and manage company representatives."
)



def get_error_message(response):

    try:
        data = response.json()

        detail = data.get(
            "detail",
            data,
        )

        if isinstance(detail, str):
            return detail

        return str(detail)

    except ValueError:
        return (
            response.text
            or "Unexpected backend error."
        )



def fetch_representatives():

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives",
            params={
                "organization_id": ORGANIZATION_ID,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()


    except requests.RequestException as error:

        st.error(
            f"Could not load representatives: {error}"
        )

        return []



def check_calendar_status(
    representative_id: str,
):

    try:

        response = requests.get(
            f"{API_BASE_URL}/representatives/{representative_id}/calendar/check",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()


    except requests.RequestException as error:

        return {
            "calendar_connected": False,
            "connection_status": "Unknown",
            "error": str(error),
        }



def add_representative(
    representative_name,
    service,
    service_description,
    company_email,
):

    payload = {

        "organization_id":
            ORGANIZATION_ID,

        "representative_name":
            representative_name,

        "service":
            service,

        "service_description":
            service_description,

        "company_email":
            company_email,
    }


    try:

        response = requests.post(
            f"{API_BASE_URL}/representatives",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )


        if response.status_code == 201:

            return (
                True,
                "Representative added successfully."
            )


        return (
            False,
            get_error_message(response)
        )


    except requests.RequestException as error:

        return (
            False,
            str(error)
        )



def delete_representative(
    representative_id,
):

    try:

        response = requests.delete(
            f"{API_BASE_URL}/representatives/{representative_id}",
            timeout=REQUEST_TIMEOUT,
        )


        if response.status_code == 204:

            return True


        return False


    except requests.RequestException:

        return False





with st.form(
    "add_representative_form",
    clear_on_submit=True,
):

    st.subheader(
        "Add Representative"
    )


    representative_name = st.text_input(
        "Representative Name",
        placeholder="Ali",
    )


    service = st.text_input(
        "Service",
        placeholder="Vehicle Inspection",
    )


    service_description = st.text_area(
        "Service Description",
        placeholder=(
            "Describe the service provided..."
        ),
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

            st.error(
                "Representative name is required."
            )


        elif not service.strip():

            st.error(
                "Service is required."
            )


        elif not service_description.strip():

            st.error(
                "Service description is required."
            )


        elif not company_email.strip():

            st.error(
                "Company email is required."
            )


        else:

            success, message = add_representative(
                representative_name.strip(),
                service.strip(),
                service_description.strip(),
                company_email.strip(),
            )


            if success:

                st.success(message)

                st.rerun()


            else:

                st.error(message)



st.divider()


st.subheader(
    "Representatives"
)



representatives = fetch_representatives()



if not representatives:

    st.info(
        "No representatives added yet."
    )


else:


    for representative in representatives:


        representative_id = (
            representative[
                "representative_id"
            ]
        )


        # Check real Google status
        calendar_status = check_calendar_status(
            representative_id
        )


        connection_status = (
            calendar_status.get(
                "connection_status",
                "Unknown",
            )
        )



        with st.container(border=True):


            col1, col2, col3, col4, col5, col6, col7 = st.columns(
                [
                    1.2,
                    1.2,
                    1.5,
                    2,
                    1.2,
                    1.2,
                    0.8,
                ]
            )


            with col1:

                st.write(
                    "**Representative**"
                )

                st.write(
                    representative.get(
                        "representative_name",
                        "Unknown",
                    )
                )


            with col2:

                st.write(
                    "**Service**"
                )

                st.write(
                    representative.get(
                        "service",
                        "",
                    )
                )


            with col3:

                st.write(
                    "**Email**"
                )

                st.write(
                    representative.get(
                        "company_email",
                        "",
                    )
                )


            with col4:

                st.write(
                    "**Description**"
                )

                st.write(
                    representative.get(
                        "service_description",
                        "",
                    )
                )


            with col5:

                st.write(
                    "**Invitation**"
                )


                invitation = representative.get(
                    "invitation_status",
                    "Pending",
                )


                if invitation == "Sent":

                    st.success(
                        "Sent"
                    )

                elif invitation == "Email Failed":

                    st.error(
                        "Failed"
                    )

                else:

                    st.warning(
                        invitation
                    )



            with col6:

                st.write(
                    "**Calendar**"
                )


                if connection_status == "Connected":

                    st.success(
                        "Connected"
                    )


                elif connection_status == "Revoked":

                    st.error(
                        "Revoked"
                    )


                else:

                    st.warning(
                        "Not Connected"
                    )



            with col7:

                st.write(
                    "**Action**"
                )


                if st.button(
                    "Delete",
                    key=f"delete_{representative_id}",
                    use_container_width=True,
                ):

                    if delete_representative(
                        representative_id
                    ):

                        st.success(
                            "Deleted successfully."
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Delete failed."
                        )