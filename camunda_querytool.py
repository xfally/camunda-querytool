import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

title = "Camunda Process Instance Query Tool"

st.set_page_config(
    page_title=title,
    page_icon=":mag:",  # 放大镜图标
    layout="wide",
)

st.session_state.base_url = st.session_state.get(
    "base_url", "http://localhost:8080/engine-rest"
)
st.session_state.username = st.session_state.get("username", "")
st.session_state.password = st.session_state.get("password", "")
st.session_state.token = st.session_state.get("token", "")

# 侧边栏认证配置
with st.sidebar:
    st.header("Connection Configuration")

    st.session_state.base_url = st.text_input(
        "Camunda Base URL", st.session_state.base_url
    )

    # 认证方式选择
    auth_method = st.radio(
        "Select Authentication Method", ("Bearer Token", "Basic Auth")
    )

    if auth_method == "Bearer Token":
        st.session_state.token = st.text_input(
            "Bearer Token", st.session_state.token, type="password"
        )
    else:
        st.session_state.username = st.text_input("Username", st.session_state.username)
        st.session_state.password = st.text_input(
            "Password", st.session_state.password, type="password"
        )

    # 连接测试按钮
    def test_connection():
        try:
            headers = {}
            if auth_method == "Bearer Token":
                headers["Authorization"] = f"Bearer {st.session_state.token}"
                response = requests.get(
                    f"{st.session_state.base_url}/engine", headers=headers
                )
            else:
                response = requests.get(
                    f"{st.session_state.base_url}/engine",
                    auth=HTTPBasicAuth(
                        st.session_state.username, st.session_state.password
                    ),
                )

            if response.status_code == 200:
                st.success("Connection successful!")
            else:
                st.error(f"Connection failed! Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button("Test Connection"):
        test_connection()


def query_process_instance(process_instance_id):
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.get(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}",
                headers=headers,
            )
        else:
            response = requests.get(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to query process instance. Status code: {response.status_code}"
            )
            return {}
    except Exception as e:
        st.error(f"An error occurred while querying process instance: {e}")
        return {}


def query_process_instances():
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.get(
                f"{st.session_state.base_url}/process-instance", headers=headers
            )
        else:
            response = requests.get(
                f"{st.session_state.base_url}/process-instance",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to query process instances. Status code: {response.status_code}"
            )
            return []
    except Exception as e:
        st.error(f"An error occurred while queying process instances: {e}")
        return []


def query_history_process_instances():
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.get(
                f"{st.session_state.base_url}/history/process-instance", headers=headers
            )
        else:
            response = requests.get(
                f"{st.session_state.base_url}/history/process-instance",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to query history process instances. Status code: {response.status_code}"
            )
            return []
    except Exception as e:
        st.error(f"An error occurred while querying history process instances: {e}")
        return []


def delete_process_instance(process_instance_id):
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.delete(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}?skipCustomListeners=true&skipIoMappings=true&failIfNotExists=false",
                headers=headers,
            )
        else:
            response = requests.delete(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}?skipCustomListeners=true&skipIoMappings=true&failIfNotExists=false",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 204:
            st.success(f"Process instance {process_instance_id} deleted successfully!")
        else:
            st.error(
                f"Failed to delete process instance {process_instance_id}. Status code: {response.status_code}"
            )
    except Exception as e:
        st.error(
            f"An error occurred while deleting process instance {process_instance_id}: {e}"
        )


def delete_history_process_instance(history_process_instance_id):
    # 该实例可能在进行中，先尝试删除进行中的实例
    delete_process_instance(history_process_instance_id)
    # 然后才能删除历史实例
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.delete(
                f"{st.session_state.base_url}/history/process-instance/{history_process_instance_id}?failIfNotExists=false",
                headers=headers,
            )
        else:
            response = requests.delete(
                f"{st.session_state.base_url}/history/process-instance/{history_process_instance_id}?failIfNotExists=false",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 204:
            st.success(
                f"History Process instance {history_process_instance_id} deleted successfully!"
            )
        else:
            st.error(
                f"Failed to delete history process instance {history_process_instance_id}. Status code: {response.status_code}"
            )
    except Exception as e:
        st.error(
            f"An error occurred while deleting history process instance {history_process_instance_id}: {e}"
        )


def view_process_instance_variables(process_instance_id):
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.get(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}/variables?deserializeValues=false",
                headers=headers,
            )
        else:
            response = requests.get(
                f"{st.session_state.base_url}/process-instance/{process_instance_id}/variables?deserializeValues=false",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to retrieve variables for process instance {process_instance_id}. Status code: {response.status_code}"
            )
    except Exception as e:
        st.error(
            f"An error occurred while retrieving variables for process instance {process_instance_id}: {e}"
        )


def view_history_process_instance_variables(history_process_instance_id):
    try:
        headers = {}
        if auth_method == "Bearer Token":
            headers["Authorization"] = f"Bearer {st.session_state.token}"
            response = requests.get(
                f"{st.session_state.base_url}/history/variable-instance?processInstanceId={history_process_instance_id}&deserializeValues=false",
                headers=headers,
            )
        else:
            response = requests.get(
                f"{st.session_state.base_url}/history/variable-instance?processInstanceId={history_process_instance_id}&deserializeValues=false",
                auth=HTTPBasicAuth(
                    st.session_state.username, st.session_state.password
                ),
            )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(
                f"Failed to retrieve variables for history process instance {history_process_instance_id}. Status code: {response.status_code}"
            )
    except Exception as e:
        st.error(
            f"An error occurred while retrieving variables for history process instance {history_process_instance_id}: {e}"
        )


