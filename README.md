<p align="center">
  <img src="client/src/assets/eye_icon.png" alt="Logo" width="150" height="150">
</p>

# Horus

**Horus** is a _network scanner_ designed to identify devices on a network and detect vulnerabilities, developed for the NOI Hackathon SFSCON Edition 2024.  
It’s perfect for users who prefer a graphical interface over command-line tools and want an easy way to check for vulnerabilities in their networked devices. With Horus, results from command-line tools like nmap are presented in a user-friendly, clear and easy-to-understand dashboard.

Key features include "Find My Device," which helps users identify the device associated with a specific IP address, and a chatbot that can explain the services running on the network and any vulnerabilities that are detected.

Horus is also incredibly easy to install and use, making it a great choice for both novice and experienced users who want to quickly assess the security of their network.

The name "Horus" was chosen for this network scanner because it is inspired by the ancient Egyptian god Horus, who was often depicted as a protector and guardian. Just as Horus watched over and safeguarded Egypt, this tool is designed to safeguard your network by detecting and addressing vulnerabilities, ensuring your devices are protected from potential threats.

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