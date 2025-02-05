import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Profile from "./components/Profile";
import AuthCallback from "./components/AuthCallback";
import ResetPassword from "./components/ResetPassword";
import ProfileRedirect from './components/ProfileRedirect';

function App() {
    return (
        <div>
            <h1>FastAPI Auth</h1>
            <Routes>
                <Route path="/" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/auth/callback" element={<AuthCallback />} />
                <Route path="/reset-password" element={<ResetPassword />} />
                <Route path="/profile-redirect" element={<ProfileRedirect />} />
            </Routes>
        </div>
    );
}

export default App;
