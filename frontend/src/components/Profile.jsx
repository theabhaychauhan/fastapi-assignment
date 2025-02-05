import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Profile = () => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [updatedUser, setUpdatedUser] = useState({
        full_name: '',
        bio: '',
        phone: '',
        email: '',
        photo: null,
    });
    const [coins, setCoins] = useState([]);
    const [selectedCoin, setSelectedCoin] = useState('');
    const [coinDetails, setCoinDetails] = useState(null);
    const [weatherData, setWeatherData] = useState(null);

    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    useEffect(() => {
        if (!token) {
            navigate('/login');
            return;
        }

        const fetchUserProfile = async () => {
            try {
                const response = await fetch("http://localhost:8000/auth/profile", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch user details");
                }

                const userData = await response.json();
                setUser(userData);
                setUpdatedUser({
                    full_name: userData.full_name,
                    bio: userData.bio,
                    phone: userData.phone,
                    email: userData.email,
                });
            } catch (err) {
                setError(err.message);
            }
        };

        fetchUserProfile();
    }, [token, navigate]);

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate('/login');
    };

    const handleChange = (e) => {
        if (e.target.name === "photo") {
            setUpdatedUser({
                ...updatedUser,
                photo: e.target.files[0],
            });
        } else {
            setUpdatedUser({
                ...updatedUser,
                [e.target.name]: e.target.value,
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/auth/profile/update", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(updatedUser),
            });

            if (!response.ok) {
                throw new Error("Failed to update user details");
            }

            const updatedUserData = await response.json();
            setUser(updatedUserData);
            setEditMode(false);
        } catch (err) {
            setError(err.message);
        }
    };

    const handlePhotoUpload = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("photo", updatedUser.photo);

        try {
            const response = await fetch("http://localhost:8000/auth/profile/upload-photo", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Failed to upload photo");
            }

            const result = await response.json();
            console.log(result.message);
        } catch (err) {
            setError(err.message);
        }
    };

    const fetchAvailableCoins = async () => {
        try {
            const response = await fetch("http://localhost:8000/binance/data", {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                },
            });
            if (!response.ok) {
                throw new Error("Failed to fetch coin data");
            }
            const data = await response.json();
            setCoins(data);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleSelectCoin = async (coinSymbol) => {
        setSelectedCoin(coinSymbol);

        if (coinSymbol) {
            try {
                const response = await fetch(`http://localhost:8000/coin-prices/${coinSymbol}`);
                
                if (!response.ok) {
                    throw new Error("Failed to fetch coin prices from DB");
                }

                const data = await response.json();
                console.log("Received data:", data);

                if (data.error) {
                    setError(data.error);
                } else {
                    setCoinDetails(data);
                }
            } catch (err) {
                console.error("Error fetching data:", err);
                setError(err.message);
            }
        } else {
            setCoinDetails(null);
        }
    };

    const fetchWeatherData = async () => {
        try {
            const response = await fetch("http://localhost:8000/weather/data");
            const data = await response.json();
            if (data.error) {
                setError(data.error);
            } else {
                setWeatherData(data);
            }
        } catch (err) {
            setError("Failed to fetch weather data");
        }
    };

    const getChartData = () => {
        if (!coinDetails) return {};

        const labels = coinDetails.map((data) => new Date(data.timestamp).toLocaleString());
        const dataPoints = coinDetails.map((data) => data.price);

        const minValue = Math.min(...dataPoints) * 0.95;
        const maxValue = Math.max(...dataPoints) * 1.05;

        return {
            labels,
            datasets: [
                {
                    label: `${selectedCoin} Price`,
                    data: dataPoints,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderWidth: 1,
                    barThickness: 10,
                },
            ],
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        min: minValue,
                        max: maxValue,
                    },
                },
            },
        };
    };


    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div style={{ maxWidth: "800px", margin: "auto", padding: "20px" }}>
            {user ? (
                <>
                    <h2>Welcome, {user.full_name}!</h2>
                    <p>Email: {user.email}</p>
                    <p>Bio: {user.bio}</p>
                    <p>Phone: {user.phone}</p>
                    {user.photo && <img src={user.photo} alt="Profile" style={{ width: '100%', borderRadius: '8px' }} />}
                    <button onClick={handleLogout}>Logout</button>

                    <button onClick={() => setEditMode(!editMode)}>
                        {editMode ? "Cancel" : "Edit Profile"}
                    </button>

                    <button onClick={() => navigate("/reset-password")}>
                        Reset Password
                    </button>

                    {editMode && (
                        <form onSubmit={handleSubmit}>
                            <input
                                type="text"
                                name="full_name"
                                value={updatedUser.full_name}
                                onChange={handleChange}
                                placeholder="Full Name"
                            />
                            <br />
                            <input
                                type="text"
                                name="bio"
                                value={updatedUser.bio}
                                onChange={handleChange}
                                placeholder="Bio"
                            />
                            <br />
                            <input
                                type="text"
                                name="phone"
                                value={updatedUser.phone}
                                onChange={handleChange}
                                placeholder="Phone"
                            />
                            <br />
                            <input
                                type="email"
                                name="email"
                                value={updatedUser.email}
                                onChange={handleChange}
                                placeholder="Email"
                            />
                            <br />
                            <input
                                type="file"
                                name="photo"
                                accept="image/*"
                                onChange={handleChange}
                            />
                            <br />
                            <button type="submit">Save Changes</button>
                        </form>
                    )}

                    {updatedUser.photo && (
                        <button onClick={handlePhotoUpload}>
                            Upload Photo
                        </button>
                    )}

                    <button onClick={fetchAvailableCoins}>
                        Fetch Coins
                    </button>

                    {coins.length > 0 && (
                        <>
                            <h3>Available Coins:</h3>
                            <pre>{JSON.stringify(coins, null, 2)}</pre>

                            <h3>Select a Coin:</h3>
                            <select value={selectedCoin} onChange={(e) => handleSelectCoin(e.target.value)}>
                                <option value="">Select a coin</option>
                                {coins.map((coin) => (
                                    <option key={coin.symbol} value={coin.symbol}>
                                        {coin.symbol}
                                    </option>
                                ))}
                            </select>
                        </>
                    )}

                    {coinDetails && (
                        <div>
                            <h3>{selectedCoin} Historical Data:</h3>
                            <Bar data={getChartData()} options={{ responsive: true, maintainAspectRatio: false }} />
                        </div>
                    )}

                    <button onClick={fetchWeatherData}>
                        Fetch Weather Data
                    </button>

                    {weatherData && (
                        <div>
                            <h3>Weather Data:</h3>
                            <pre>{JSON.stringify(weatherData, null, 2)}</pre>
                        </div>
                    )}
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Profile;
