import copy
from datetime import datetime, timedelta

import streamlit as st
from pandas import DataFrame

from config import TIMETABLE, LUNCH_START, LUNCH_END, CLERK_COUNT_START_VALUE, CLERK_COUNT_RANGE, DISTRIBUTIONS, \
    SIM_DEFAULT_DURATION_DAYS, PROBABILITY_START_VALUE, STEP_SIZE_RANGE, STEP_SIZE_DEFAULT, QUEUE_LENGTH_RANGE, \
    QUEUE_LENGTH_START, SERVICE_MIN_MIN, SERVICE_MIN_START, SERVICE_MIN_STEP, SERVICE_MAX_START, SERVICE_MAX_STEP
from distribution import Distribution
from model import Model
from operation import Operation


def initialize_model(clerk_count, distribution, client_probability, service_min_minutes,
                     service_max_minutes, queue_max_length, step_size_minutes, simulation_end):
    st.session_state.model = Model(clerk_count, distribution, client_probability, service_min_minutes,
                                   service_max_minutes, queue_max_length, step_size_minutes, simulation_end)
    st.session_state.old_stats = st.session_state.model.stats


def enter_parameters():
    st.subheader('Simulation parameters:')
    clerk_count = st.slider('Number of clerks:', *CLERK_COUNT_RANGE, value=CLERK_COUNT_START_VALUE)
    distribution = Distribution(st.selectbox('Probability distribution:', DISTRIBUTIONS))
    col1, col2, col3, col4 = st.columns([6, 2, 1, 2])
    with col1:
        st.text('Service duration interval (minutes):')
    with col2:
        service_min_minutes = \
            st.number_input('from', SERVICE_MIN_MIN, value=SERVICE_MIN_START, step=SERVICE_MIN_STEP, key=2)
    with col3:
        st.text(' ... ')
    with col4:
        service_max_minutes = \
            st.number_input('to', service_min_minutes + 1, value=SERVICE_MAX_START, step=SERVICE_MAX_STEP, key=4)
    queue_max_length = st.slider('Max queue length:', *QUEUE_LENGTH_RANGE, value=QUEUE_LENGTH_START)
    step_size_minutes = st.slider('Simulation step (minutes):', *STEP_SIZE_RANGE, value=STEP_SIZE_DEFAULT)
    client_probability = st.slider('Client arrival probability (during step):', 0., 1., value=PROBABILITY_START_VALUE)
    simulation_end = st.date_input('Simulation end:', value=datetime.now() + timedelta(days=SIM_DEFAULT_DURATION_DAYS),
                                   min_value=datetime.now() + timedelta(hours=3))
    st.text('\n')
    if st.button('SAVE ✅') or 'model' not in st.session_state:
        initialize_model(clerk_count, distribution, client_probability, service_min_minutes,
                         service_max_minutes, queue_max_length, step_size_minutes, simulation_end)
    return clerk_count, distribution, client_probability, service_min_minutes, \
           service_max_minutes, queue_max_length, step_size_minutes, simulation_end


def display_updates(updates):
    for update in updates:
        if update[0] == Operation.STAND_INTO_QUEUE:
            st.text(f'Client {update[1]} -> Queue')
        if update[0] == Operation.START_SERVICE:
            st.text(f'Client {update[2]} -> Clerk {update[1]}')
        if update[0] == Operation.FINISH_SERVICE:
            st.text(f'Clerk {update[1]} finished with Client {update[2]}')
        if update[0] == Operation.LEAVE_QUEUE:
            st.text(f'Client {update[1]} Left')


def simulate_step():
    if st.button('RESTART 🔁', key=10):
        initialize_model(clerk_count, distribution, client_probability, service_min_minutes,
                         service_max_minutes, queue_max_length, step_size_minutes, simulation_end)
    if st.button('STEP', use_container_width=True, key=11):
        updates = st.session_state.model.step()
        st.subheader(f"Current time: {st.session_state.model.current_time.strftime('%H:%M, %d.%m.%Y')}")
        stats = st.session_state.model.stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("queue_length", stats.queue_length,
                      stats.queue_length - st.session_state.old_stats.queue_length)
            st.metric("clerks_occupied", f"{stats.clerks_occupied}/{clerk_count}",
                      stats.clerks_occupied - st.session_state.old_stats.clerks_occupied)
        with col2:
            st.metric("clients_served", stats.clients_served,
                      stats.clients_served - st.session_state.old_stats.clients_served)
            st.metric("clients_lost", stats.clients_lost,
                      stats.clients_lost - st.session_state.old_stats.clients_lost)
        with col3:
            st.metric("avg_queue_length", f"{stats.avg_queue_length:.2f}",
                      stats.avg_queue_length - st.session_state.old_stats.avg_queue_length)
            st.metric("max_queue_length", stats.max_queue_length,
                      stats.max_queue_length - st.session_state.old_stats.max_queue_length)
        with col4:
            st.metric("avg_waiting_time_minutes", f"{stats.avg_waiting_time_minutes:.2f}",
                      stats.avg_waiting_time_minutes - st.session_state.old_stats.avg_waiting_time_minutes)
            st.metric("avg_clerk_utilization", f"{stats.avg_clerk_utilization:.2f}",
                      stats.avg_clerk_utilization - st.session_state.old_stats.avg_clerk_utilization)
        st.session_state.old_stats = copy.copy(stats)
        st.subheader(f"Profit = {st.session_state.model.current_profit:.2f}")
        display_updates(updates)


def simulate_full():
    if st.button('RESTART 🔁', key=12):
        initialize_model(clerk_count, distribution, client_probability, service_min_minutes,
                         service_max_minutes, queue_max_length, step_size_minutes, simulation_end)
    if st.button('SIMULATE', use_container_width=True, key=13):
        st.session_state.model.simulate()
        stats = st.session_state.model.stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("clients_served", stats.clients_served)
            st.metric("clients_lost", stats.clients_lost)
        with col2:
            st.metric("avg_queue_length", f"{stats.avg_queue_length:.2f}")
            st.metric("max_queue_length", stats.max_queue_length)
        with col3:
            st.metric("avg_waiting_time_minutes", f"{stats.avg_waiting_time_minutes:.2f}")
            st.metric("avg_clerk_utilization", f"{stats.avg_clerk_utilization:.2f}")
        st.subheader(f"Profit = {st.session_state.model.current_profit:.2f}")


def display_timetable():
    st.subheader("Bank branch timetable:")
    st.table(DataFrame(TIMETABLE, columns=['from', 'to'], index=['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']))
    st.text(f"Lunch break: {LUNCH_START} - {LUNCH_END}")


if __name__ == '__main__':
    st.title('Bank branch simulation 🏫')
    param_page, step_sim_page, full_sim_page, timetable_page = \
        st.tabs(["Parameters", "Step simulation", "Full simulation", "Timetable"])

    with param_page:
        clerk_count, distribution, client_probability, service_min_minutes, \
        service_max_minutes, queue_max_length, step_size_minutes, simulation_end = enter_parameters()

    with step_sim_page:
        simulate_step()

    with full_sim_page:
        simulate_full()

    with timetable_page:
        display_timetable()
