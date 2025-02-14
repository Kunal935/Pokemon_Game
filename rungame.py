import streamlit as st 
import pandas as pd 
import numpy as np 
from fuzzywuzzy import process 
import requests


# Function for gif call
def get_req(p):
    api = 'AIzaSyDd0Ni8PlCt9ob1mVJzHDhu2uU4_O3KY64' 
    url = f"https://tenor.googleapis.com/v2/search?q=Pokemon+{p}&key={api}&client_key=my_test_app&limit=8"

    try:
        r = requests.get(url)
        r.raise_for_status()  # Check for errors
        data = r.json()
        
        if 'results' in data and len(data['results']) > 0:
            # Filter the results to get the exact match for the Pokémon name
            for result in data['results']:
                if p.lower() == result.get('title', '').lower():  # Exact name match
                    return result['media_formats']['gif']['url']
            # If no exact match found, return the first gif as fallback
            return data['results'][0]['media_formats']['gif']['url']
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
    return None

# Function to perform comparison
def comp(p1, p2):
    win1, win2 = 0, 0
    
    # Convert to lowercase for fuzzy matching
    p1 = p1.lower()
    p2 = p2.lower()
    
    # Get the best match for each Pokémon name using extractOne
    if p1 in df['Name'].str.lower().values and p2 in df['Name'].str.lower().values:
        p1_name = p1
        p2_name = p2
        
    else :
        p1_match = process.extractOne(p1, df['Name'] , score_cutoff=50)
        p2_match = process.extractOne(p2, df['Name'], score_cutoff=50)
    
    # Check if both Pokémon names were matched
    if p1_match is None or p2_match is None:
        st.write('⚠︎ No Matches found ⚠︎')
        return
    
    # Extract the matched names (best matches)
    p1_name = p1_match[0]
    p2_name = p2_match[0]
    
    # Display the matched names
    name1 = get_req(p1_name)
    name2 = get_req(p2_name)
    
    st.markdown(f"""<h5>🔥Your First Pokemon {p1_name} : <img src = "{name1}" width = "50" /></h5>""", unsafe_allow_html=True)
    st.markdown(f"""<h5>🔥Your Second Pokemon {p2_name} : <img src = {name2} width = "50"/></h5>""", unsafe_allow_html=True)
    
    # Retrieve the stats for the matched Pokémon
    stat1 = for_comp[for_comp['Name'] == p1_name].iloc[0]
    stat2 = for_comp[for_comp['Name'] == p2_name].iloc[0]
    
    # Double the stats for Legendary Pokémon
    if stat1['Legendary']:
        stat1 = stat1 * 2
    if stat2['Legendary']:
        stat2 = stat2 * 2

    # Create a comparison table for stats
    pok_stat = pd.DataFrame({
        'Stat': ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
        p1_name: [stat1['HP'], stat1['Attack'], stat1['Defense'], stat1['Sp. Atk'], stat1['Sp. Def'], stat1['Speed']],
        p2_name: [stat2['HP'], stat2['Attack'], stat2['Defense'], stat2['Sp. Atk'], stat2['Sp. Def'], stat2['Speed']]
    })
    
    # Display the comparison table
    st.write(f"**Comparison between {p1_name} and {p2_name}:**")
    st.table(pok_stat)

    # Compare the stats one by one
    for stat in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']:
        if stat1[stat] > stat2[stat]:
            win1 += 1
        elif stat1[stat] < stat2[stat]:
            win2 += 1
    
    # Display the result of comparison
    if win1 > win2:
        st.markdown(f"""<h5>🏆{p1_name} wins with better stats🏆<img src = {name1} width = "60"/></h5>""", unsafe_allow_html=True)
    elif win2 > win1:
        st.markdown(f"""<h5>🏆{p2_name} wins with better stats🏆<img src = {name2} width = "60"/></h5>""", unsafe_allow_html=True)
    else:
        st.write(f"😕It's hard to decide who will win between {p1_name} and {p2_name}😕")


# Load the dataset
df = pd.read_csv('Pokemon.csv')

# Selecting relevant columns for comparison
for_comp = df[['Name', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation', 'Legendary']]

# Layout for displaying image and title
col1, col2 = st.columns([1, 5])

a = get_req('pokemon fighting new')
b = get_req('pikachu licking')
st.markdown(f"""<h2>  <img src = "{a}" width = "60"/>   COMPARE YOUR POKEMONS   <img src = "{b}" width = "60"/>
            </h2>""", unsafe_allow_html=True)

# Text input for Pokémon names
pok1 = st.text_input('First Pokemon Name')
pok2 = st.text_input('Second Pokemon Name')

# Button to compare Pokémon
click = st.button('Compare')


# Execute comparison when button is clicked
if click:
    comp(pok1, pok2)
