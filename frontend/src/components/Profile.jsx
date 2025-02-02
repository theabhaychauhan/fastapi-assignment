import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);

    const navigate = useNavigate();
    const token = localStorage.getItem("token");

    useEffect(() => {
        if (!token) {
            navigate('/login'); // Redirect to login page if token is not available
            return;
        }

        const fetchUserProfile = async () => {
            try {
                const response = await fetch("http://localhost:8000/auth/profile", {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error("Failed to fetch user details");
                }

                const userData = await response.json();
                setUser(userData);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchUserProfile();
    }, [token, navigate]);

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate('/login'); // Redirect to login page after logout
    };

    if (error) {
        return <p style={{ color: "red" }}>{error}</p>;
    }

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
            {user ? (
                <>
                    <h2>Welcome, {user.full_name}!</h2>
                    <p>Email: {user.email}</p>
                    <button onClick={handleLogout}>Logout</button>
                </>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default Profile;
