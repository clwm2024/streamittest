import streamlit as st

# Titel der Anwendung
st.title("Hallo, Streamlit!")

# Einfacher Text
st.write("Das ist eine einfache Streamlit-Anwendung.")

# Eingabefeld für Text
name = st.text_input("Gib deinen Namen ein")

# Button
if st.button("Senden"):
    st.write(f"Hallo, {name}!")

# Slider
age = st.slider("Wähle dein Alter", 0, 100, 25)
st.write(f"Dein Alter ist {age}")
