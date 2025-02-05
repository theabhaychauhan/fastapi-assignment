import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const ProfileRedirect = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const token = params.get("token");

        if (token) {
            localStorage.setItem("token", token);
            navigate("/profile");
        }
    }, [navigate]);

    return <div>Loading...</div>;
};

export default ProfileRedirect;
