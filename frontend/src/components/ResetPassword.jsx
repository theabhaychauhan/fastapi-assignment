import { useState } from "react";

const ResetPassword = () => {
    const [newPassword, setNewPassword] = useState("");
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const token = localStorage.getItem("token");

    const handleChange = (e) => {
        setNewPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        try {
            const response = await fetch("http://localhost:8000/auth/profile/reset-password", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ new_password: newPassword }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Failed to reset password");
            }

            setSuccess("Password updated successfully!");
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
            <h2>Reset Password</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="password"
                    name="new_password"
                    value={newPassword}
                    onChange={handleChange}
                    placeholder="Enter new password"
                    required
                />
                <br />
                <button type="submit">Update Password</button>
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {success && <p style={{ color: "green" }}>{success}</p>}
        </div>
    );
};

export default ResetPassword;
