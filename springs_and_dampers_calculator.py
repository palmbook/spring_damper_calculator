import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
        page_title="Spring Rates and Damper Settings Calculator by palmbook",
)

def calc_spring_rate(f, M):
    return 4 * (np.pi ** 2) * (f ** 2) * M

def calc_wheel_rate(K, mr):
    return K * (mr ** 2)

def calc_bump(M, wr, mr):
    D_crit = 2 * np.sqrt(M * wr)
    D_crit_coilover = D_crit / (mr ** 2)
    return (st.session_state.damp_target / 100) * D_crit_coilover
    
def update_widget():
    if st.session_state.natural_frequency_value <= 1:
        st.session_state.natural_frequency_display = "This natural frequency is suitable for a **passenger car**."
    elif st.session_state.natural_frequency_value <= 1.5:
        st.session_state.natural_frequency_display = "This natural frequency is suitable for a **sports car**."
    elif st.session_state.natural_frequency_value <= 2.5:
        st.session_state.natural_frequency_display = "This natural frequency is suitable for a **non-aero race car**."
    elif st.session_state.natural_frequency_value <= 3.5:
        st.session_state.natural_frequency_display = "This natural frequency is suitable for a **race car with moderate downforce**."
    else:
        st.session_state.natural_frequency_display = "This natural frequency is suitable for a **race car with high downforce**."
    
    st.session_state.rear_weight_dist = 100 - st.session_state.front_weight_dist
    
    st.session_state.front_spring_rate = calc_spring_rate(st.session_state.natural_frequency_value, (st.session_state.sprung_weight * (st.session_state.front_weight_dist / 100) / 2))
    st.session_state.rear_spring_rate = calc_spring_rate(st.session_state.natural_frequency_value, (st.session_state.sprung_weight * (st.session_state.rear_weight_dist / 100) / 2))
    
    st.session_state.front_wheel_rate = calc_wheel_rate(st.session_state.front_spring_rate, st.session_state.front_mr)
    st.session_state.rear_wheel_rate = calc_wheel_rate(st.session_state.rear_spring_rate, st.session_state.rear_mr)
    
    if st.session_state.damp_target <= 30:
        st.session_state.damping_display = "a passenger car"
    elif st.session_state.damp_target <= 50:
        st.session_state.damping_display = "a performance/track car"
    else:
        st.session_state.damping_display = "a dedicated race car"
        
    if st.session_state.br_ratio == '2:1':
        st.session_state.br_ratio_text = "Comfort-oriented Ratio"
        st.session_state.rebound_mult = 2
    else:
        st.session_state.br_ratio_text = "Recommended Ratio for Most Cars"
        st.session_state.rebound_mult = 3
    
    st.session_state.front_bump = calc_bump((st.session_state.sprung_weight * (st.session_state.front_weight_dist / 100) / 2), st.session_state.front_wheel_rate, st.session_state.front_mr)
    st.session_state.rear_bump = calc_bump((st.session_state.sprung_weight * (st.session_state.rear_weight_dist / 100) / 2), st.session_state.rear_wheel_rate, st.session_state.rear_mr)
    

    
# Initialize session state for text display
if "natural_frequency_display" not in st.session_state:
    st.session_state.natural_frequency_display = "This natural frequency is suitable for a **non-aero race car**."
if "rear_weight_dist" not in st.session_state:
    st.session_state.rear_weight_dist = 50
if "front_spring_rate" not in st.session_state:
    st.session_state.front_spring_rate = calc_spring_rate(2.5, 1000 / 4)
if "rear_spring_rate" not in st.session_state:
    st.session_state.rear_spring_rate = calc_spring_rate(2.5, 1000 / 4)
if "front_wheel_rate" not in st.session_state:
    st.session_state.front_wheel_rate = calc_wheel_rate(st.session_state.front_spring_rate, 0.5)
if "rear_wheel_rate" not in st.session_state:
    st.session_state.rear_wheel_rate = calc_wheel_rate(st.session_state.rear_spring_rate, 0.5)
if "damp_target" not in st.session_state:
    st.session_state.damp_target = 50
if "damping_display" not in st.session_state:
    st.session_state.damping_display = "a passenger car"
if "front_bump" not in st.session_state:
    st.session_state.front_bump = calc_bump(1000 / 4, st.session_state.front_wheel_rate, 0.5)
if "rear_bump" not in st.session_state:
    st.session_state.rear_bump = calc_bump(1000 / 4, st.session_state.rear_wheel_rate, 0.5)
if "br_ratio_text" not in st.session_state:
    st.session_state.br_ratio_text = "Recommended Ratio for Most Cars"
if "rebound_mult" not in st.session_state:
    st.session_state.rebound_mult = 3
    
