import React, { useEffect } from 'react';

const App = () => {
  const streamUrl = 'http://192.168.68.104:8080/stream'; // MJPEG Stream URL
  const wsUrl = 'ws://192.168.68.104:8081'; // WebSocket server URL

  useEffect(() => {
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      console.log('WebSocket connected');
    };

    socket.onmessage = (event) => {
      console.log('Message from server:', event.data);
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    const handleKeyPress = (event) => {
      const commandMap = {
        w: 'THRUSTER FORWARD',
        a: 'THRUSTER LEFT',
        s: 'THURSTER BACKWARD',
        d: 'THRUSTER RIGHT',
        ' ': 'THRUSTER STOP',
        ArrowUp: 'CAM U',
        ArrowDown: 'CAM D',
        ArrowLeft: 'CAM L',
        ArrowRight: 'CAM R',
        q: 'QUIT',
      };

      const command = commandMap[event.key];
      if (command && socket.readyState === WebSocket.OPEN) {
        socket.send(command);
        console.log(`Sent command: ${command}`);
      }
    };

    window.addEventListener('keydown', handleKeyPress);

    return () => {
      socket.close();
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, []);

  const topHeaderStyle = {
    display: 'flex',
    justifyContent: 'space-evenly',
    alignItems: 'center',
    padding: '30px',
    backgroundColor: '#333',
    color: '#fff',
    borderBottom: '3px solid #ccc',
  };

  const controlBoxStyle = {
    textAlign: 'center',
    padding: '25px',
    border: '2px solid #ddd',
    borderRadius: '15px',
    boxShadow: '0 6px 8px rgba(0, 0, 0, 0.1)',
    width: '280px',
    backgroundColor: '#444',
    color: '#fff',
  };

  const titleStyle = {
    fontSize: '24px',
    fontWeight: 'bold',
    marginBottom: '15px',
    color: '#fff',
  };

  const movementStyle = {
    fontSize: '20px',
    color: '#ddd',
    margin: '8px 0',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  };

  const symbolStyle = {
    fontSize: '26px',
    fontWeight: 'bold',
    marginRight: '10px',
    color: '#fff',
  };

  const mainContentStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: '50px',
    padding: '20px',
  };

  const cameraBoxStyle = {
    width: '1320px', // Increased width
    height: '740px', // Increased height
    border: '2px solid #ccc',
    borderRadius: '15px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: '18px',
    backgroundColor: '#f7f9fc',
    boxShadow: '0 6px 10px rgba(0, 0, 0, 0.1)',
  };

  const imgStyle = {
    width: '100%',
    height: '100%',
    borderRadius: '15px',
    objectFit: 'cover',
  };

  const projectTitleStyle = {
    marginTop: '20px',
    fontSize: '64px', // Large font size
    fontWeight: 'bold',
    color: '#fff', // Text color for better contrast
    textAlign: 'center',
    backgroundColor: '#333', // Dark background
    padding: '30px 0', // Padding for height
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '15px', // Spacing between title and icon
    width: '100%', // Full width
  };

  const iconStyle = {
    fontSize: '48px', // Icon size
  };

  return (
    <div>
      {/* Header Section */}
      <div style={topHeaderStyle}>
        <div style={controlBoxStyle}>
          <p style={titleStyle}>Camera Movement</p>
          <p style={movementStyle}>
            <span style={symbolStyle}>W</span> Forward
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>A</span> Left
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>S</span> Backward
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>D</span> Right
          </p>
        </div>
        <div style={controlBoxStyle}>
          <p style={titleStyle}>Boat Movement</p>
          <p style={movementStyle}>
            <span style={symbolStyle}>↑</span> Thruster Forward
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>←</span> Rotate Left
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>→</span> Rotate Right
          </p>
          <p style={movementStyle}>
            <span style={symbolStyle}>↓</span> Thruster Backward
          </p>
        </div>
      </div>

      {/* Main Content Section */}
      <div style={mainContentStyle}>
        <div style={cameraBoxStyle}>
          <img src={streamUrl} alt="Camera View" style={imgStyle} />
        </div>
      </div>

      {/* Bottom Section */}
      <div style={projectTitleStyle}>
        <span>Inspectle</span>
        <span style={iconStyle}>🐢</span>
      </div>
    </div>
  );
};

export default App;
