import os
import time
import tempfile
import requests
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
from datetime import datetime
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Finance Assistant( AI Portfolio Manager )",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint URLs
API_BASE_URL = f"http://localhost:{os.getenv('FASTAPI_PORT', '8000')}"
MARKET_BRIEF_URL = f"{API_BASE_URL}/market-brief"
QUERY_URL = f"{API_BASE_URL}/query"
VOICE_QUERY_URL = f"{API_BASE_URL}/voice-query"

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None
# Add initialization for selected_device_index
if 'selected_device_index' not in st.session_state:
    st.session_state.selected_device_index = None

# Function to list available audio input devices
def list_audio_devices():
    p = pyaudio.PyAudio()
    devices = []
    try:
        info = p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(0, num_devices):
            device_info = p.get_device_info_by_host_api_device_index(0, i)
            if device_info.get('maxInputChannels') > 0: # Check if it's an input device
                devices.append({'index': i, 'name': device_info.get('name')})
    except Exception as e:
        st.error(f"Error listing audio devices: {e}")
    finally:
        p.terminate()
    return devices

# Function to record audio
def record_audio(duration=5, sample_rate=16000, input_device_index=None):
    """Record audio from microphone.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Audio sample rate
        input_device_index: Index of the input device to use (optional)
        
    Returns:
        Path to recorded audio file
    """
    # Audio recording parameters
    chunk = 1024
    audio_format = pyaudio.paInt16
    channels = 1
    
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    
    # Open stream
    try:
        stream = p.open(
            format=audio_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk,
            input_device_index=input_device_index # Use the provided index
        )
    except Exception as e:
        st.error(f"Error opening audio stream. Check input device index and permissions: {e}")
        p.terminate()
        return None # Return None if stream cannot be opened

    # Record audio
    st.info(f"Recording for {duration} seconds...")
    frames = []
    # Add a check to ensure stream is open before reading
    if stream:
        for i in range(0, int(sample_rate / chunk * duration)):
            try:
                data = stream.read(chunk)
                frames.append(data)
            except IOError as e:
                st.error(f"IOError during recording: {e}. This might indicate a problem with the audio device.")
                break # Exit loop on error

    # Stop and close the stream
    if stream:
        stream.stop_stream()
        stream.close()
    p.terminate()
    
    # Save to temporary file only if frames were captured
    if frames:
        temp_dir = tempfile.gettempdir()
        audio_file = os.path.join(temp_dir, f"voice_query_{int(time.time())}.wav")
        
        # Write to WAV file
        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return audio_file
    else:
        st.warning("No audio frames were recorded.")
        return None # Return None if no frames were recorded

# Function to get market brief
def get_market_brief(voice_output=True):
    """Get morning market brief from API.
    
    Args:
        voice_output: Whether to include voice output
        
    Returns:
        Market brief response
    """
    try:
        response = requests.post(f"{MARKET_BRIEF_URL}?voice_output={str(voice_output).lower()}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error getting market brief: {e}")
        return None

