import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const AuthCallback = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get("token");

        if (token) {
            localStorage.setItem("token", token);
            navigate("/profile");
        } else {
            navigate("/login");
        }
    }, [navigate]);

    return <p>Logging you in...</p>;
};

export default AuthCallback;
