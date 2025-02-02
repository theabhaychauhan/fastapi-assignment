import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
    const [formData, setFormData] = useState({
        full_name: "",
        email: "",
        password: "",
    });

    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);

        try {
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!response.ok) {
                throw new Error("Registration Failed");
            }
            alert("Registration successful!");
            navigate("/login");
        } catch (err) {
            setError(err.message);
        }
    };

    return (
      <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
          <h2>Register</h2>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <form onSubmit={handleSubmit}>
              <input
                  type="text"
                  name="full_name"
                  placeholder="Name"
                  value={formData.full_name}
                  onChange={handleChange}
                  required
              />
              <br />
              <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
              />
              <br />
              <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={formData.password}
                  onChange={handleChange}
                  required
              />
              <br />
              <button type="submit">Register</button>
          </form>
          <button onClick={() => navigate("/login")} style={{ marginTop: "10px" }}>
              Login
          </button>
          <button onClick={() => window.location.href = "http://localhost:8000/auth/login/google"} style={{ marginTop: "10px" }}>
              Login with Google
          </button>
      </div>
  );  
};

export default Register;
