<p align="center">
  <img src="client/src/assets/eye_icon.png" alt="Logo" width="150" height="150">
</p>

# Horus

Horus is a network scanner that identifies devices on a network and checks for vulnerabilities, made for NOI Hackathon SFSCON Edition 2024.  
The end user should be a normal user that wants to check the devices on his network for vulnerabilities and can see cli tools results such as nmap displayed in a user-friendly interface.   
Other important functions are "Find my device", which can help the user to understand which devise has a certain IP and a chatbot who can help the user to understand the vulnerabilities found.

## Features

- Scan the network for devices
- Check devices for vulnerabilities
- Display scan results in a web interface
- Can help you find devices on network
- Offer a basic chatbot to help you with vulnerabilities explanation
- Show the SSID of the connected Wi-Fi network

## Technologies Used

- **Backend**: Python, FastAPI
- **Frontend**: Vue.js
- **Scripting**: Nmap, Vulscan

## Roadmap

- [x] Set up backend server with FastAPI
- [x] Set up frontend client with Vue.js
- [x] Implement basic network scanning functionality
- [x] Integrate Nmap and Vulscan for vulnerability checks
- [x] Display scan results in web interface
- [x] Show SSID of connected Wi-Fi network
- [ ] Create basic chatbot for vulnerability explanations
- [ ] Improve UI/UX of the web interface
- [ ] Implement real-time updates for scan results

## Setup

### Backend

1. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

2. **Run the server**:
    ```sh
    uvicorn server.main:app --reload
    ```

### Frontend

1. **Navigate to the client directory**:
    ```sh
    cd client
    ```

2. **Install dependencies**:
    ```sh
    npm install
    ```

3. **Run the development server**:
    ```sh
    npm run serve
    ```

## Endpoints
There is a swagger interface at `http://server.domain/docs` to test the endpoints made with FastAPI.
- **Start Scan**: `POST /start`
- **Get Scan Results**: `GET /scan`
- **Get SSID**: `GET /ssid`
- **Check if Device is Online**: `GET /isonline/{ip}`

## Usage

1. Start the backend server.
2. Start the frontend development server.
3. Open the web interface in your browser.
4. Use the interface to start a network scan and view the results.

## License

This project is licensed under the GNU-GPLv3 License - see the [LICENSE](LICENSE) file for details.