# 设置页面标题
st.title(title)

# Tab区分不同的请求页面
tab1, tab2 = st.tabs(["Process Instances", "History Process Instances"])


@st.dialog("View Process Instance Variables", width="large")
def view_process_instance_variables_dialog(process_instance_id):
    st.write(f"Process Instance: {process_instance_id}")
    variables = view_process_instance_variables(process_instance_id)
    if variables:
        st.write(variables)


@st.dialog("View History Process Instance Variables", width="large")
def view_history_process_instance_variables_dialog(
    history_process_instance_id,
):
    st.write(f"History Process Instance: {history_process_instance_id}")
    variables = view_history_process_instance_variables(history_process_instance_id)
    if variables:
        st.write(variables)


@st.dialog("Delete Process Instances")
def delete_process_instances_dialog(process_instance_ids):
    st.write(f"Are you sure to delete Process Instances:")
    st.write(process_instance_ids)
    if st.button("Delete", key="delete_process_instances"):
        for process_instance_id in process_instance_ids:
            delete_process_instance(process_instance_id)
        st.session_state.pop("selected_process_instance_ids", None)  # 删除缓存


@st.dialog("Delete History Process Instances")
def delete_history_process_instances_dialog(history_process_instance_ids):
    st.write(
        f"Are you sure to delete History Process Instances (This operation will also delete related Process Instances):"
    )
    st.write(history_process_instance_ids)
    if st.button("Delete", key="delete_history_process_instances"):
        for history_process_instance_id in history_process_instance_ids:
            delete_history_process_instance(history_process_instance_id)
        st.session_state.pop("selected_history_process_instance_ids", None)  # 删除缓存


with tab1:
    st.header("Process Instances")

    # 查询按钮
    if st.button("Query Process Instances"):
        # 查询数据
        st.session_state.process_instances = query_process_instances()

    # 显示数据
    if "process_instances" in st.session_state and st.session_state.process_instances:
        st.write(
            f"Total number of process instances: {len(st.session_state.process_instances)}"
        )
        event = st.dataframe(
            st.session_state.process_instances,
            selection_mode="multi-row",
            on_select="rerun",
        )
        # 记录选中行
        row_indexs = event.selection.rows
        if row_indexs:
            st.session_state.selected_process_instance_ids = []
            for row_index in row_indexs:
                selected_process_instance_id = st.session_state.process_instances[
                    row_index
                ]["id"]
                st.session_state.selected_process_instance_ids.append(
                    selected_process_instance_id
                )
        else:
            st.session_state.pop("selected_process_instance_ids", None)  # 删除缓存

    # 处理选中的流程实例
    if (
        "selected_process_instance_ids" in st.session_state
        and st.session_state.selected_process_instance_ids
    ):
        col1, col2, col3 = st.columns(3, vertical_alignment="top")
        with col1:
            st.write(
                f"Selected Process Instances: {st.session_state.selected_process_instance_ids}"
            )

        with col2:
            # 查看变量按钮
            if st.button("View Variables", use_container_width=True):
                if st.session_state.selected_process_instance_ids.__len__() > 1:
                    st.error("Please select only one process instance.")
                else:
                    view_process_instance_variables_dialog(
                        st.session_state.selected_process_instance_ids[0]
                    )

        with col3:
            # 删除按钮
            if st.button("Delete Process Instance", use_container_width=True):
                delete_process_instances_dialog(
                    st.session_state.selected_process_instance_ids
                )


with tab2:
    st.header("History Process Instances")

    # 查询按钮
    if st.button("Query History Process Instances"):
        # 查询数据
        st.session_state.history_process_instances = query_history_process_instances()

    # 显示数据
    if (
        "history_process_instances" in st.session_state
        and st.session_state.history_process_instances
    ):
        st.write(
            f"Total number of history process instances: {len(st.session_state.history_process_instances)}"
        )
        event = st.dataframe(
            st.session_state.history_process_instances,
            selection_mode="multi-row",
            on_select="rerun",
        )
        # 记录选中行
        row_indexs = event.selection.rows
        if row_indexs:
            st.session_state.selected_history_process_instance_ids = []
            for row_index in row_indexs:
                selected_history_process_instance_id = (
                    st.session_state.history_process_instances[row_index]["id"]
                )
                st.session_state.selected_history_process_instance_ids.append(
                    selected_history_process_instance_id
                )
        else:
            st.session_state.pop(
                "selected_history_process_instance_ids", None
            )  # 删除缓存

    # 处理选中的流程实例
    if (
        "selected_history_process_instance_ids" in st.session_state
        and st.session_state.selected_history_process_instance_ids
    ):
        col1, col2, col3 = st.columns(3, vertical_alignment="top")
        with col1:
            st.write(
                f"Selected History Process Instances: {st.session_state.selected_history_process_instance_ids}"
            )

        with col2:
            # 查看变量按钮
            if st.button("View History Variables", use_container_width=True):
                if st.session_state.selected_history_process_instance_ids.__len__() > 1:
                    st.error("Please select only one history process instance.")
                else:
                    view_history_process_instance_variables_dialog(
                        st.session_state.selected_history_process_instance_ids[0]
                    )

        with col3:
            # 删除按钮
            if st.button("Delete History Process Instance", use_container_width=True):
                delete_history_process_instances_dialog(
                    st.session_state.selected_history_process_instance_ids,
                )
