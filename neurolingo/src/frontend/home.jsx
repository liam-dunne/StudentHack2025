import React from 'react';
import "../styles/home.css";
import {useEffect, useState} from 'react';
import io from "socket.io-client";

const socket = io("http://127.0.0.1:5000");

function Home() {
    const [talking, setTalking] = useState(false);
    const [image, setImage] = useState("mic_off.png");
    
    useEffect(() => {
        socket.on("update", (data) => {
            console.log("Socket update received:", data);
            setTalking(data.talking); 
            if (!talking) {
                setImage("mic_off.png");
            }
            else {
                setImage("mic_on.png");
            }// Update state dynamically
        });
        
    }, [talking, setImage, setTalking]);

    async function startTranslating() {
        const apiUrl = "http://127.0.0.1:5000/api/translate";

        try {
            fetch(apiUrl, {
                method: 'POST',              
            });
        }
        catch (error) {
            alert(`Something went wrong: ${error.message}`);
        }
    }

    return (
        <div className="app">
            <div className="app-header">
                <h1>Welcome to NeuroLingo</h1>
            </div>
            <div className="app-body">
                <div className="avatar">
                    <img src="avatar.png" alt="Help" id="avatar"></img>
                </div>
                <div className="mic">
                    <img src={image} id="mic" className="mic-image"></img>
                </div>
                <div className="start-button">
                    <button onClick={startTranslating}>Start Translating</button>
                </div>
            </div>
        </div>
        
    );
}

export default Home;