st.title("Automotive Spring Rates and Damper Settings Calculator")
st.divider() 

st.subheader("Spring Rates")

st.number_input("Sprung Weight", min_value=0, value=1000, step=1, key="sprung_weight", on_change=update_widget)

st.slider("Front Weight Distribution (%)", 0.0, 100.0, step=0.1, value=50.0, key="front_weight_dist", on_change=update_widget)
st.markdown("Rear Distribution is {:.2f}%".format(st.session_state.rear_weight_dist))

st.slider("Select Natural Frequency Target", 0.5, 6.0, value=2.5, key="natural_frequency_value", on_change=update_widget)
st.markdown(st.session_state.natural_frequency_display)

with st.container(border=True):
    st.subheader("Optimal Spring Rates")
    sr_col1, sr_col2 = st.columns(2)

    with sr_col1:
        st.markdown('''#### Front Spring Rate
        {} N/m'''.format(int(st.session_state.front_spring_rate)))

    with sr_col2:
        st.markdown('''#### Rear Spring Rate
        {} N/m'''.format(int(st.session_state.rear_spring_rate)))

st.divider() 

st.subheader('Wheel Rate')
wr_input_col1, wr_input_col2 = st.columns(2)

with wr_input_col1:
    st.number_input("Front Motion Ratio", min_value=0.0, value=0.5, step=0.01, key="front_mr", on_change=update_widget)

with wr_input_col2:
    st.number_input("Rear Motion Ratio", min_value=0.0, value=0.5, step=0.01, key="rear_mr", on_change=update_widget)

with st.container(border=True):
    st.subheader("Optimal Wheel Rates")
    wr_col1, wr_col2 = st.columns(2)
    with wr_col1:
        st.markdown('''#### Front Wheel Rate
            {} N/m'''.format(int(st.session_state.front_wheel_rate)))

    with wr_col2:
        st.markdown('''#### Rear Wheel Rate
            {} N/m'''.format(int(st.session_state.rear_wheel_rate)))
        
st.divider() 

st.subheader('Damper Settings')
st.slider("Select Bump Target (% of Critical Damping)", 20, 70, key="damp_target", on_change=update_widget)
st.markdown("This setting is suitable for **{}**".format(st.session_state.damping_display))

st.selectbox(
    "Bump:Rebound Ratio",
    ("2:1", "3:1"), index=1, key="br_ratio", on_change=update_widget
)
st.markdown(st.session_state.br_ratio_text)

with st.container(border=True):
    st.subheader("Optimal Bump/Rebound")
    
    st.subheader("Slow")
    damp_col1, damp_col2 = st.columns(2)
    with damp_col1:
        st.markdown('''##### Front Bump
            {} Ns/m'''.format(int(st.session_state.front_bump)))
        st.markdown('''##### Front Rebound
            {} Ns/m'''.format(int(st.session_state.front_bump * st.session_state.rebound_mult)))

    with damp_col2:
        st.markdown('''##### Rear Bump
            {} Ns/m'''.format(int(st.session_state.rear_bump)))
        st.markdown('''##### Rear Rebound
            {} Ns/m'''.format(int(st.session_state.rear_bump * st.session_state.rebound_mult)))

    st.subheader("Fast")
    damp_fast_col1, damp_fast_col2 = st.columns(2)
    with damp_fast_col1:
        st.markdown('''##### Front Bump
            {} Ns/m'''.format(int(st.session_state.front_bump / 2)))
        st.markdown('''##### Front Rebound
            {} Ns/m'''.format(int(st.session_state.front_bump * st.session_state.rebound_mult / 2)))

    with damp_fast_col2:
        st.markdown('''##### Rear Bump
            {} Ns/m'''.format(int(st.session_state.rear_bump / 2)))
        st.markdown('''##### Rear Rebound
            {} Ns/m'''.format(int(st.session_state.rear_bump * st.session_state.rebound_mult / 2)))
st.divider() 

st.markdown('''
#### References

1. [Spring Rates and Suspension Frequencies - Plus Frequency Calculator!](https://www.drtuned.com/tech-ramblings/2017/10/2/spring-rates-suspension-frequencies)
2. [Critical Damping Calculator](https://www.omnicalculator.com/physics/critical-damping)
3. [Optimal Damping](https://www.eng-tips.com/threads/optimal-damping.136068/)
4. [A Survey of Guidelines for Specifying Dampers](https://www.eng-tips.com/threads/a-survey-of-guidelines-for-specifying-dampers.471668)
5. [Dampers Part 5: Critical Damping](https://www.racecompengineering.com/blogs/the-apex-files/dampers-part-5-critical-damping)
''')
