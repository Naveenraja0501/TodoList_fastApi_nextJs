import { useState } from "react";
import axiosInstance from "../utils/axiosInstance";
import Link from "next/link"; 
import "../styles/SignUp.css"; 

export default function SignUp() {
  const [form, setForm] = useState({ user_name: "", user_email: "", password: "" });
  const [message, setMessage] = useState("");           // success/error message
  const [messageType, setMessageType] = useState("");   // 'success' or 'error'

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axiosInstance.post("/signup", form);
      setMessage("Signup successful! You can now login.");
      setMessageType("success");
      setForm({ user_name: "", user_email: "", password: "" });
    } catch (error) {
      console.error(error);
      setMessage("Signup failed! Please try again.");
      setMessageType("error");
    }

    // Hide message after 3 seconds
    setTimeout(() => {
      setMessage("");
      setMessageType("");
    }, 3000);
  };

  return (
    <div className="container">
      <div className="form-container">
        <div className="highlighted-card">
          <form onSubmit={handleSubmit}>
            <h2>Sign Up</h2>

            {/* Notification Message */}
            {message && (
              <div className={`notification ${messageType}`}>
                {message}
              </div>
            )}

            <input
              type="text"
              placeholder="Full Name"
              value={form.user_name}
              onChange={(e) => setForm({ ...form, user_name: e.target.value })}
              required
            />

            <input
              type="email"
              placeholder="Email"
              value={form.user_email}
              onChange={(e) => setForm({ ...form, user_email: e.target.value })}
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />

            <button type="submit">Sign Up</button>

            <p>
              Already have an account? <Link href="/signin">Login</Link>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}