# Function to submit text query
def submit_text_query(query, voice_output=True):
    """Submit text query to API.
    
    Args:
        query: Text query
        voice_output: Whether to include voice output
        
    Returns:
        Query response
    """
    try:
        response = requests.post(
            f"{QUERY_URL}?voice_output={str(voice_output).lower()}",
            json={"query": query}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error submitting query: {e}")
        return None

# Function to submit voice query
def submit_voice_query(audio_file, voice_output=True):
    """Submit voice query to API.
    
    Args:
        audio_file: Path to audio file
        voice_output: Whether to include voice output
        
    Returns:
        Query response
    """
    try:
        with open(audio_file, 'rb') as f:
            files = {'file': (os.path.basename(audio_file), f, 'audio/wav')}
            response = requests.post(
                f"{VOICE_QUERY_URL}?voice_output={str(voice_output).lower()}",
                files=files
            )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error submitting voice query: {e}")
        return None

# Function to play audio
def play_audio(audio_url):
    """Play audio from URL.
    
    Args:
        audio_url: URL to audio file
    """
    try:
        audio_response = requests.get(f"{API_BASE_URL}{audio_url}")
        audio_response.raise_for_status()
        
        st.audio(audio_response.content, format="audio/mp3")
    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Function to display portfolio data
def display_portfolio_data(portfolio_data):
    """Display portfolio data visualization.
    
    Args:
        portfolio_data: Portfolio data dictionary
    """
    # Create a pie chart of holdings
    if portfolio_data and 'holdings' in portfolio_data:
        holdings = portfolio_data['holdings']
        
        # Extract data for pie chart
        labels = [h.get('name', h.get('symbol', 'Unknown')) for h in holdings]
        values = [h.get('value', 0) for h in holdings]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Asia Tech Portfolio Allocation')
        
        # Display in Streamlit
        st.pyplot(fig)
        
        # Display allocation metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Asia Tech Allocation", 
                f"{portfolio_data.get('asia_tech_allocation_pct', 0):.1f}%",
                f"{portfolio_data.get('allocation_change_pct', 0):+.1f}%"
            )
        with col2:
            st.metric(
                "Total AUM", 
                f"${portfolio_data.get('total_aum', 0):,.0f}"
            )
        with col3:
            st.metric(
                "Asia Tech Value", 
                f"${portfolio_data.get('asia_tech_allocation', 0):,.0f}"
            )
        
        # Display holdings table
        st.subheader("Holdings Detail")
        holdings_df = pd.DataFrame(holdings)
        if not holdings_df.empty:
            # Format columns
            if 'value' in holdings_df.columns:
                holdings_df['value'] = holdings_df['value'].apply(lambda x: f"${x:,.0f}")
            if 'allocation_pct' in holdings_df.columns:
                holdings_df['allocation_pct'] = holdings_df['allocation_pct'].apply(lambda x: f"{x:.1f}%")
            if 'daily_change_pct' in holdings_df.columns:
                holdings_df['daily_change_pct'] = holdings_df['daily_change_pct'].apply(lambda x: f"{x:+.2f}%")
            
            st.dataframe(holdings_df)

# Function to display stock performance
def display_stock_performance(performance_data):
    """Display stock performance visualization.
    
    Args:
        performance_data: Stock performance data dictionary
    """
    if performance_data:
        st.subheader("Stock Performance")
        st.write(performance_data.get('performance_summary', 'No performance data available'))
        
        # Display top and bottom performers
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Performers")
            top_performers = performance_data.get('top_performers', [])
            if top_performers:
                for performer in top_performers:
                    st.metric(
                        performer.get('name', performer.get('symbol', 'Unknown')),
                        f"{performer.get('change_pct', 0):+.2f}%"
                    )
        
        with col2:
            st.subheader("Bottom Performers")
            bottom_performers = performance_data.get('bottom_performers', [])
            if bottom_performers:
                for performer in bottom_performers:
                    st.metric(
                        performer.get('name', performer.get('symbol', 'Unknown')),
                        f"{performer.get('change_pct', 0):+.2f}%"
                    )

# Function to display earnings surprises
def display_earnings_surprises(earnings_data):
    """Display earnings surprises visualization.
    
    Args:
        earnings_data: Earnings data dictionary
    """
    if earnings_data:
        st.subheader("Earnings Surprises")
        st.write(earnings_data.get('surprise_summary', 'No earnings data available'))
        
        # Display positive and negative surprises
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Positive Surprises")
            positive_surprises = earnings_data.get('positive_surprises', [])
            if positive_surprises:
                for surprise in positive_surprises:
                    st.metric(
                        surprise.get('name', surprise.get('symbol', 'Unknown')),
                        f"+{surprise.get('surprise_pct', 0):.2f}%",
                        delta_color="normal"
                    )
        
        with col2:
            st.subheader("Negative Surprises")
            negative_surprises = earnings_data.get('negative_surprises', [])
            if negative_surprises:
                for surprise in negative_surprises:
                    st.metric(
                        surprise.get('name', surprise.get('symbol', 'Unknown')),
                        f"{surprise.get('surprise_pct', 0):.2f}%",
                        delta_color="inverse"
                    )

