import copy
import streamlit as st
from model import Model
from bank_branch import Operation


if __name__ == '__main__':
    st.title('Bank branch simulation 🏫')
    tab1, tab2, tab3 = st.tabs(["Parameters", "Step simulation", "Full simulation"])

    with tab1:
        st.subheader('Simulation parameters:')
        clerk_count = st.slider('Number of clerks:', 2, 7, value=3)
        distribution = st.selectbox('Probability distribution:', ['uniform', 'normal'])
        col1, col2, col3, col4 = st.columns([6, 2, 1, 2])
        with col1:
            st.text('Order interval (minutes):')
            st.text('\n'); st.text('\n'); st.text('\n')
            st.text('Service duration interval (minutes):')
        with col2:
            client_min_minutes = st.number_input('from', 0, step=1, key=1)
            service_min_minutes = st.number_input('from', 0, value=10, step=1, key=2)
        with col3:
            st.text(' ... ')
            st.text('\n'); st.text('\n'); st.text('\n')
            st.text(' ... ')
        with col4:
            client_max_minutes = st.number_input('to', client_min_minutes + 1, value=10, step=1, key=3)
            service_max_minutes = st.number_input('to', service_min_minutes + 1, value=30, step=1, key=4)
        queue_max_length = st.slider('Max queue length:', 5, 20, value=10)
        step_size_minutes = st.slider('Simulation step (minutes):', 1, 20, value=2)
        step_count = st.number_input('Number of steps:', 1, value=1000, step=1)
        st.text('\n')
        if st.button('SAVE ✅') or 'model' not in st.session_state:
            st.session_state.model = Model(clerk_count, distribution, client_min_minutes, client_max_minutes,
                    service_min_minutes, service_max_minutes, queue_max_length, step_size_minutes, step_count)
            st.session_state.old_stats = st.session_state.model.get_stats()

    with tab2:
        if st.button('RESTART 🔁', key=10):
            st.session_state.model = Model(clerk_count, distribution, client_min_minutes, client_max_minutes,
                    service_min_minutes, service_max_minutes, queue_max_length, step_size_minutes, step_count)
            st.session_state.old_stats = st.session_state.model.get_stats()
        if st.button('STEP', use_container_width=True, key=11):
            updates = st.session_state.model.step()
            stats = st.session_state.model.get_stats()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("queue_length", stats.queue_length,
                          stats.queue_length - st.session_state.old_stats.queue_length)
                st.metric("clerks_occupied", stats.clerks_occupied,
                          stats.clerks_occupied - st.session_state.old_stats.clerks_occupied)
            with col2:
                st.metric("clients_served", stats.clients_served,
                          stats.clients_served - st.session_state.old_stats.clients_served)
                st.metric("clients_lost", stats.clients_lost,
                          stats.clients_lost - st.session_state.old_stats.clients_lost)
            with col3:
                st.metric("avg_queue_length", stats.avg_queue_length,
                          stats.avg_queue_length - st.session_state.old_stats.avg_queue_length)
                st.metric("max_queue_length", stats.max_queue_length,
                          stats.max_queue_length - st.session_state.old_stats.max_queue_length)
            with col4:
                st.metric("avg_waiting_time_minutes", stats.avg_waiting_time_minutes,
                          stats.avg_waiting_time_minutes - st.session_state.old_stats.avg_waiting_time_minutes)
                st.metric("avg_clerk_utilization", stats.avg_clerk_utilization,
                          stats.avg_clerk_utilization - st.session_state.old_stats.avg_clerk_utilization)
            st.session_state.old_stats = copy.copy(stats)
            st.subheader(f"Profit = {st.session_state.model.get_current_profit():.2f}")
            for update in updates:
                if update[0] == Operation.STAND_INTO_QUEUE:
                    st.text(f'Client {update[1]} -> Queue')
                if update[0] == Operation.START_SERVICE:
                    st.text(f'Client {update[2]} -> Clerk {update[1]}')
                if update[0] == Operation.FINISH_SERVICE:
                    st.text(f'Clerk {update[1]} finished with Client {update[2]}')
                if update[0] == Operation.LEAVE_QUEUE:
                    st.text(f'Client {update[1]} Left')

    with tab3:
        if st.button('RESTART 🔁', key=12):
            st.session_state.model = Model(clerk_count, distribution, client_min_minutes, client_max_minutes,
                    service_min_minutes, service_max_minutes, queue_max_length, step_size_minutes, step_count)
        if st.button('SIMULATE', use_container_width=True, key=13):
            st.session_state.model.simulate()
            stats = st.session_state.model.get_stats()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("queue_length", stats.queue_length)
                st.metric("clerks_occupied", stats.clerks_occupied)
            with col2:
                st.metric("clients_served", stats.clients_served)
                st.metric("clients_lost", stats.clients_lost)
            with col3:
                st.metric("avg_queue_length", stats.avg_queue_length)
                st.metric("max_queue_length", stats.max_queue_length)
            with col4:
                st.metric("avg_waiting_time_minutes", stats.avg_waiting_time_minutes)
                st.metric("avg_clerk_utilization", stats.avg_clerk_utilization)
            st.subheader(f"Profit = {st.session_state.model.get_current_profit():.2f}")