# Function to display risk analysis
def display_risk_analysis(risk_data):
    """Display risk analysis visualization.
    
    Args:
        risk_data: Risk analysis data dictionary
    """
    if risk_data:
        st.subheader("Risk Analysis")
        st.write(risk_data.get('risk_summary', 'No risk analysis available'))
        
        # Display risk score gauge
        risk_score = risk_data.get('risk_score', 5)
        
        # Create a gauge chart for risk score
        fig, ax = plt.subplots(figsize=(10, 2))
        
        # Define the gauge range and colors
        gauge_range = np.linspace(0, 10, 100)
        colors = plt.cm.RdYlGn_r(gauge_range / 10)
        
        # Create the gauge
        ax.barh(0, 10, height=0.6, color='lightgray')
        ax.barh(0, risk_score, height=0.6, color=plt.cm.RdYlGn_r(risk_score / 10))
        
        # Add the pointer
        ax.plot([risk_score, risk_score], [-0.3, 0.3], color='black', linewidth=2)
        ax.plot([risk_score], [0], marker='o', markersize=10, color='black')
        
        # Set the limits and remove axes
        ax.set_xlim(0, 10)
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.set_xticks([0, 2.5, 5, 7.5, 10])
        ax.set_xticklabels(['Low', '', 'Medium', '', 'High'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Add title and risk score
        plt.title(f"Risk Score: {risk_score:.1f}/10 - {risk_data.get('risk_level', 'Medium').title()} Risk")
        
        # Display in Streamlit
        st.pyplot(fig)
        
        # Display risk factors
        st.subheader("Risk Factors")
        risk_factors = risk_data.get('risk_factors', [])
        if risk_factors:
            for factor in risk_factors:
                st.write(f"• {factor}")

# Main app layout
st.title("Finance Assistant(AI Portfolio Manager) 💹")
st.write("A multi-agent finance assistant that delivers spoken market briefs")

# Sidebar
st.sidebar.title("Options")
voice_output = st.sidebar.checkbox("Enable Voice Output", value=True)


st.sidebar.write("Note: Please select the appropriate microphone.")# Display available audio devices in the sidebar
st.sidebar.header("Audio Input Devices")
available_devices = list_audio_devices() # This function tries to find devices

if available_devices: # This block runs ONLY if devices are found
    st.sidebar.write("Select your microphone:")
    
    # Find the current index based on session state, default to 0 if none selected
    current_index = 0
    if st.session_state.selected_device_index is not None:
        for i, device in enumerate(available_devices):
            if device['index'] == st.session_state.selected_device_index:
                current_index = i
                break

    # {{ edit_1 }}
    # Display the selectbox for choosing the device
    device_names = [f"Index {d['index']}: {d['name']}" for d in available_devices]
    selected_device_name = st.sidebar.selectbox(
        "Choose Device",
        device_names,
        index=current_index, # Set default based on session state
        key="audio_device_selectbox" # Add a key for the selectbox
    )

    # Find the index of the selected device and store it in session state
    for device in available_devices:
        if f"Index {device['index']}: {device['name']}" == selected_device_name:
            st.session_state.selected_device_index = device['index'] # Store in session state
            break

    st.sidebar.caption(f"Selected device index: {st.session_state.selected_device_index}")

    # REMOVE the button from here - it belongs in tab2
    # if st.button("🎤 Record", key="record_buttons"):
    #     # Access selected_device_index from session state
    #     if st.session_state.selected_device_index is not None: # Only record if a device is selected
    #         with st.spinner("Recording..."):
    #             # Pass the selected device index from session state to record_audio
    #             audio_file = record_audio(duration=5, input_device_index=st.session_state.selected_device_index)
    #             st.session_state.audio_file = audio_file
    #             if audio_file:
    #                 st.success("Recording complete!")
    #             else:
    #                 st.error("Recording failed.")
    #     else:
    #         st.warning("Please select an audio input device in the sidebar.")
    # {{ end_edit_1 }}

else: # This block runs if NO devices are found
    st.sidebar.warning("No audio input devices found. Please check your microphone setup.")
    # Ensure selected_device_index is None if no devices are found
    st.session_state.selected_device_index = None


# Tabs for different functions
tab1,tab2,tab3 = st.tabs(["Morning Market Brief", "Ask a Question", "Investor Story"])

# Morning Market Brief tab
with tab1:
    st.header("Morning Market Brief")
    st.write("Get your daily market brief focusing on Asia stocks")
    
    # Button to get market brief
    if st.button("Generate Market Brief", key="generate_brief"):
        with st.spinner("Generating market brief..."):
            brief_response = get_market_brief(voice_output)
            
            if brief_response:
                # Display the brief
                st.subheader("Market Brief")
                st.write(brief_response['brief'])
                
                # Play audio if available
                if voice_output and 'audio_url' in brief_response and brief_response['audio_url']:
                    st.subheader("Audio Brief")
                    play_audio(brief_response['audio_url'])
                
                # Display visualizations
                st.header("Portfolio Analysis")
                
                # Create tabs for different visualizations
                viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs(["Portfolio", "Performance", "Earnings", "Risk"])
                
                with viz_tab1:
                    display_portfolio_data(brief_response['portfolio_data'])
                
                with viz_tab2:
                    display_stock_performance(brief_response['stock_performance'])
                
                with viz_tab3:
                    display_earnings_surprises(brief_response['earnings_analysis'])
                
                with viz_tab4:
                    display_risk_analysis(brief_response['risk_analysis'])
                
                # Add to history
                st.session_state.history.append({
                    'type': 'market_brief',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'brief': brief_response['brief'],
                    'audio_url': brief_response.get('audio_url')
                })

# Ask a Question tab
with tab2:
    st.header("Ask a Question")
    st.write("Ask specific questions about your Asia stock exposure, general finance and much more")

    # Text input for questions
    query = st.text_input("Enter your question", placeholder="What's our risk exposure in Asia tech stocks today?")

    # {{ edit_1 }}
    # Voice input section - improved layout
    st.subheader("Voice Input") # Use a subheader for clarity
    st.write("Click the button below to record your question:") # Add a clear instruction

    # Place the Record button below the instruction
    # The button will take up the default width unless placed in columns
    if st.button("🎤 Record", key="record_button_tab2_improved"): # Changed key again for uniqueness
        # Access selected_device_index from session state
        if st.session_state.selected_device_index is not None: # Only record if a device is selected
            with st.spinner("Recording..."):
                # Pass the selected device index from session state to record_audio
                audio_file = record_audio(duration=5, input_device_index=st.session_state.selected_device_index)
                st.session_state.audio_file = audio_file
                if audio_file:
                    st.success("Recording complete!")
                else:
                    st.error("Recording failed.")
        else:
            # This warning will now appear in the main tab if no device was selected in the sidebar
            st.warning("Please select an audio input device in the sidebar.")

    # Remove the old column layout for voice input
    # col1, col2 = st.columns([3, 1])
    # with col1:
    #     st.write("Or use voice input:")
    # with col2:
    #     if st.button("🎤 Record", key="record_button_tab2"):
    #         # ... recording logic ...
    #         pass # Remove this old button logic

    # {{ end_edit_1 }}

    # Submit buttons
    # Keep submit buttons in columns below the voice input section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Text Question", key="submit_text") and query:
            with st.spinner("Processing your question..."):
                response = submit_text_query(query, voice_output)
                
                if response:
                    # Display the answer
                    st.subheader("Answer")
                    st.write(response['answer'])
                    
                    # Display confidence
                    st.progress(min(response['confidence'] / 100, 1.0))
                    st.caption(f"Confidence: {response['confidence']:.1f}%")
                    
                    # Play audio if available
                    if voice_output and 'audio_url' in response and response['audio_url']:
                        st.subheader("Audio Response")
                        play_audio(response['audio_url'])
                    
                    # Display sources
                    if 'sources' in response and response['sources']:
                        st.subheader("Sources")
                        for i, source in enumerate(response['sources']):
                            with st.expander(f"Source {i+1} - Confidence: {source['confidence']:.1f}%"):
                                st.write(source['content'])
                                st.caption(f"Type: {source['metadata'].get('type', 'Unknown')}")
                    
                    # Add to history
                    st.session_state.history.append({
                        'type': 'text_query',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'query': query,
                        'answer': response['answer'],
                        'audio_url': response.get('audio_url')
                    })
    
    with col2:
        if st.button("Submit Voice Question", key="submit_voice") and st.session_state.audio_file:
            with st.spinner("Processing your voice question..."):
                response = submit_voice_query(st.session_state.audio_file, voice_output)
                
                if response:
                    # Display transcription
                    st.subheader("Transcription")
                    st.write(response['transcription'])
                    
                    # Display the answer
                    st.subheader("Answer")
                    st.write(response['answer'])
                    
                    # Display confidence
                    st.progress(min(response['confidence'] / 100, 1.0))
                    st.caption(f"Confidence: {response['confidence']:.1f}%")
                    
                    # Play audio if available
                    if voice_output and 'audio_url' in response and response['audio_url']:
                        st.subheader("Audio Response")
                        play_audio(response['audio_url'])
                    
                    # Display sources
                    if 'sources' in response and response['sources']:
                        st.subheader("Sources")
                        for i, source in enumerate(response['sources']):
                            with st.expander(f"Source {i+1} - Confidence: {source['confidence']:.1f}%"):
                                st.write(source['content'])
                                st.caption(f"Type: {source['metadata'].get('type', 'Unknown')}")
                    
                    # Add to history
                    st.session_state.history.append({
                        'type': 'voice_query',
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'transcription': response['transcription'],
                        'answer': response['answer'],
                        'audio_url': response.get('audio_url')
                    })


# Investor Story tab
with tab3:
    st.header("Meet Ms. Anya Sharma")
    st.write("A seasoned investor with a keen eye on emerging markets, particularly the Asia tech sector.")

    st.subheader("Anya's Portfolio Snapshot")

    # Hardcoded portfolio data from api_agent
    anya_portfolio_data = {
        'total_aum': 1000000,
        'asia_tech_allocation': 220000,
        'previous_asia_tech_allocation': 180000,
        'holdings': [
            {'symbol': 'TSM', 'name': 'Taiwan Semiconductor', 'value': 50000},
            {'symbol': 'BABA', 'name': 'Alibaba', 'value': 40000},
            {'symbol': '005930.KS', 'name': 'Samsung Electronics', 'value': 35000},
            {'symbol': 'BIDU', 'name': 'Baidu', 'value': 30000},
            {'symbol': 'JD', 'name': 'JD.com', 'value': 25000},
            {'symbol': 'PDD', 'name': 'PDD Holdings', 'value': 40000}
        ]
    }

    # Calculate metrics for display
    total_aum = anya_portfolio_data.get('total_aum', 0)
    current_allocation = anya_portfolio_data.get('asia_tech_allocation', 0)
    previous_allocation = anya_portfolio_data.get('previous_asia_tech_allocation', 0)

    current_allocation_pct = (current_allocation / total_aum) * 100 if total_aum else 0
    previous_allocation_pct = (previous_allocation / total_aum) * 100 if total_aum else 0
    allocation_change_pct = current_allocation_pct - previous_allocation_pct

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Asia Tech Allocation",
            f"{current_allocation_pct:.1f}%",
            f"{allocation_change_pct:+.1f}%"
        )
    with col2:
        st.metric(
            "Total AUM",
            f"${total_aum:,.0f}"
        )
    with col3:
        st.metric(
            "Asia Tech Value",
            f"${current_allocation:,.0f}"
        )

    st.subheader("Holdings Detail")
    holdings_df = pd.DataFrame(anya_portfolio_data['holdings'])

    if not holdings_df.empty:
        # Calculate allocation percentage for each holding
        holdings_df['allocation_pct'] = (holdings_df['value'] / current_allocation) * 100 if current_allocation else 0

        # Format columns
        if 'value' in holdings_df.columns:
            holdings_df['value'] = holdings_df['value'].apply(lambda x: f"${x:,.0f}")
        if 'allocation_pct' in holdings_df.columns:
            holdings_df['allocation_pct'] = holdings_df['allocation_pct'].apply(lambda x: f"{x:.1f}%")

        # Select and reorder columns for display
        display_cols = ['symbol', 'name', 'value', 'allocation_pct']
        holdings_df = holdings_df[display_cols]

        st.dataframe(holdings_df, hide_index=True)

    st.write("""
    Anya's strategic move to increase her exposure reflects her strong conviction in the sector's future performance.
    She actively monitors these positions, relying on timely data to inform her next strategic decisions in the fast-paced Asia tech landscape.
    """)


# Display interaction history in sidebar
st.sidebar.header("Interaction History")
for i, interaction in enumerate(reversed(st.session_state.history)):
    with st.sidebar.expander(f"{interaction['timestamp']} - {interaction['type']}"):
        if interaction['type'] == 'market_brief':
            st.write("Market Brief:")
            st.write(interaction['brief'])
        elif interaction['type'] == 'text_query':
            st.write(f"Question: {interaction['query']}")
            st.write(f"Answer: {interaction['answer']}")
        elif interaction['type'] == 'voice_query':
            st.write(f"Question: {interaction['transcription']}")
            st.write(f"Answer: {interaction['answer']}")
        
        if 'audio_url' in interaction and interaction['audio_url']:
            if st.button("Play Audio", key=f"play_{i}"):
                play_audio(interaction['audio_url'])